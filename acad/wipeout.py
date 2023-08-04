from dataclasses import dataclass
from acad.raster_image import AcadRasterImage
from acad.utils import AcadUtil
from sql.models import AcDbWipeoutBase
from pywintypes import com_error


@dataclass
class AcDbWipeout(AcadRasterImage, AcadUtil):
    """
    autoscript generated
    """
    def db_process_in_session_(self, session, space=None):
        # not sure if the case for all wipeout objects, but had some problematic properties in testing
        potential_excludes = ['name', 'image_file']
        excludes = []
        for p in potential_excludes:
            try:
                getattr(self, p)
            except com_error:
                excludes.append(p)

        sql_dct = self._dict_from_shared(AcDbWipeoutBase, excludes=excludes)

        instance = self.db_add_in_session_(model=AcDbWipeoutBase, session=session, space=space, dct=sql_dct)

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
