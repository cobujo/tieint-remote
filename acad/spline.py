from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbSplineBase
from mylogger import logger


@dataclass
class AcDbSpline(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def area(self):
        return self.obj.Area

    @property
    def closed(self):
        return self.obj.Closed

    @property
    def closed2(self):
        return self.obj.Closed2

    @property
    def control_points(self):
        return self.obj.ControlPoints

    @property
    def degree(self):
        return self.obj.Degree

    @property
    def degree2(self):
        return self.obj.Degree2

    @property
    def end_tangent(self):
        return self.obj.EndTangent

    @property
    def fit_points(self):
        return self.obj.FitPoints

    @property
    def fit_tolerance(self):
        return self.obj.FitTolerance

    @property
    def is_periodic(self):
        return self.obj.IsPeriodic

    @property
    def is_planar(self):
        return self.obj.IsPlanar

    @property
    def is_rational(self):
        return self.obj.IsRational

    @property
    def knot_parameterization(self):
        return self.obj.KnotParameterization

    @property
    def knots(self):
        return self.obj.Knots

    @property
    def number_of_control_points(self):
        return self.obj.NumberOfControlPoints

    @property
    def number_of_fit_points(self):
        return self.obj.NumberOfFitPoints

    @property
    def spline_frame(self):
        return self.obj.SplineFrame

    @property
    def spline_method(self):
        return self.obj.SplineMethod

    @property
    def start_tangent(self):
        return self.obj.StartTangent

    @property
    def weights(self):
        return self.obj.Weights

    def add_fit_point(self, index, fit_point):
        return self.obj.AddFitPoint(Index=index, fitPoint=fit_point)

    def delete_fit_point(self, index):
        return self.obj.DeleteFitPoint(Index=index)

    def elevate_order(self, order):
        return self.obj.ElevateOrder(Order=order)

    def get_control_point(self, index):
        return self.obj.GetControlPoint(Index=index)

    def get_fit_point(self, index):
        return self.obj.GetFitPoint(Index=index)

    def get_weight(self, index):
        return self.obj.GetWeight(Index=index)

    def offset(self, distance):
        return self.obj.Offset(Distance=distance)

    def purge_fit_data(self):
        return self.obj.PurgeFitData()

    def reverse(self):
        return self.obj.Reverse()

    def set_control_point(self, index, control_point):
        return self.obj.SetControlPoint(Index=index, controlPoint=control_point)

    def set_fit_point(self, index, fit_point):
        return self.obj.SetFitPoint(Index=index, fitPoint=fit_point)

    def set_weight(self, index, weight):
        return self.obj.SetWeight(Index=index, weight=weight)

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbSplineBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'fit_points'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_array_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
