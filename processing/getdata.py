import os
from settings import auto_config as cfg
from typing import Optional
from os import listdir, path
from os.path import isfile, join
from acad.document import AcadDocument
from tenacity import retry, stop_after_attempt, TryAgain, wait_incrementing
from mylogger import logger, my_before_sleep
from pywintypes import com_error
from sql import session_scope, engine_named, safe_check_dot_db
from acad import get_or_init_acad_raw
from sql.models import metadata, HandleCheckBase
from sql.helpers import db_add_or_merge
from time import sleep
import re


def parse_filename(filename: str) -> Optional[tuple]:
    """
    regex pattern info:
    (.+) -> getting the first group before...
    (([GAMES]|-?IP) -> start of next group either begins with GAMES, IP, or -IP
    \d{2} -> followed by 2 digits
    \w{0,2} -> followed by 0, 1, or 2 letters
    (?i) -> optional, followed by i
    \.DWG -> end of string expected to be .DWG
    :param filename:
    :return:
    """
    pattern = '(.+)(([GAMES]|-?IP)\d{2}\w{0,2}(?i)\.DWG)'
    match = re.search(pattern, filename, re.DOTALL)
    try:
        tn, dn = match.group(1), match.group(2)
        # there should not be any hyphens in tool name; not expecting hyphens in drawing name but could exist for legacy files (i.e. IP sheets?)
        tn = tn.replace('-', '')
        return tn, dn
    except IndexError:
        logger.error(f'unable to parse expected tool name, drawing name from filename: {filename}')
        return


@retry(stop=stop_after_attempt(4), wait=wait_incrementing(start=5, increment=5, max=30), before_sleep=my_before_sleep)
def acad_open_doc_raw(file: str, acad_app=None):
    """
    isolated function to open DWG in AutoCAD in order to control retries
    :param file: str
        validated outside this function
    :param acad_app: win32com.client.dynamic.Dispatch
        expecting to pass an initialized app.  If None, will attemtp to initialize
    :return:
    """
    if not acad_app:
        acad_app = get_or_init_acad_raw()

    try:
        # TODO: Medium -> like get_or_init_acad_raw(), change this func to detect if the doc is already open and use that
        doc_raw = acad_app.Documents.Open(file)
        if not doc_raw:
            logger.info(f'no COM object for the document returned for file: {file}, trying again...')
            raise TryAgain

        return doc_raw
    except com_error as e:
        if e.strerror == 'The RPC server is unavailable.':  # this is the error we expect when AutoCAD is closed
            logger.info('No AutoCAD instance detected, starting new instance...')
            raise TryAgain
        # we're already using ComWrapper to avoid this (indicative of not getting a response in time) but may need to account for it here as well
        elif e.strerror == 'Call was rejected by callee.':
            callee_sleep = 1
            logger.info(f'Getting a call rejected error, sleeping for {callee_sleep} second(s)...')
            sleep(1)
            raise TryAgain
        else:
            logger.error(f'unexpected com_error! {e}')
            return


def db_process_doc_with_recovery(doc: AcadDocument, db_name: str, spaces: tuple):
    """
    Similar to document.db_process_in_session_everything_, but allows for document to be recovered in case of crash, and db import to continue
    :param doc:
    :param db_name:
    :param spaces:
    :return:
    """
    with session_scope(engine_named(db_name)) as ss:
        doc.db_process_in_session_(session=ss)

    full_name = doc.full_name
    doc_name = doc.name
    for space in spaces:
        acad_results = doc.set_get_acad_results_from_space(space=space)
        objs = acad_results.acad_objs
        if objs:
            handles = [o.handle for o in objs]
            if not handles:
                raise ValueError(f'unable to get handles from document: {doc_name}')

            # load all handles found in the document into the table with init status
            handle_instances = [HandleCheckBase(handle=h, document_name=doc_name, status='init') for h in handles]
            with session_scope(engine_named(db_name)) as ss:
                [db_add_or_merge(instance=i, session_scope=ss) for i in handle_instances]
                logger.info('handles initialized...')

            while objs:
                obj = objs.pop(0)
                try:
                    doc_ok = doc.active  # if file (doc) is not open, will error out here
                    if not doc_ok:
                        raise RuntimeError('doc is not ok')

                    with session_scope(engine_named(db_name)) as ss:
                        try:
                            handle = obj.handle
                            obj.db_process_in_session_(session=ss, space=space)
                            handle_instance = HandleCheckBase(handle=handle, document_name=doc_name, status='ok')
                            ss.merge(handle_instance)
                            logger.info(f'imported object, handle: {handle}')
                        except Exception as e:
                            if handle:
                                e_msg = e.args[0]
                                handle_instance = HandleCheckBase(handle=handle, document_name=doc_name, status='error', message=e_msg)
                                ss.merge(handle_instance)
                                logger.error(f'error importing object, handle: {handle}')

                            else:
                                logger.error('unable to get handle of object, status unknown')

                except (com_error, AttributeError, RuntimeError):
                    logger.info(f'attempting to restart AutoCAD, on file: {full_name}')
                    doc_raw = acad_open_doc_raw(file=full_name)
                    logger.info('sleep 10...')
                    sleep(10)
                    doc = AcadDocument(doc_raw)
                    acad_results = doc.set_get_acad_results_from_space(space=space)
                    objs_all = acad_results.acad_objs
                    # query for handle status and get filtered down list of objects left for import
                    with session_scope(engine_named(db_name)) as ss:
                        remaining = ss.query(HandleCheckBase).filter(HandleCheckBase.status == 'init', HandleCheckBase.document_name == doc_name).all()
                        handles_remaining = [r.handle for r in remaining]

                    objs = [o for o in objs_all if o.handle in handles_remaining]

        else:
            logger.info(f'no objects in {doc.name}, {space}space to import to db')


