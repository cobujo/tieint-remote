from dataclasses import dataclass
from acad.collection import AcadCollection


@dataclass
class AcDbBlockTable(AcadCollection):
    """
    All properties and methods should be about the same in "collection" type objects
    except for the add method, which varies by collection type
    """

    def add(self, insertion_point, name: str):
        return self.obj.Add(InsertionPoint=insertion_point, Name=name)
