from dataclasses import dataclass
from acad.object import AcadObject


@dataclass
class AcDbPlotSettings(AcadObject):
    """
    autoscript generated
    """

    @property
    def canonical_media_name(self):
        return self.obj.CanonicalMediaName

    @property
    def center_plot(self):
        return self.obj.CenterPlot

    @property
    def config_name(self):
        return self.obj.ConfigName

    @property
    def model_type(self):
        return self.obj.ModelType

    @property
    def name(self):
        return self.obj.Name

    @property
    def paper_units(self):
        return self.obj.PaperUnits

    @property
    def plot_hidden(self):
        return self.obj.PlotHidden

    @property
    def plot_origin(self):
        return self.obj.PlotOrigin

    @property
    def plot_rotation(self):
        return self.obj.PlotRotation

    @property
    def plot_type(self):
        return self.obj.PlotType

    @property
    def plot_viewport_borders(self):
        return self.obj.PlotViewportBorders

    @property
    def plot_viewports_first(self):
        return self.obj.PlotViewportsFirst

    @property
    def plot_with_lineweights(self):
        return self.obj.PlotWithLineweights

    @property
    def plot_with_plot_styles(self):
        return self.obj.PlotWithPlotStyles

    @property
    def scale_lineweights(self):
        return self.obj.ScaleLineweights

    @property
    def show_plot_styles(self):
        return self.obj.ShowPlotStyles

    @property
    def standard_scale(self):
        return self.obj.StandardScale

    @property
    def style_sheet(self):
        return self.obj.StyleSheet

    @property
    def use_standard_scale(self):
        return self.obj.UseStandardScale

    @property
    def view_to_plot(self):
        return self.obj.ViewToPlot

    def copy_from(self, p_plot_config):
        return self.obj.CopyFrom(pPlotConfig=p_plot_config)

    def get_canonical_media_names(self):
        return self.obj.GetCanonicalMediaNames()

    def get_custom_scale(self, numerator, denominator):
        return self.obj.GetCustomScale(Numerator=numerator, Denominator=denominator)

    def get_locale_media_name(self, name):
        return self.obj.GetLocaleMediaName(Name=name)

    def get_paper_margins(self, lower_left, upper_right):
        return self.obj.GetPaperMargins(LowerLeft=lower_left, UpperRight=upper_right)

    def get_paper_size(self, width, height):
        return self.obj.GetPaperSize(Width=width, Height=height)

    def get_plot_device_names(self):
        return self.obj.GetPlotDeviceNames()

    def get_plot_style_table_names(self):
        return self.obj.GetPlotStyleTableNames()

    def get_window_to_plot(self, lower_left, upper_right):
        return self.obj.GetWindowToPlot(LowerLeft=lower_left, UpperRight=upper_right)

    def refresh_plot_device_info(self):
        return self.obj.RefreshPlotDeviceInfo()

    def set_custom_scale(self, numerator, denominator):
        return self.obj.SetCustomScale(Numerator=numerator, Denominator=denominator)

    def set_window_to_plot(self, lower_left, upper_right):
        return self.obj.SetWindowToPlot(LowerLeft=lower_left, UpperRight=upper_right)
