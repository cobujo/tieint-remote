from dataclasses import dataclass
from acad.collection import AcadCollection


@dataclass
class AcDbLayerTable(AcadCollection):
    """
    All properties and methods should be about the same in "collection" type objects
    except for the add method, which varies by collection type
    """

    def generate_usage_data(self):
        return self.obj.GenerateUsageData()
