from dataclasses import dataclass, field
from typing import Optional
import win32com.client as client
from acad.utils import AcadUtil
from sql.models import AcadSummaryInfoBase
from acad.comwrapper import ComWrapper


@dataclass
class AcadSummaryInfo(AcadUtil):
    """
    autoscript generated
    """
    com_obj: client.CDispatch
    obj: ComWrapper = field(init=False)
    _document_name: Optional[str] = None

    def __post_init__(self):
        self.obj = ComWrapper(self.com_obj)

    # similar to AcadAcCmColor with id
    @property
    def document_name_(self):
        return self._document_name

    @property
    def author(self):
        return self.obj.Author

    @property
    def comments(self):
        return self.obj.Comments

    @property
    def hyperlink_base(self):
        return self.obj.HyperlinkBase

    @property
    def keywords(self):
        return self.obj.Keywords

    @property
    def last_saved_by(self):
        return self.obj.LastSavedBy

    @property
    def revision_number(self):
        return self.obj.RevisionNumber

    @property
    def subject(self):
        return self.obj.Subject

    @property
    def title(self):
        return self.obj.Title

    def add_custom_info(self, key, value):
        return self.obj.AddCustomInfo(key=key, Value=value)

    def get_custom_by_index(self, index, p_key, p_value):
        return self.obj.GetCustomByIndex(Index=index, pKey=p_key, pValue=p_value)

    def get_custom_by_key(self, key, p_value):
        return self.obj.GetCustomByKey(key=key, pValue=p_value)

    def num_custom_info(self):
        return self.obj.NumCustomInfo()

    def remove_custom_by_index(self, index):
        return self.obj.RemoveCustomByIndex(Index=index)

    def remove_custom_by_key(self, key):
        return self.obj.RemoveCustomByKey(key=key)

    def set_custom_by_index(self, index, key, value):
        return self.obj.SetCustomByIndex(Index=index, key=key, Value=value)

    def set_custom_by_key(self, key, value):
        return self.obj.SetCustomByKey(key=key, Value=value)

    def db_process_in_session_(self, session, space=None):
        if not self.document_name_:
            raise ValueError(f'adding to {AcadSummaryInfoBase.__tablename__} requires document name (foreign key) to be set to link to document table')

        self.db_add_in_session_(model=AcadSummaryInfoBase, session=session, space=space)
