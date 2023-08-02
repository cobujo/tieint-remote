from dataclasses import dataclass
from acad.object import AcadObject


@dataclass
class AcadCollection(AcadObject):
    """
    autoscript generated

    This is NOT an actual AutoCAD object; created to reduce redundancies, as it appears in the object model
    that all collections (i.e. PlotConfigurations, Blocks, etc.) have the same methods and properties.

    Not intending to add any collections to db, will instead add the objects within the collection to db
    """

    @property
    def count(self) -> int:
        return self.obj.Count

    def add(self, name: str):
        return self.obj.Add(Name=name)

    def item(self, index: int):
        return self.obj.Item(Index=index)
