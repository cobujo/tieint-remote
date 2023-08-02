from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbEllipseBase
from mylogger import logger


@dataclass
class AcDbEllipse(AcadEntity, AcadUtil):
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
    def end_angle(self):
        return self.obj.EndAngle

    @property
    def end_parameter(self):
        return self.obj.EndParameter

    @property
    def end_point(self):
        return self.obj.EndPoint

    @property
    def major_axis(self):
        return self.obj.MajorAxis

    @property
    def major_radius(self):
        return self.obj.MajorRadius

    @property
    def minor_axis(self):
        return self.obj.MinorAxis

    @property
    def minor_radius(self):
        return self.obj.MinorRadius

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def radius_ratio(self):
        return self.obj.RadiusRatio

    @property
    def start_angle(self):
        return self.obj.StartAngle

    @property
    def start_parameter(self):
        return self.obj.StartParameter

    @property
    def start_point(self):
        return self.obj.StartPoint

    def offset(self, distance):
        return self.obj.Offset(Distance=distance)

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbEllipseBase, session=session, space=space)

        coord_attrs = ['center', 'start_point', 'end_point', 'minor_axis', 'major_axis']
        reqd_attrs = ['center', 'start_point', 'end_point']
        coord_import = [self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=a, space=space, obj_instance=instance) for a in coord_attrs]

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attrs):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')
