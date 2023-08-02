from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.utils import AcadUtil
from sql.models import AcDbPointBase
from mylogger import logger


@dataclass
class AcDbPoint(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def coordinates(self):
        return self.obj.Coordinates

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def thickness(self):
        return self.obj.Thickness

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        instance = self.db_add_in_session_(model=AcDbPointBase, session=session, space=space)
        if not instance:
            return

        coord_attr = 'coordinates'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')
