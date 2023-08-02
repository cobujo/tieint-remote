from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbCircleBase
from mylogger import logger


@dataclass
class AcDbCircle(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def area(self):
        return self.obj.Area

    @property
    def center(self):
        return self.obj.Center

    @property
    def circumference(self):
        return self.obj.Circumference

    @property
    def diameter(self):
        return self.obj.Diameter

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def radius(self):
        return self.obj.Radius

    @property
    def thickness(self):
        return self.obj.Thickness

    def offset(self, distance):
        return self.obj.Offset(Distance=distance)

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbCircleBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'center'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')
