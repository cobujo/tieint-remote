from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbLeaderBase
from mylogger import logger


@dataclass
class AcDbLeader(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def annotation(self):
        return self.obj.Annotation

    @property
    def arrowhead_block(self):
        return self.obj.ArrowheadBlock

    @property
    def arrowhead_size(self):
        return self.obj.ArrowheadSize

    @property
    def arrowhead_type(self):
        return self.obj.ArrowheadType

    @property
    def coordinates(self):
        return self.obj.Coordinates

    @property
    def dimension_line_color(self):
        return self.obj.DimensionLineColor

    @property
    def dimension_line_weight(self):
        return self.obj.DimensionLineWeight

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def scale_factor(self):
        return self.obj.ScaleFactor

    @property
    def style_name(self):
        return self.obj.StyleName

    @property
    def text_gap(self):
        return self.obj.TextGap

    @property
    def type(self):
        return self.obj.Type

    @property
    def vertical_text_position(self):
        return self.obj.VerticalTextPosition

    def evaluate(self):
        return self.obj.Evaluate()

    # LISTED AS PROPERTY IN ACAD ACTIVEX DOCS BUT IS ACTUALLY A METHOD!
    def coordinate(self, index):
        return self.obj.Coordinate(index)

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbLeaderBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'coordinates'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_array_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
