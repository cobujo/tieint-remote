from dataclasses import dataclass, field
from sql import session_scope, engine_named, safe_check_dot_db
from sql.helpers import query_stmt, db_add_or_merge, ss_result_to_namedtuples
from sql.models import (
    AcadDocumentBase,
    DesignError,
    AcDbAttributeBase,
    TitleBlockEtc,
    AcDbBlockReferenceBase,
    RevStrip
)
from sqlalchemy.orm import ColumnProperty
from settings import constants as cn
from mylogger import logger
from typing import Optional
from operator import attrgetter
from itertools import groupby
import json

def processing_error(category: str, friendly: str, verbose: str, fatal: bool, session):
    if fatal:
        friendly = f'Unable to proceed! {friendly}'
        logger.error(friendly)
    else:
        logger.warning(friendly)

    de = DesignError(category=category, friendly=friendly, verbose=verbose, fatal=fatal)
    session.add(de)


def matching_records_attrs(rows: list, model, field_name: str, content_field_name: str) -> Optional[dict]:
    """
    Given rows of attributes in a block, get all values for a given field name and return which ones
    match against columns in a given model
    Expecting to use this when querying for all attributes in a block, and putting desired content from each attribute
    into a block table
    :param rows:
    :param model:
    :param field_name:
    :param content_field_name:
    :return:
    """
    try:
        # below dict will have column names as keys, not arg names
        attr_dict_all = {getattr(r, field_name): getattr(r, content_field_name) for r in rows}
    except AttributeError:
        logger.error(f'object {rows[0]} is missing one or both attributes: {field_name}, {content_field_name}')
        return

    # we're checking the field names in the rows against the column names, BUT returning them on the arg name,
    # so that it can be loaded into the model instance.  This should be the same in most cases but varies
    # i.e. arg->dwg, column->DWG#
    column_arg_mapping = {prop.columns[0].name: prop.key for prop in model.__mapper__.iterate_properties if isinstance(prop, ColumnProperty)}
    model_cols = list(column_arg_mapping.keys())

    attr_dict = {column_arg_mapping[k]: v for k, v in attr_dict_all.items() if k in model_cols}

    # handle case where target table class has document_name but source table (acad object) has document
    try:
        doc = rows[0].document
    except AttributeError:
        doc = None

    if doc and 'document_name' in model_cols:
        attr_dict['document_name'] = doc

    return attr_dict


def get_blocks_from_name(session, name):
    dwgs = session.query(AcDbBlockReferenceBase).filter_by(name=name).distinct().all()
    if not dwgs:
        return

    return dwgs


