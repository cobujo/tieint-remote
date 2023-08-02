from dataclasses import dataclass, field
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.exc import IntegrityError
from mylogger import logger
from typing import Optional
import warnings
from acad import Spaces
from sql.models import AcadAttributeErrorsBase
from sql.helpers import db_add_or_merge
from settings import constants as cn


@dataclass
class AcadAttributeError:
    name: Optional[str] = None
    error: Optional[str] = None


@dataclass
class AcadUtil(object):
    """
    We want these methods available to everything, not just children of AcadObject (i.e. AcadDocument), hence the separate class
    """
    attr_errors: Optional[list[AcadAttributeError]] = field(default_factory=list, init=False)

    @classmethod
    def _all_props(cls):
        return [p for p in dir(cls) if getattr(cls, p).__class__.__name__ == 'property']

    @classmethod
    def _shared_props(cls, model):
        model_columns = [c.name for c in model.__table__.columns]
        return list(set(cls._all_props()) & set(model_columns))

    def getattr_handle_errors(self, name):
        try:
            return getattr(self, name)
        except Exception as e:
            self.attr_errors.append(AcadAttributeError(name=name, error=repr(e)))
            # reason to return "flag" value indicating attr error other than None?
            # at this time just go with None
            return

    def _dict_from_shared(self, model, excludes: Optional[iter] = None):
        # from shared properties <-> columns, create dictionary
        shared = self._shared_props(model)
        if excludes:
            shared = [s for s in shared if s not in excludes]

        return {s: self.getattr_handle_errors(s) for s in shared}

    def db_add_in_session_(self, model: DeclarativeMeta, session, space: Optional[str] = None,
                           dct: Optional[dict] = None, process_attr_errors=True):
        """
        baseline function for translating acad models -> sql model and adding to db
        will need to override this method for more complex models, i.e. models that have attributes that are additional acad models
        :param model: sql model
        :param session: session_scope(bind=engine)
            creating function to be within session for efficiency; expecting to call function many times within a single session
        :param space: str
            paper or model *** we can't get this from native acad obj attributes but this may be valuable, so will need to manually add it on db process ***
        :param dct: dict
            if provided, will input this dictionary into sql model instance, otherwise will find shared attrs between obj and sql model
        :param process_attr_errors: bool
            if true, import into db attr errors if present
        :return:
        """
        if not dct:
            dct = self._dict_from_shared(model)
            if not dct:
                raise ValueError(
                    f'No shared properties between class ({self.__class__.__name__}) and sql model ({model.__name__}), unable to process')

        # BAND-AID: adding line below due to receiving this out of nowhere on _db_process, why?
        # TypeError: unhashable type: 'AcadDocument'
        if 'document' in dct:
            if hasattr(dct['document'], 'name'):
                dct['document'] = dct['document'].name
            # TEMP!!!
            else:
                logger.warning('document not in dictionary!')
                dct['document'] = 'no doc'

        instance = model(**dct)

        try:
            if hasattr(instance, cn.SPACE_ATTR_NAME):
                if space in Spaces:
                    setattr(instance, cn.SPACE_ATTR_NAME, space)
                else:
                    # TODO: Mild -> store "space" exceptions somewhere else?  Build more complete list?
                    if model not in ['AcadSummaryInfoBase', 'AcadLayerBase']:
                        logger.warning(
                            f'db model: {model.__name__} has {cn.SPACE_ATTR_NAME} attribute but your value ({space}) is not valid!')
        except TypeError:
            logger.error(
                f'attribute name must be a string, you put: {cn.SPACE_ATTR_NAME}, type: {type(cn.SPACE_ATTR_NAME)}')

        db_add_or_merge(instance=instance, session_scope=session)

        logger.info(f"queued {model.__name__} to db, handle: {dct.get('handle')}")

        if process_attr_errors:
            if self.attr_errors:
                logger.info(f'there are {len(self.attr_errors)} errors...')
                attr_e_instances = [
                    AcadAttributeErrorsBase(
                        document_name=dct.get('document'),
                        object_id=dct.get('object_id'),
                        handle=dct.get('handle'),
                        space=space,
                        attr_name=a.name,
                        attr_error=a.error
                    ) for a in self.attr_errors
                ]

                [db_add_or_merge(instance=i, session_scope=session) for i in attr_e_instances]
                logger.warning(f'added {len(self.attr_errors)} attr errors to db')

        return instance
