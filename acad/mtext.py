from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbMTextBase
from mylogger import logger


@dataclass
class AcDbMText(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def attachment_point(self):
        return self.obj.AttachmentPoint

    @property
    def background_fill(self):
        return self.obj.BackgroundFill

    @property
    def drawing_direction(self):
        return self.obj.DrawingDirection

    @property
    def height(self):
        return self.obj.Height

    @property
    def insertion_point(self):
        return self.obj.InsertionPoint

    @property
    def line_spacing_distance(self):
        return self.obj.LineSpacingDistance

    @property
    def line_spacing_factor(self):
        return self.obj.LineSpacingFactor

    @property
    def line_spacing_style(self):
        return self.obj.LineSpacingStyle

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def rotation(self):
        return self.obj.Rotation

    @property
    def style_name(self):
        return self.obj.StyleName

    @property
    def text_string(self):
        return self.obj.TextString

    @property
    def width(self):
        return self.obj.Width

    def field_code(self):
        return self.obj.FieldCode()

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbMTextBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'insertion_point'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
