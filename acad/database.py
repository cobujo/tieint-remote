from dataclasses import dataclass, field
import win32com.client as client
from acad.summary_info import AcadSummaryInfo
from acad.layer import AcadLayer
from acad.layers import AcDbLayerTable
from acad.block import AcDbBlockTableRecord
from acad.blocks import AcDbBlockTable
from acad.layout import AcDbLayout
from acad.layouts import AcadLayouts
from acad.paperspace import AcadPaperSpace
from acad.modelspace import AcadModelSpace
from typing import Optional
import warnings
from acad.comwrapper import ComWrapper


@dataclass
class AcadDatabase(object):
    """
    autoscript generated
    """
    com_obj: client.CDispatch
    obj: ComWrapper = field(init=False)
    _handle_static: Optional[str] = None

    def __post_init__(self):
        self.obj = ComWrapper(self.com_obj)

    @property
    def blocks(self):
        return AcDbBlockTable(self.obj.Blocks)

    @property
    def blocks_list_(self):
        return [AcDbBlockTableRecord(b) for b in self.obj.Blocks]

    @property
    def dictionaries(self):
        return self.obj.Dictionaries

    @property
    def dim_styles(self):
        return self.obj.DimStyles

    @property
    def elevation_model_space(self):
        return self.obj.ElevationModelSpace

    @property
    def elevation_paper_space(self):
        return self.obj.ElevationPaperSpace

    @property
    def groups(self):
        return self.obj.Groups

    # sometimes we require the collection object, rather than a list of the objects it containts
    # i.e. for adding to the collection; in these cases make a separate _list_ property
    @property
    def layers(self):
        return AcDbLayerTable(self.obj.Layers)

    @property
    def layers_list_(self) -> list[AcadLayer]:
        return [AcadLayer(o) for o in self.obj.Layers]

    @property
    def layouts_list_(self):
        return [AcDbLayout(l) for l in self.obj.Layouts]

    @property
    def layouts(self):
        return AcadLayouts(self.obj.Layouts)

    @property
    def limits(self):
        return self.obj.Limits

    @property
    def linetypes(self):
        return self.obj.Linetypes

    @property
    def material(self):
        warnings.warn('material raising AttributeError: Open.Material')
        return

    @property
    def model_space(self):
        return AcadModelSpace(self.obj.ModelSpace)

    @property
    def paper_space(self):
        return AcadPaperSpace(self.obj.PaperSpace)

    @property
    def plot_configurations(self):
        return self.obj.PlotConfigurations

    @property
    def preferences(self):
        return self.obj.Preferences

    @property
    def registered_applications(self):
        return self.obj.RegisteredApplications

    @property
    def section_manager(self):
        return self.obj.SectionManager

    @property
    def summary_info(self) -> AcadSummaryInfo:
        return AcadSummaryInfo(self.obj.SummaryInfo)

    @property
    def text_styles(self):
        return self.obj.TextStyles

    @property
    def user_coordinate_systems(self):
        return self.obj.UserCoordinateSystems

    @property
    def viewports(self):
        return self.obj.Viewports

    @property
    def views(self):
        return self.obj.Views

    def copy_objects(self, objects, owner=None, id_pairs=None):
        return self.obj.CopyObjects(Objects=objects, Owner=owner, IdPairs=id_pairs)

    def handle_to_object(self, handle):
        return self.obj.HandleToObject(Handle=handle)

    def object_id_to_object(self, object_id):
        return self.obj.ObjectIdToObject(ObjectID=object_id)
