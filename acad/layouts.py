from dataclasses import dataclass
from acad.collection import AcadCollection


@dataclass
class AcadLayouts(AcadCollection):
    """
    ObjectName for Layouts is AcDbDictionary, however this is a different object from a dictionary
    as defined in the docs...not sure how this happens.
    """
    def delete(self):
        raise NotImplementedError('This method is not available to AcadLayouts')
