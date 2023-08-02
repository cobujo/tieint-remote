from dataclasses import dataclass
from acad.entity import AcadEntity


@dataclass
class AcadTable(AcadEntity):

    @property
    def allow_manual_heights(self):
        return self.obj.AllowManualHeights

    @property
    def allow_manual_positions(self):
        return self.obj.AllowManualPositions

    @property
    def breaks_enabled(self):
        return self.obj.BreaksEnabled

    @property
    def columns(self):
        return self.obj.Columns

    @property
    def column_width(self):
        return self.obj.ColumnWidth

    @property
    def direction(self):
        return self.obj.Direction

    @property
    def enable_break(self):
        return self.obj.EnableBreak

    @property
    def flow_direction(self):
        return self.obj.FlowDirection

    @property
    def has_sub_selection(self):
        return self.obj.HasSubSelection

    @property
    def header_suppressed(self):
        return self.obj.HeaderSuppressed

    @property
    def height(self):
        return self.obj.Height

    @property
    def horz_cell_margin(self):
        return self.obj.HorzCellMargin

    @property
    def insertion_point(self):
        return self.obj.InsertionPoint

    @property
    def minimum_table_height(self):
        return self.obj.MinimumTableHeight

    @property
    def minimum_table_width(self):
        return self.obj.MinimumTableWidth

    @property
    def regenerate_table_suppressed(self):
        return self.obj.RegenerateTableSuppressed

    @property
    def repeat_bottom_labels(self):
        return self.obj.RepeatBottomLabels

    @property
    def repeat_top_labels(self):
        return self.obj.RepeatTopLabels

    @property
    def row_height(self):
        return self.obj.RowHeight

    @property
    def rows(self):
        return self.obj.Rows

    @property
    def style_name(self):
        return self.obj.StyleName

    @property
    def table_break_flow_direction(self):
        return self.obj.TableBreakFlowDirection

    @property
    def table_break_height(self):
        return self.obj.TableBreakHeight

    @property
    def table_style_overrides(self):
        return self.obj.TableStyleOverrides

    @property
    def title_suppressed(self):
        return self.obj.TitleSuppressed

    @property
    def vert_cell_margin(self):
        return self.obj.VertCellMargin

    @property
    def width(self):
        return self.obj.Width
