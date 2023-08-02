from dataclasses import dataclass, field
from typing import Optional
import win32com.client as client
from acad.utils import AcadUtil
from sql.models import AcadDynamicBlockReferencePropertyBase
from acad.comwrapper import ComWrapper


@dataclass
class AcadDynamicBlockReferenceProperty(AcadUtil):
    """
    created manually
    """
    com_obj: client.CDispatch
    obj: ComWrapper = field(init=False)
    _block_reference_handle: Optional[str] = None

    def __post_init__(self):
        self.obj = ComWrapper(self.com_obj)

    @property
    def block_reference_handle_(self):
        return self._block_reference_handle

    @property
    def allowed_values(self):
        return self.obj.AllowedValues

    @property
    def description(self):
        return self.obj.Description

    @property
    def property_name(self):
        return self.obj.PropertyName

    @property
    def read_only(self):
        return self.obj.ReadOnly

    @property
    def show(self):
        return self.obj.Show

    @property
    def units_type(self):
        return self.obj.UnitsType

    @property
    def value(self):
        return self.obj.Value

    def db_process_in_session_(self, session, space=None):
        if not self.block_reference_handle_:
            raise ValueError(f'adding row to {AcadDynamicBlockReferencePropertyBase.__tablename__} requires block reference handle (foreign key) to be set; this is generated based on what block this comes from')

        # value can be anything (float, str, tuple); right now just making it a string for db import
        # may want to add a typedecorator for handling this coming out of the db in the future?
        sql_dct = self._dict_from_shared(model=AcadDynamicBlockReferencePropertyBase)
        sql_dct['value'] = str(sql_dct['value'])

        self.db_add_in_session_(model=AcadDynamicBlockReferencePropertyBase, session=session, space=space, dct=sql_dct)
