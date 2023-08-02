from dataclasses import dataclass
from acad.dim import AcadDimension


@dataclass
class AcDbRotatedDimension(AcadDimension):
    """
    autoscript generated
    """

    @property
    def alt_round_distance(self):
        return self.obj.AltRoundDistance

    @property
    def alt_sub_units_factor(self):
        return self.obj.AltSubUnitsFactor

    @property
    def alt_sub_units_suffix(self):
        return self.obj.AltSubUnitsSuffix

    @property
    def alt_suppress_leading_zeros(self):
        return self.obj.AltSuppressLeadingZeros

    @property
    def alt_suppress_trailing_zeros(self):
        return self.obj.AltSuppressTrailingZeros

    @property
    def alt_suppress_zero_feet(self):
        return self.obj.AltSuppressZeroFeet

    @property
    def alt_suppress_zero_inches(self):
        return self.obj.AltSuppressZeroInches

    @property
    def alt_text_prefix(self):
        return self.obj.AltTextPrefix

    @property
    def alt_text_suffix(self):
        return self.obj.AltTextSuffix

    @property
    def alt_tolerance_precision(self):
        return self.obj.AltTolerancePrecision

    @property
    def alt_tolerance_suppress_leading_zeros(self):
        return self.obj.AltToleranceSuppressLeadingZeros

    @property
    def alt_tolerance_suppress_trailing_zeros(self):
        return self.obj.AltToleranceSuppressTrailingZeros

    @property
    def alt_tolerance_suppress_zero_feet(self):
        return self.obj.AltToleranceSuppressZeroFeet

    @property
    def alt_tolerance_suppress_zero_inches(self):
        return self.obj.AltToleranceSuppressZeroInches

    @property
    def alt_units(self):
        return self.obj.AltUnits

    @property
    def alt_units_format(self):
        return self.obj.AltUnitsFormat

    @property
    def alt_units_precision(self):
        return self.obj.AltUnitsPrecision

    @property
    def alt_units_scale(self):
        return self.obj.AltUnitsScale

    @property
    def arrowhead1_block(self):
        return self.obj.Arrowhead1Block

    @property
    def arrowhead1_type(self):
        return self.obj.Arrowhead1Type

    @property
    def arrowhead2_block(self):
        return self.obj.Arrowhead2Block

    @property
    def arrowhead2_type(self):
        return self.obj.Arrowhead2Type

    @property
    def arrowhead_size(self):
        return self.obj.ArrowheadSize

    @property
    def dim_constr_desc(self):
        return self.obj.DimConstrDesc

    @property
    def dim_constr_expression(self):
        return self.obj.DimConstrExpression

    @property
    def dim_constr_form(self):
        return self.obj.DimConstrForm

    @property
    def dim_constr_name(self):
        return self.obj.DimConstrName

    @property
    def dim_constr_reference(self):
        return self.obj.DimConstrReference

    @property
    def dim_constr_value(self):
        return self.obj.DimConstrValue

    @property
    def dimension_line_color(self):
        return self.obj.DimensionLineColor

    @property
    def dimension_line_extend(self):
        return self.obj.DimensionLineExtend

    @property
    def dimension_linetype(self):
        return self.obj.DimensionLinetype

    @property
    def dimension_line_weight(self):
        return self.obj.DimensionLineWeight

    @property
    def dim_line1_suppress(self):
        return self.obj.DimLine1Suppress

    @property
    def dim_line2_suppress(self):
        return self.obj.DimLine2Suppress

    @property
    def dim_line_inside(self):
        return self.obj.DimLineInside

    @property
    def extension_line_color(self):
        return self.obj.ExtensionLineColor

    @property
    def extension_line_extend(self):
        return self.obj.ExtensionLineExtend

    @property
    def extension_line_offset(self):
        return self.obj.ExtensionLineOffset

    @property
    def extension_line_weight(self):
        return self.obj.ExtensionLineWeight

    @property
    def ext_line1_linetype(self):
        return self.obj.ExtLine1Linetype

    @property
    def ext_line1_suppress(self):
        return self.obj.ExtLine1Suppress

    @property
    def ext_line2_linetype(self):
        return self.obj.ExtLine2Linetype

    @property
    def ext_line2_suppress(self):
        return self.obj.ExtLine2Suppress

    @property
    def ext_line_fixed_len(self):
        return self.obj.ExtLineFixedLen

    @property
    def ext_line_fixed_len_suppress(self):
        return self.obj.ExtLineFixedLenSuppress

    @property
    def fit(self):
        return self.obj.Fit

    @property
    def force_line_inside(self):
        return self.obj.ForceLineInside

    @property
    def fraction_format(self):
        return self.obj.FractionFormat

    @property
    def horizontal_text_position(self):
        return self.obj.HorizontalTextPosition

    @property
    def linear_scale_factor(self):
        return self.obj.LinearScaleFactor

    @property
    def measurement(self):
        return self.obj.Measurement

    @property
    def primary_units_precision(self):
        return self.obj.PrimaryUnitsPrecision

    @property
    def round_distance(self):
        return self.obj.RoundDistance

    @property
    def sub_units_factor(self):
        return self.obj.SubUnitsFactor

    @property
    def sub_units_suffix(self):
        return self.obj.SubUnitsSuffix

    @property
    def suppress_zero_feet(self):
        return self.obj.SuppressZeroFeet

    @property
    def suppress_zero_inches(self):
        return self.obj.SuppressZeroInches

    @property
    def text_inside(self):
        return self.obj.TextInside

    @property
    def text_inside_align(self):
        return self.obj.TextInsideAlign

    @property
    def text_outside_align(self):
        return self.obj.TextOutsideAlign

    @property
    def tolerance_suppress_zero_feet(self):
        return self.obj.ToleranceSuppressZeroFeet

    @property
    def tolerance_suppress_zero_inches(self):
        return self.obj.ToleranceSuppressZeroInches

    @property
    def units_format(self):
        return self.obj.UnitsFormat