@dataclass
class PkgQuery(object):
    """
    As a general rule, helper functions with preceding _ will take the session scope as an arg,
    because it's expected this will run within a larger function that will initialize the session
    """
    db_name: str
    db: str = field(init=False)

    def __post_init__(self):
        self.db = safe_check_dot_db(self.db_name)

    @staticmethod
    def _get_owned_dwg_list(ss):
        # looking for SSOE Logo block
        blocks = get_blocks_from_name(ss, cn.OWNED_DWG_BLOCK_NAME)
        if not blocks:
            return

        return [b.document for b in blocks]

    @staticmethod
    def _get_ifr_dwg_list(ss):
        blocks = get_blocks_from_name(ss, cn.IFR_BLOCK_NAME)
        if not blocks:
            return

        return [b.document for b in blocks]

    @staticmethod
    def _get_nfc_dwg_list(ss):
        blocks = get_blocks_from_name(ss, cn.NFC_BLOCK_NAME)
        if not blocks:
            return

        return [b.document for b in blocks]

    def build_titleblocks(self):
        with session_scope(engine_named(self.db)) as ss:
            # don't want to assume all sheets have the same title block name (especially IFR sheets by other firms
            # we'll look for an attribute with tag_string = 'DWG#', should be common attribute among all title blocks
            tblock_dwg_attrs_q = ss.query(AcDbAttributeBase).filter_by(tag_string=cn.TITLE_BLOCK_REQUIRED_ATTR).group_by(AcDbAttributeBase.handle)
            tblock_dwg_attrs = tblock_dwg_attrs_q.all()
            if not tblock_dwg_attrs:
                friendly = 'Titleblocks are not as expected'
                verbose = f'{query_stmt(tblock_dwg_attrs_q)} returns 0 rows'
                processing_error(category='title block', friendly=friendly, verbose=verbose, fatal=True, session=ss)
                return

            owned_dwg_list = self._get_owned_dwg_list(ss)
            ifr_dwg_list = self._get_ifr_dwg_list(ss)
            nfc_dwg_list = self._get_nfc_dwg_list(ss)

            doc_list = []
            for attr in tblock_dwg_attrs:
                # query for all attrs under the block returned given the title block required attr query
                tblock_attrs = ss.query(AcDbAttributeBase).filter_by(block_reference_handle_=attr.block_reference_handle_).group_by(AcDbAttributeBase.handle).all()
                # get attr dictionary for all fields that match the TitleBlock table
                # (should still work for other firms titleblock, but may not return as many values)
                attr_dict = matching_records_attrs(rows=tblock_attrs, model=TitleBlockEtc, field_name='tag_string', content_field_name='text_string')
                tb = TitleBlockEtc(**attr_dict)
                if tb.document_name not in doc_list:
                    doc_list.append(tb.document_name)

                    if owned_dwg_list:
                        tb.owned_dwg_ = tb.document_name in owned_dwg_list

                    if ifr_dwg_list:
                        tb.ifr_dwg_ = tb.document_name in ifr_dwg_list

                    if nfc_dwg_list:
                        tb.nfc_dwg_ = tb.document_name in nfc_dwg_list

                    db_add_or_merge(instance=tb, session_scope=ss)
                else:
                    logger.warning(f'{tb.document_name} was already added, are there multiple titleblocks in this drawing?')

    def build_rev_strips(self):
        with session_scope(engine_named(self.db)) as ss:
            rev_strip_blocks_q = ss.query(AcDbBlockReferenceBase).filter(AcDbBlockReferenceBase.name.like(cn.REV_STRIP_NAME_SSOE)).group_by(AcDbBlockReferenceBase.handle)
            rev_strip_blocks = rev_strip_blocks_q.all()
            if not rev_strip_blocks:
                friendly = 'no rev strips found'
                verbose = f'{query_stmt(rev_strip_blocks_q)} returns 0 rows'
                processing_error(category='rev strip error', friendly=friendly, verbose=verbose, fatal=True, session=ss)
                return

            # group rev strip blocks by document name, and order by y coordinate
            # (not using coordinates table for this)
            rev_strip_blocks.sort(key=lambda x: (x.document, x.insertion_point[1]))
            rs_blocks_grouped = groupby(rev_strip_blocks, key=attrgetter('document'))

            for doc, revs in rs_blocks_grouped:
                # since we're ordering by y coord ascending, let's define a rank to easily identify and list what the rev order should be for each document
                for rank, rev in enumerate(revs):
                    rev_attrs_q = ss.query(AcDbAttributeBase).filter_by(block_reference_handle_=rev.handle).group_by(AcDbAttributeBase.handle).order_by(AcDbAttributeBase.handle)
                    rev_attrs = rev_attrs_q.all()
                    if not rev_attrs:
                        friendly = 'revision strip has no attributes'
                        verbose = f'{query_stmt(rev_attrs_q)} returns 0 rows'
                        processing_error(category='rev strip error', friendly=friendly, verbose=verbose, fatal=False, session=ss)

                    attr_dict = matching_records_attrs(rows=rev_attrs, model=RevStrip, field_name='tag_string', content_field_name='text_string')

                    rs = RevStrip(**attr_dict)
                    # due to tag_string not having a unique requirement in a block, and allowing invalid chars, need to manually get the rev numbers under '#'
                    # ther are two '#' tags, the main one used will have the larger height
                    hashes = [ra for ra in rev_attrs if ra.tag_string == '#']
                    hashes.sort(key=attrgetter('height'), reverse=True)

                    rs.hash_1 = hashes[0].text_string
                    rs.hash_2 = hashes[1].text_string
                    rs.rank_ = rank
                    rs.block_reference_handle_ = rev.handle

                    db_add_or_merge(instance=rs, session_scope=ss)
