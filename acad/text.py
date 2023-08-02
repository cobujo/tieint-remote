from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbTextBase
from mylogger import logger


@dataclass
class AcDbText(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def alignment(self):
        return self.obj.Alignment

    @property
    def backward(self):
        return self.obj.Backward

    @property
    def height(self):
        return self.obj.Height

    @property
    def insertion_point(self):
        return self.obj.InsertionPoint

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def oblique_angle(self):
        return self.obj.ObliqueAngle

    @property
    def rotation(self):
        return self.obj.Rotation

    @property
    def scale_factor(self):
        return self.obj.ScaleFactor

    @property
    def style_name(self):
        return self.obj.StyleName

    @property
    def text_alignment_point(self):
        return self.obj.TextAlignmentPoint

    @property
    def text_generation_flag(self):
        return self.obj.TextGenerationFlag

    @property
    def text_string(self):
        return self.obj.TextString

    @property
    def thickness(self):
        return self.obj.Thickness

    @property
    def upside_down(self):
        return self.obj.UpsideDown

    def field_code(self):
        return self.obj.FieldCode()

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbTextBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'insertion_point'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')
