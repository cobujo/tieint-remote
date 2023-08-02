from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbLineBase
from mylogger import logger


@dataclass
class AcDbLine(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def angle(self):
        return self.obj.Angle

    @property
    def delta(self):
        return self.obj.Delta

    @property
    def end_point(self):
        return self.obj.EndPoint

    @property
    def length(self):
        return self.obj.Length

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def start_point(self):
        return self.obj.StartPoint

    @property
    def thickness(self):
        return self.obj.Thickness

    def offset(self, distance):
        return self.obj.Offset(Distance=distance)

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbLineBase, session=session, space=space)
        if not instance:
            return

        coord_attrs = ['start_point', 'end_point']
        reqd_attrs = coord_attrs
        coord_import = [self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=a, space=space, obj_instance=instance) for a in coord_attrs]

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attrs):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')
