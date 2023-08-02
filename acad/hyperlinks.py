from dataclasses import dataclass, field
import win32com.client as client
from typing import Optional, Union
from acad.comwrapper import ComWrapper


@dataclass
class AcadHyperlinks(object):
    com_obj: client.CDispatch
    obj: ComWrapper = field(init=False)

    def __post_init__(self):
        self.obj = ComWrapper(self.com_obj)

    @property
    def application(self):
        return self.obj.Application

    @property
    def count(self) -> int:
        return self.obj.Count

    def add(self, name: str, description: Optional, named_location: Optional):
        return self.obj.Add(Name=name, Description=description, NamedLocation=named_location)

    def item(self, index: Union[str, int]):
        return self.obj.Item(Index=index)
