from dataclasses import dataclass
from acad.object import AcadObject
from acad.true_color import AcadAcCmColor
from acad.utils import AcadUtil
from sql.models import AcadLayerBase


@dataclass
class AcadLayer(AcadObject, AcadUtil):
    """
    autoscript generated
    """

    @property
    def description(self) -> str:
        return self.obj.Description

    @property
    def freeze(self) -> bool:
        return self.obj.Freeze

    @property
    def layer_on(self) -> bool:
        return self.obj.LayerOn

    @property
    def linetype(self) -> str:
        return self.obj.Linetype

    @property
    def lineweight(self) -> int:
        return self.obj.Lineweight

    @property
    def lock(self) -> bool:
        return self.obj.Lock

    @property
    def material(self) -> str:
        return self.obj.Material

    @property
    def name(self) -> str:
        return self.obj.Name

    @property
    def plot_style_name(self) -> str:
        return self.obj.PlotStyleName

    @property
    def plottable(self) -> bool:
        return self.obj.Plottable

    @property
    def true_color(self) -> AcadAcCmColor:
        return AcadAcCmColor(self.obj.TrueColor, _id=self._true_color_id)

    @property
    def _true_color_id(self) -> str:
        return f'{self.handle}_layer_true_color'

    @property
    def used(self) -> bool:
        return self.obj.Used

    @property
    def viewport_default(self) -> bool:
        return self.obj.ViewportDefault

    def _dict_from_shared_nocolors(self, model):
        excludes = ('_true_color_id',)
        return self._dict_from_shared(model=model, excludes=excludes)

    def db_process_in_session_(self, session, space=None, include=('color',)):
        if 'color' in include:
            self.true_color.db_process_in_session_(session=session, space=space)

            self.db_add_in_session_(model=AcadLayerBase, session=session, space=space)

        else:
            sql_dct = self._dict_from_shared_nocolors(model=AcadLayerBase)
            self.db_add_in_session_(model=AcadLayerBase, session=session, space=space, dct=sql_dct)
