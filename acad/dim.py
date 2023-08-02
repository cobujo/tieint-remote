from dataclasses import dataclass
from acad.entity import AcadEntity


@dataclass
class AcadDimension(AcadEntity):
    """
    autoscript generated

    Created solely to follow ActiveX object hierarchy
    Not intending to use this object directly
    """

    @property
    def decimal_separator(self):
        return self.obj.DecimalSeparator

    @property
    def dim_txt_direction(self):
        return self.obj.DimTxtDirection

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def rotation(self):
        return self.obj.Rotation

    @property
    def scale_factor(self):
        return self.obj.ScaleFactor

    @property
    def style_name(self):
        return self.obj.StyleName

    @property
    def suppress_leading_zeros(self):
        return self.obj.SuppressLeadingZeros

    @property
    def suppress_trailing_zeros(self):
        return self.obj.SuppressTrailingZeros

    @property
    def text_color(self):
        return self.obj.TextColor

    @property
    def text_fill(self):
        return self.obj.TextFill

    @property
    def text_fill_color(self):
        return self.obj.TextFillColor

    @property
    def text_gap(self):
        return self.obj.TextGap

    @property
    def text_height(self):
        return self.obj.TextHeight

    @property
    def text_movement(self):
        return self.obj.TextMovement

    @property
    def text_override(self):
        return self.obj.TextOverride

    @property
    def text_position(self):
        return self.obj.TextPosition

    @property
    def text_prefix(self):
        return self.obj.TextPrefix

    @property
    def text_rotation(self):
        return self.obj.TextRotation

    @property
    def text_style(self):
        return self.obj.TextStyle

    @property
    def text_suffix(self):
        return self.obj.TextSuffix

    @property
    def tolerance_display(self):
        return self.obj.ToleranceDisplay

    @property
    def tolerance_height_scale(self):
        return self.obj.ToleranceHeightScale

    @property
    def tolerance_justification(self):
        return self.obj.ToleranceJustification

    @property
    def tolerance_lower_limit(self):
        return self.obj.ToleranceLowerLimit

    @property
    def tolerance_precision(self):
        return self.obj.TolerancePrecision

    @property
    def tolerance_suppress_leading_zeros(self):
        return self.obj.ToleranceSuppressLeadingZeros

    @property
    def tolerance_suppress_trailing_zeros(self):
        return self.obj.ToleranceSuppressTrailingZeros

    @property
    def tolerance_upper_limit(self):
        return self.obj.ToleranceUpperLimit

    @property
    def vertical_text_position(self):
        return self.obj.VerticalTextPosition
