from dataclasses import dataclass
from acad.object import AcadObject


@dataclass
class AcadDictionary(AcadObject):

    @property
    def count(self) -> int:
        return self.obj.Count

    @property
    def name(self) -> str:
        return self.obj.Name

    def add_object(self, keyword: str, object_name: str):
        return AcadObject(self.obj.AddObject(Keyword=keyword, ObjectName=object_name))

    def add_x_record(self, keyword: str):
        return self.obj.AddXRecord(Keyword=keyword)

    def get_name(self, obj):
        return self.obj.GetName(Object=obj)

    def get_object(self, name):
        return self.obj.GetObject(Name=name)

    def item(self, index):
        return self.obj.Item(Index=index)

    def remove(self, name):
        return self.obj.Remove(Name=name)

    def rename(self, old_name, new_name):
        return self.obj.Rename(OldName=old_name, NewName=new_name)

    def replace(self, old_name, p_obj):
        return self.obj.Replace(OldName=old_name, pObj=p_obj)
