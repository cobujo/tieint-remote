from dataclasses import dataclass
from acad.plot_configuration import AcDbPlotSettings


@dataclass
class AcDbLayout(AcDbPlotSettings):
    """
    autoscript generated
    """

    @property
    def block(self):
        return self.obj.Block

    @property
    def tab_order(self):
        return self.obj.TabOrder
