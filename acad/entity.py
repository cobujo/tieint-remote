from dataclasses import dataclass
from acad.object import AcadObject
from acad.true_color import AcadAcCmColor
from typing import Optional
from sql.models import ObjectBoundingBox
from acad import Spaces
from mylogger import logger
from sql.helpers import db_add_or_merge


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

    def get_bounding_box(self) -> tuple:
        # UPDATE: documentation is incorrect; input args are required but don't have to be "real", method will return tuple for min and max point regardless of input
        return self.obj.GetBoundingBox(MinPoint=None, MaxPoint=None)

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

    def db_process_bounding_box_in_session_(self, session, space: Optional[str] = None, obj_instance=None):
        """
        modeled after db_process[coordinates]_in_session_ methods under acad.object
        note this in the entity class since AcadEntity has the GetBoundingBox method
        :param session:
            expecting to run within a session scope
        :param space: str
            paper or model
        :param obj_instance:
            the sql instance, for establishing the relationship
        :return:
        """
        try:
            bbox = self.get_bounding_box()
        except AttributeError:
            raise AttributeError(f'expecting {self.__class__.__name__} to be a child of AcadEntity, however does not have the GetBoundingBox method!')

        # only getting x and y values (not expecting to ever have use for z)
        min_point, max_point = bbox[0], bbox[1]
        min_x, min_y = min_point[0], min_point[1]
        max_x, max_y = max_point[0], max_point[1]

        obb = ObjectBoundingBox(
            document_name=self.document.name,
            handle_id=self._handle_static,
            class_name=self.__class__.__name__,
            x_min=min_x,
            x_max=max_x,
            y_min=min_y,
            y_max=max_y
        )

        if space in Spaces:
            obb.space = space
        else:
            logger.warning(f'Expecting space to be one of: {Spaces}, instead received {space}')
            logger.warning(f'expecting {self.__class__.__name__} to be a child of AcadEntity and exist in a space')

        if obj_instance:
            obb.object = obj_instance

        db_add_or_merge(instance=obb, session_scope=session)
