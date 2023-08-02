from dataclasses import dataclass
from acad.entity import AcadEntity


@dataclass
class AcDbSolid(AcadEntity):
    """
    autoscript generated
    """

    @property
    def coordinate(self):
        return self.obj.Coordinate

    @property
    def coordinates(self):
        return self.obj.Coordinates

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def thickness(self):
        return self.obj.Thickness
