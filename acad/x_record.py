from dataclasses import dataclass
from acad.object import AcadObject


@dataclass
class AcadXRecord(AcadObject):

    @property
    def name(self) -> str:
        return self.obj.Name

    @property
    def translate_ids(self) -> bool:
        return self.obj.TranslateIDs

    def get_x_record_data(self, x_record_data_type, x_record_data_value):
        return self.obj.GetXRecordData(XRecordDataType=x_record_data_type, XRecordDataValue=x_record_data_value)

    def set_x_record_data(self, x_record_data_type, x_record_data):
        return self.obj.SetXRecordData(XRecordDataType=x_record_data_type, XRecordData=x_record_data)
