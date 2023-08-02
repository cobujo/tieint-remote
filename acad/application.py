from dataclasses import dataclass, field
import win32com.client as client
from acad.comwrapper import ComWrapper


@dataclass
class AcadApplication(object):
    """
    autoscript generated
    """
    com_obj: client.CDispatch
    obj: ComWrapper = field(init=False)

    def __post_init__(self):
        self.obj = ComWrapper(self.com_obj)

    @property
    def active_document(self):
        from acad.document import AcadDocument
        return AcadDocument(self.obj.ActiveDocument)

    @property
    def application(self):
        return self.obj.Application

    @property
    def caption(self):
        return self.obj.Caption

    @property
    def documents(self):
        return self.obj.Documents

    @property
    def full_name(self):
        return self.obj.FullName

    @property
    def height(self):
        return self.obj.Height

    @property
    def hwnd(self):
        return self.obj.HWND

    @property
    def locale_id(self):
        return self.obj.LocaleID

    @property
    def menu_bar(self):
        return self.obj.MenuBar

    @property
    def menu_groups(self):
        return self.obj.MenuGroups

    @property
    def name(self):
        return self.obj.Name

    @property
    def path(self):
        return self.obj.Path

    @property
    def preferences(self):
        return self.obj.Preferences

    @property
    def status_id(self):
        return self.obj.StatusID

    @property
    def vbe(self):
        return self.obj.VBE

    @property
    def version(self):
        return self.obj.Version

    @property
    def visible(self):
        return self.obj.Visible

    @property
    def width(self):
        return self.obj.Width

    @property
    def window_left(self):
        return self.obj.WindowLeft

    @property
    def window_state(self):
        return self.obj.WindowState

    @property
    def window_top(self):
        return self.obj.WindowTop

    def eval(self, expression):
        return self.obj.Eval(Expression=expression)

    def get_acad_state(self):
        return self.obj.GetAcadState()

    def get_interface_object(self, prog_id):
        return self.obj.GetInterfaceObject(ProgID=prog_id)

    def list_arx(self):
        return self.obj.ListARX()

    def load_arx(self):
        return self.obj.LoadARX()

    def load_dvb(self, name):
        return self.obj.LoadDVB(Name=name)

    def quit(self):
        return self.obj.Quit()

    def run_macro(self, macro_path):
        return self.obj.RunMacro(MacroPath=macro_path)

    def unload_arx(self):
        return self.obj.UnloadARX()

    def unload_dvb(self, name):
        return self.obj.UnloadDVB(Name=name)

    def update(self):
        return self.obj.Update()

    def zoom_all(self):
        return self.obj.ZoomAll()

    def zoom_center(self, center, magnify):
        return self.obj.ZoomCenter(Center=center, Magnify=magnify)

    def zoom_extents(self):
        return self.obj.ZoomExtents()

    def zoom_pick_window(self):
        return self.obj.ZoomPickWindow()

    def zoom_previous(self):
        return self.obj.ZoomPrevious()

    def zoom_scaled(self, scale, scale_type):
        return self.obj.ZoomScaled(scale=scale, ScaleType=scale_type)

    def zoom_window(self, lower_left, upper_right):
        return self.obj.ZoomWindow(LowerLeft=lower_left, UpperRight=upper_right)
