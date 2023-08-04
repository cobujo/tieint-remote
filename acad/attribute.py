from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbAttributeBase
from typing import Optional
from mylogger import logger


@dataclass
class AcDbAttribute(AcadEntity, AcadUtil):
    """
    autoscript generated
    This appears to also be an AttributeReference in the docs?
    Not sure if there's a difference between the two
    """
    _block_reference_handle: Optional[str] = None

    @property
    def block_reference_handle_(self):
        return self._block_reference_handle

    @property
    def alignment(self):
        return self.obj.Alignment

    @property
    def backward(self):
        return self.obj.Backward

    @property
    def constant(self):
        return self.obj.Constant

    @property
    def field_length(self):
        return self.obj.FieldLength

    @property
    def height(self):
        return self.obj.Height

    @property
    def insertion_point(self):
        return self.obj.InsertionPoint

    @property
    def invisible(self):
        return self.obj.Invisible

    @property
    def lock_position(self):
        return self.obj.LockPosition

    @property
    def mode(self):
        return self.obj.Mode

    @property
    def m_text_attribute(self):
        return self.obj.MTextAttribute

    @property
    def m_text_attribute_content(self):
        return self.obj.MTextAttributeContent

    @property
    def m_text_boundary_width(self):
        return self.obj.MTextBoundaryWidth

    @property
    def m_text_drawing_direction(self):
        return self.obj.MTextDrawingDirection

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def oblique_angle(self):
        return self.obj.ObliqueAngle

    @property
    def preset(self):
        return self.obj.Preset

    @property
    def prompt_string(self):
        return self.obj.PromptString

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
    def tag_string(self):
        return self.obj.TagString

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

    @property
    def verify(self):
        return self.obj.Verify

    def update_m_text_attribute(self):
        return self.obj.UpdateMTextAttribute()

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        if not self._block_reference_handle:
            raise ValueError(f'adding row to {AcDbAttributeBase.__tablename__} requires block reference id to connect what this attribute belongs to')

        instance = self.db_add_in_session_(model=AcDbAttributeBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'insertion_point'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
