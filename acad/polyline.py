from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbPolylineBase
from pywintypes import com_error
import warnings
from mylogger import logger


@dataclass
class AcDbPolyline(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def area(self):
        return self.obj.Area

    @property
    def closed(self):
        return self.obj.Closed

    @property
    def constant_width(self):
        try:
            return self.obj.ConstantWidth
        except com_error:
            return

    @property
    def coordinates(self):
        return self.obj.Coordinates

    @property
    def elevation(self):
        return self.obj.Elevation

    @property
    def length(self):
        return self.obj.Length

    @property
    def linetype_generation(self):
        return self.obj.LinetypeGeneration

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def thickness(self):
        return self.obj.Thickness

    # not storing in db, not consistently working
    @property
    def type_(self):
        return self.obj.Type

    @staticmethod
    def append_vertex():
        warnings.warn('append_vertex raising AttributeError: <unknown>.AppendVertex')

    # LISTED AS PROPERTY IN ACAD ACTIVEX DOCS BUT IS ACTUALLY A METHOD!
    def coordinate(self, index):
        return self.obj.Coordinate(index)

    def explode(self):
        return self.obj.Explode()

    def get_bulge(self, index):
        return self.obj.GetBulge(Index=index)

    def get_width(self, index, start_width, end_width):
        return self.obj.GetWidth(Index=index, StartWidth=start_width, EndWidth=end_width)

    def offset(self, distance):
        return self.obj.Offset(Distance=distance)

    def set_bulge(self, index, bulge):
        return self.obj.SetBulge(Index=index, bulge=bulge)

    def set_width(self, index, start_width, end_width):
        return self.obj.SetWidth(Index=index, StartWidth=start_width, EndWidth=end_width)

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbPolylineBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'coordinates'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_2d_coordinates_array_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
