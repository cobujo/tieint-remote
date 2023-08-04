from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.true_color import AcadAcCmColor
from acad.utils import AcadUtil
from sql.models import AcDbHatchBase
from pywintypes import com_error
from mylogger import logger


@dataclass
class AcDbHatch(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def area(self):
        return self.obj.Area

    @property
    def associative_hatch(self):
        return self.obj.AssociativeHatch

    @property
    def background_color(self) -> AcadAcCmColor:
        return AcadAcCmColor(self.obj.BackgroundColor, _id=self._background_color_id)

    @property
    def _background_color_id(self) -> str:
        return f'{self.handle}_hatch_background_color'

    @property
    def elevation(self):
        return self.obj.Elevation

    @property
    def gradient_angle(self):
        return self.obj.GradientAngle

    @property
    def gradient_centered(self):
        return self.obj.GradientCentered

    @property
    def gradient_color1(self) -> AcadAcCmColor:
        return AcadAcCmColor(self.obj.GradientColor1, _id=self._gradient_color1_id)

    @property
    def _gradient_color1_id(self) -> str:
        return f'{self.handle}_hatch_gradient_color1'

    @property
    def gradient_color2(self) -> AcadAcCmColor:
        return AcadAcCmColor(self.obj.GradientColor2, _id=self._gradient_color2_id)

    @property
    def _gradient_color2_id(self) -> str:
        return f'{self.handle}_hatch_gradient_color2'

    @property
    def gradient_name(self):
        return self.obj.GradientName

    @property
    def hatch_object_type(self):
        return self.obj.HatchObjectType

    @property
    def hatch_style(self):
        return self.obj.HatchStyle

    @property
    def iso_pen_width(self):
        return self.obj.ISOPenWidth

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def number_of_loops(self):
        return self.obj.NumberOfLoops

    @property
    def origin(self):
        return self.obj.Origin

    @property
    def pattern_angle(self):
        return self.obj.PatternAngle

    @property
    def pattern_double(self):
        return self.obj.PatternDouble

    @property
    def pattern_name(self):
        return self.obj.PatternName

    @property
    def pattern_scale(self):
        return self.obj.PatternScale

    @property
    def pattern_space(self):
        return self.obj.PatternSpace

    @property
    def pattern_type(self):
        return self.obj.PatternType

    def append_inner_loop(self, object_array):
        return self.obj.AppendInnerLoop(ObjectArray=object_array)

    def append_outer_loop(self, object_array):
        return self.obj.AppendOuterLoop(ObjectArray=object_array)

    def evaluate(self):
        return self.obj.Evaluate()

    def get_loop_at(self, index, object_array):
        return self.obj.GetLoopAt(Index=index, ObjectArray=object_array)

    def insert_loop_at(self, index, loop_type, object_array):
        return self.obj.InsertLoopAt(Index=index, LoopType=loop_type, ObjectArray=object_array)

    def set_pattern(self, pattern_type, pattern_name):
        return self.obj.SetPattern(PatternType=pattern_type, PatternName=pattern_name)

    def _dict_from_shared_nocolors(self, model):
        excludes = ('_background_color_id', '_gradient_color1_id', '_gradient_color2_id')
        return self._dict_from_shared(model=model, excludes=excludes)

    def db_process_in_session_(self, session, space=None, include=('color',)):
        # *** can not find anything in docs that gives coordinates for hatch object! ***
        # as of now we have no way to add this to the object coordinates table
        kws = dict(model=AcDbHatchBase, session=session, space=space)
        if 'color' in include:
            colors = ['background_color', 'gradient_color1', 'gradient_color2']
            for color_str in colors:
                try:
                    color = getattr(self, color_str)
                    color.db_process_in_session_(session=session, space=space)
                except com_error as e:
                    logger.warning(f'unable to create AcCmColor obj from {color_str} and store in db, likely because required constant is not set')

        else:
            sql_dct = self._dict_from_shared_nocolors(AcDbHatchBase)
            kws['dct'] = sql_dct

        instance = self.db_add_in_session_(**kws)
        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
