from dataclasses import dataclass
from acad.block import AcDbBlockTableRecord


@dataclass
class AcadPaperSpace(AcDbBlockTableRecord):
    """
    autoscript generated
    """

    def add_p_viewport(self, center, width, height):
        return self.obj.AddPViewport(Center=center, Width=width, Height=height)
