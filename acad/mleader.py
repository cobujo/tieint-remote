from dataclasses import dataclass, field
from acad.entity import AcadEntity
from acad.true_color import AcadAcCmColor
from acad.utils import AcadUtil
from sql.models import AcDbMLeaderBase
import warnings
from mylogger import logger


@dataclass
class AcDbMLeader(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

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
    def block_connection_type(self):
        return self.obj.BlockConnectionType

    @property
    def block_scale(self):
        return self.obj.BlockScale

    @property
    def content_block_name(self):
        return self.obj.ContentBlockName

    @property
    def content_block_type(self):
        return self.obj.ContentBlockType

    @property
    def content_type(self) -> int:
        return self.obj.ContentType

    @property
    def dog_legged(self) -> bool:
        return self.obj.DogLegged

    @property
    def dogleg_length(self) -> float:
        return self.obj.DoglegLength

    @property
    def landing_gap(self) -> float:
        return self.obj.LandingGap

    @property
    def leader_count(self) -> int:
        return self.obj.LeaderCount

    @property
    def leader_line_color(self) -> AcadAcCmColor:
        return AcadAcCmColor(com_obj=self.obj.LeaderLineColor, _id=self._leader_line_color_id)

    @property
    def _leader_line_color_id(self) -> str:
        return f'{self.handle}_mleader_line_color'

    @property
    def leader_line_type(self):
        return self.obj.LeaderLineType

    @property
    def leader_line_weight(self):
        return self.obj.LeaderLineWeight

    @property
    def leader_type(self):
        return self.obj.LeaderType

    # listed as prop in docs, but links to Name property for other objects?
    # @property
    # def normal(self):
    #     return self.obj.Normal

    @property
    def scale_factor(self):
        return self.obj.ScaleFactor

    @property
    def style_name(self):
        return self.obj.StyleName

    @property
    def text_attachment_direction(self):
        return self.obj.TextAttachmentDirection

    @property
    def text_background_fill(self):
        return self.obj.TextBackgroundFill

    @property
    def text_bottom_attachment_type(self):
        return self.obj.TextBottomAttachmentType

    @property
    def text_direction(self):
        return self.obj.TextDirection

    @property
    def text_frame_display(self):
        return self.obj.TextFrameDisplay

    @property
    def text_height(self):
        return self.obj.TextHeight

    @property
    def text_justify(self):
        return self.obj.TextJustify

    @property
    def text_left_attachment_type(self):
        return self.obj.TextLeftAttachmentType

    @property
    def text_line_spacing_distance(self):
        return self.obj.TextLineSpacingDistance

    @property
    def text_line_spacing_factor(self):
        return self.obj.TextLineSpacingFactor

    @property
    def text_line_spacing_style(self):
        return self.obj.TextLineSpacingStyle

    @property
    def text_right_attachment_type(self):
        return self.obj.TextRightAttachmentType

    @property
    def text_rotation(self):
        return self.obj.TextRotation

    @property
    def text_string(self):
        return self.obj.TextString

    @property
    def text_style_name(self):
        return self.obj.TextStyleName

    @property
    def text_top_attachment_type(self):
        return self.obj.TextTopAttachmentType

    @property
    def text_width(self):
        return self.obj.TextWidth

    @property
    def type_(self):
        return self.obj.Type

    def add_leader(self):
        return self.obj.AddLeader()

    def add_leader_line(self, leader_index, point_array):
        return self.obj.AddLeaderLine(leaderIndex=leader_index, pointArray=point_array)

    def add_leader_line_ex(self, point_array):
        return self.obj.AddLeaderLineEx(pointArray=point_array)

    @staticmethod
    def evaluate(self):
        warnings.warn('evaluate raising AttributeError: <unknown>.Evaluate')

    def get_block_attribute_value(self, attdef_id):
        return self.obj.GetBlockAttributeValue(attdefId=attdef_id)

    def get_dogleg_direction(self, leader_index):
        return self.obj.GetDoglegDirection(leaderIndex=leader_index)

    def get_leader_index(self, leader_line_index):
        return self.obj.GetLeaderIndex(leaderLineIndex=leader_line_index)

    def get_leader_line_indexes(self, leader_index):
        return self.obj.GetLeaderLineIndexes(leaderIndex=leader_index)

    def get_leader_line_vertices(self, leader_line_index):
        return self.obj.GetLeaderLineVertices(leaderLineIndex=leader_line_index)

    def get_vertex_count(self, leader_line_index):
        return self.obj.GetVertexCount(leaderLineIndex=leader_line_index)

    def remove_leader(self, leader_index):
        return self.obj.RemoveLeader(leaderIndex=leader_index)

    def remove_leader_line(self, leader_line_index):
        return self.obj.RemoveLeaderLine(leaderLineIndex=leader_line_index)

    def set_block_attribute_value(self, attdef_id, value):
        return self.obj.SetBlockAttributeValue(attdefId=attdef_id, Value=value)

    def set_dogleg_direction(self, leader_index, dir_vec):
        return self.obj.SetDoglegDirection(leaderIndex=leader_index, dirVec=dir_vec)

    def set_leader_line_vertices(self, leader_line_index, point_array):
        return self.obj.SetLeaderLineVertices(leaderLineIndex=leader_line_index, pointArray=point_array)

    def db_process_in_session_(self, session, space=None, include=('color',)):
        if not self.valid_handle():
            return

        coord_attr = 'get_leader_line_vertices'
        # process coordinates array for each leader
        leader_count = self.leader_count
        if not leader_count:
            return

        instance = None
        if 'color' in include:
            self.leader_line_color.db_process_in_session_(session=session, space=space)

            instance = self.db_add_in_session_(model=AcDbMLeaderBase, session=session, space=space)

        else:
            # if not adding color to db, remove color id from model
            sql_dct = self._dict_from_shared(AcDbMLeaderBase)
            sql_dct.pop('_leader_line_color_id')
            instance = self.db_add_in_session_(model=AcDbMLeaderBase, session=session, space=space, dct=sql_dct)

        if not instance:
            return

        coord_import = []
        for index in range(leader_count):
            coord_import.append(self.db_process_prop_3d_coordinates_array_in_session_(session=session, attr_name=coord_attr, space=space, args=(index,), obj_instance=instance))

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=coord_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
