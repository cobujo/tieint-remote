from dataclasses import dataclass
from acad.object import AcadObject
from acad.true_color import AcadAcCmColor


@dataclass
class AcadEntity(AcadObject):
    """
    autoscript generated
    """

    @property
    def entity_transparency(self) -> str:
        return self.obj.EntityTransparency

    @property
    def hyperlinks(self):
        return self.obj.Hyperlinks

    @property
    def layer(self) -> str:
        return self.obj.Layer

    @property
    def linetype(self):
        return self.obj.Linetype

    @property
    def linetype_scale(self):
        return self.obj.LinetypeScale

    @property
    def lineweight(self):
        return self.obj.Lineweight

    @property
    def material(self):
        return self.obj.Material

    @property
    def plot_style_name(self):
        return self.obj.PlotStyleName

    # as of now, not storing this color in table for all entities
    @property
    def true_color(self) -> AcadAcCmColor:
        return AcadAcCmColor(self.obj.TrueColor)

    @property
    def visible(self):
        return self.obj.Visible

    def array_polar(self, number_of_objects, angle_to_fill, center_point):
        return self.obj.ArrayPolar(NumberOfObjects=number_of_objects, AngleToFill=angle_to_fill, CenterPoint=center_point)

    def array_rectangular(self, number_of_rows, number_of_columns, number_of_levels, dist_between_rows, dist_between_cols, dist_between_levels):
        return self.obj.ArrayRectangular(NumberOfRows=number_of_rows, NumberOfColumns=number_of_columns, NumberOfLevels=number_of_levels, DistBetweenRows=dist_between_rows, DistBetweenCols=dist_between_cols, DistBetweenLevels=dist_between_levels)

    def copy(self):
        return self.obj.Copy()

    def get_bounding_box(self, min_point, max_point):
        return self.obj.GetBoundingBox(MinPoint=min_point, MaxPoint=max_point)

    def highlight(self, highlight_flag):
        return self.obj.Highlight(HighlightFlag=highlight_flag)

    def intersect_with(self, intersect_object, option):
        return self.obj.IntersectWith(IntersectObject=intersect_object, option=option)

    def mirror(self, point1, point2):
        return self.obj.Mirror(Point1=point1, Point2=point2)

    def mirror3_d(self, point1, point2, point3):
        return self.obj.Mirror3D(Point1=point1, Point2=point2, point3=point3)

    def move(self, from_point, to_point):
        return self.obj.Move(FromPoint=from_point, ToPoint=to_point)

    def rotate(self, base_point, rotation_angle):
        return self.obj.Rotate(BasePoint=base_point, RotationAngle=rotation_angle)

    def rotate3_d(self, point1, point2, rotation_angle):
        return self.obj.Rotate3D(Point1=point1, Point2=point2, RotationAngle=rotation_angle)

    def scale_entity(self, base_point, scale_factor):
        return self.obj.ScaleEntity(BasePoint=base_point, ScaleFactor=scale_factor)

    def transform_by(self, transformation_matrix):
        return self.obj.TransformBy(TransformationMatrix=transformation_matrix)

    def update(self):
        return self.obj.Update()
