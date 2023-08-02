import warnings
from dataclasses import dataclass
from acad import vba_array
from acad.object import AcadObject
from acad.utils import AcadUtil
from sql.models import AcDbViewportBase
from acad.line import AcDbLine
from mylogger import logger
from typing import Optional


@dataclass
class AcDbViewport(AcadObject, AcadUtil):
    """
    autoscript generated
    """
    # below attributes NOT auto generated, will be set using other methods
    x_min_ms_: Optional[float] = None
    x_max_ms_: Optional[float] = None
    y_min_ms_: Optional[float] = None
    y_max_ms_: Optional[float] = None
    scale_: Optional[float] = None

    @property
    def arc_smoothness(self):
        return self.obj.ArcSmoothness

    @property
    def center(self):
        return self.obj.Center

    @property
    def direction(self):
        return self.obj.Direction

    @property
    def grid_on(self):
        return self.obj.GridOn

    @property
    def height(self):
        return self.obj.Height

    @property
    def lower_left_corner(self):
        return self.obj.LowerLeftCorner

    @property
    def name(self):
        return self.obj.Name

    @property
    def ortho_on(self):
        return self.obj.OrthoOn

    @property
    def snap_base_point(self):
        return self.obj.SnapBasePoint

    @property
    def snap_on(self):
        return self.obj.SnapOn

    @property
    def snap_rotation_angle(self):
        return self.obj.SnapRotationAngle

    @property
    def target(self):
        return self.obj.Target

    @property
    def ucs_icon_at_origin(self):
        return self.obj.UCSIconAtOrigin

    @property
    def ucs_icon_on(self):
        return self.obj.UCSIconOn

    @property
    def upper_right_corner(self):
        return self.obj.UpperRightCorner

    @property
    def width(self):
        return self.obj.Width

    def get_grid_spacing(self, x_spacing, y_spacing):
        return self.obj.GetGridSpacing(XSpacing=x_spacing, YSpacing=y_spacing)

    def get_snap_spacing(self, x_spacing, y_spacing):
        return self.obj.GetSnapSpacing(XSpacing=x_spacing, YSpacing=y_spacing)

    def set_grid_spacing(self, x_spacing, y_spacing):
        return self.obj.SetGridSpacing(XSpacing=x_spacing, YSpacing=y_spacing)

    def set_snap_spacing(self, x_spacing, y_spacing):
        return self.obj.SetSnapSpacing(XSpacing=x_spacing, YSpacing=y_spacing)

    @staticmethod
    def set_view():
        warnings.warn('set_view raising AttributeError: <unknown>.SetView')

    @staticmethod
    def split():
        warnings.warn('split raising AttributeError: <unknown>.Split')

    def is_valid_ms_viewport_(self):
        """
        TODO: Mild -> improve this, is there a better way to identify "non-valid" viports that aren't displayed?
        There appears to be at least 1 viewport in drawings with viewports that is not displayed; the only way to
        distinguish this vp is that the size doesn't make sense with the layout (it's somehow larger than the extents
        of the layout).  Until we get a better method we'll identify this vp by it's size
        :return: bool
        """
        extmin, extmax = self.document.get_ps_layout_extents_()
        x_range = extmax[0] - extmin[0]
        y_range = extmax[1] - extmin[1]

        if all([self.width < x_range, self.height < y_range]):
            return True

        return False

    def create_test_line_(self) -> Optional[AcDbLine]:
        # create test line in paperspace that will get moved to modelspace to determine scale & location
        p1 = vba_array(self.center)
        # this is an arbitrary amount, as long as the value is completely within the viewport
        x_offset = self.width / 4
        p2_l = list(self.center)
        p2_l[0] = p2_l[0] + x_offset
        p2 = vba_array(p2_l)
        try:
            return self.document.paper_space.add_line(start_point=p1, end_point=p2)
        except Exception as e:
            logger.error(f'error trying to create test line: {e}')
            return

    def set_modelspace_coordinates_(self):
        if not self.is_valid_ms_viewport_():
            return

        line = self.create_test_line_()
        if not line:
            logger.error(f'unable to create test line and determine ms coords for viewport, handle: {self.handle}')
            return

        p1_ps = line.start_point
        p2_ps = line.end_point
        cmd = f'_SELECT\n(HANDENT "{line.handle}")\n\n'
        self.document.send_command(cmd)
        cmd = 'CHSPACE\n\n'
        self.document.send_command(cmd)

        p1_ms = line.start_point
        p2_ms = line.end_point

        if any([p1_ps == p1_ms, p2_ps == p2_ms]):
            logger.error(f'created line was not successfully moved using CHSPACE, handle: {line.handle}')
            return

        x_delta_ps = p2_ps[0] - p1_ps[0]
        x_delta_ms = p2_ms[0] - p1_ms[0]
        self.scale_ = x_delta_ms / x_delta_ps

        width_ms = self.width * self.scale_
        height_ms = self.height * self.scale_

        self.x_min_ms_ = p1_ms[0] - (width_ms / 2)
        self.x_max_ms_ = p1_ms[0] + (width_ms / 2)
        self.y_min_ms_ = p1_ms[1] - (height_ms / 2)
        self.y_max_ms_ = p1_ms[1] + (height_ms / 2)

        # shouldn't matter since we're not saving changes, but good practive to delete line
        line.delete()

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbViewportBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'center'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=coord_attr,
                                                                       space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')
