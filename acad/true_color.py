from dataclasses import dataclass, field
from typing import Optional
import win32com.client as client
from acad.utils import AcadUtil
from sql.models import AcadAcCmColorBase
from acad.comwrapper import ComWrapper


@dataclass
class AcadAcCmColor(AcadUtil):
    """
    created manually to capture color props from AcDbHatch
    """
    com_obj: client.CDispatch
    obj: ComWrapper = field(init=False)
    _id: Optional[str] = None

    def __post_init__(self):
        self.obj = ComWrapper(self.com_obj)

    # silly, but want to allow id to be entered on init, but also to be __class__.__name__ property, so it'll come up as shared property with sql model
    @property
    def id_(self):
        return self._id

    @property
    def blue(self) -> int:
        return self.obj.Blue

    @property
    def book_name(self) -> str:
        return self.obj.BookName

    @property
    def color_index(self):
        return self.obj.ColorIndex

    @property
    def color_method(self):
        return self.obj.ColorMethod

    @property
    def color_name(self) -> str:
        return self.obj.ColorName

    @property
    def entity_color(self) -> int:
        return self.obj.EntityColor

    @property
    def green(self) -> int:
        return self.obj.Green

    @property
    def red(self) -> int:
        return self.obj.Red

    def db_process_in_session_(self, session, space=None):
        # any cases when we would add to db without generating id_ (foreign key to another object table)?
        if not self.id_:
            raise ValueError(f'adding row to {AcadAcCmColorBase.__tablename__} requires id (foreign key) to be set; this is generated based on what object and property the color is from')

        self.db_add_in_session_(model=AcadAcCmColorBase, session=session, space=space)