def db_name_from_filename(filename):
    tool_name, drawing_name = parse_filename(filename)
    if all([tool_name, drawing_name]):
        return tool_name

    logger.error(f'unable to determine db_name from filename: {filename}, check filename or parsing function for issue')
    return


def dwg_to_db(directory: str, filename: str, db_name: Optional[str] = None, acad_app=None, spaces: tuple = ('paper',)):
    """
    Singular function to process DWG to database
    Uses separate sessions for each DWG (no performance benefit at this point to use one session for multiple DWGs)
    :param directory: str
        directory path that holds DWG
    :param filename: str
        must be valid DWG
    :param db_name: str
        if None, will try to determine tool name from DWG filename
        *WARNING* probably safest to define this at the directory/batch level and pass it; processing RPs with multiple CEIDs will result in
        multiple dbs when processing sheets for different CEIDs
    :param acad_app: win32com.client.dynamic.Dispatch
        expecting to pass an initialized app.  If None, will attemtp to initialize
    :param spaces: tuple
        paper, model, or both
    :return:
    """
    if not acad_app:
        acad_app = get_or_init_acad_raw()

    if not db_name:
        db_name = db_name_from_filename(filename)
        if not db_name:
            return

    file = path.join(directory, filename)
    # TODO: NOW! fix below, test if doc_raw is in fact COM (CDispatch) object!
    doc_raw = acad_open_doc_raw(file=file, acad_app=acad_app)
    doc = AcadDocument(doc_raw)
    doc.purge_all()

    db_process_doc_with_recovery(doc=doc, db_name=db_name, spaces=spaces)

    try:
        doc.close(save_changes=False, file_name=doc.name)
        logger.info('doc closed')
    except Exception as e:
        logger.warning(f'unable to close doc (did it already crash?), error -> {e}')


def del_dbs_from_sql_dir(db_name: Optional[str] = None):
    """
    Function to delete either a specific db, or all db files from the sql directory.
    Used before creating a new db
    :param db_name: str
        if not provided, will delete all .db files from sql directory.
        *does not have to have the file extension, if it doesn't we'll add it
    :return:
    """
    if db_name:
        db_name = safe_check_dot_db(db_name)
        dbs_to_del = [db_name]

    else:
        files = [f for f in listdir(cfg.DB_DIR) if isfile(join(cfg.DB_DIR, f))]
        dbs_to_del = [f for f in files if f.lower().endswith('.db')]

    if not dbs_to_del:
        return

    [os.remove(join(cfg.DB_DIR, db)) for db in dbs_to_del]


def dir_to_db(directory: str, db_name: Optional[str] = None, create_new_db: Optional[bool] = True):
    """
    Complete function for processing entire directory of DWGs
    :param directory: str
        directory path that holds DWG
    :param db_name: str
        if not passed, will determine db name from G01.DWG
    :param create_new_db: boolean
        if True, will create new db.  Set to False if using existing db
    :return:
    """
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    if not files:
        logger.error(f'no files found in: {directory}, exiting function')
        return

    dwgs = [f for f in files if f.lower().endswith('.dwg')]
    if not dwgs:
        logger.error(f'no DWGs found in: {directory}, exiting function')
        return

    # if db_name is not passed, figure it out from G01.DWG
    if not db_name:
        try:
            g01 = next(f for f in dwgs if f.lower().endswith('g01.dwg'))
        except StopIteration:
            logger.error(f'db_name not passed, and unable to find G01 sheet for determining correct db name, exiting function')
            return

        db_name = db_name_from_filename(g01)
        if not db_name:
            return

    if create_new_db:
        del_dbs_from_sql_dir()
        metadata.create_all(bind=engine_named(db_name))

    for dwg in dwgs:
        logger.info(f'processing {dwg}...')
        dwg_to_db(directory=directory, filename=dwg, db_name=db_name)

    logger.info('processing complete!')
