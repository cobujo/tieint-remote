from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbArcBase
from mylogger import logger


@dataclass
class AcDbArc(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def arc_length(self):
        return self.obj.ArcLength

    @property
    def area(self):
        return self.obj.Area

    @property
    def center(self):
        return self.obj.Center

    @property
    def end_angle(self):
        return self.obj.EndAngle

    @property
    def end_point(self):
        return self.obj.EndPoint

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def radius(self):
        return self.obj.Radius

    @property
    def start_angle(self):
        return self.obj.StartAngle

    @property
    def start_point(self):
        return self.obj.StartPoint

    @property
    def thickness(self):
        return self.obj.Thickness

    @property
    def total_angle(self):
        return self.obj.TotalAngle

    def offset(self, distance):
        return self.obj.Offset(Distance=distance)

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbArcBase, session=session, space=space)
        if not instance:
            return

        coord_attrs = ['center', 'start_point', 'end_point']
        reqd_coords = coord_attrs
        coord_import = [self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=a, space=space, obj_instance=instance) for a in coord_attrs]

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_coords):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
