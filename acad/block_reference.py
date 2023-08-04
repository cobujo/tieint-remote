from dataclasses import dataclass
from acad.entity import AcadEntity
from acad.attribute import AcDbAttribute
from acad.dynamic_block_reference_property import AcadDynamicBlockReferenceProperty
from acad.utils import AcadUtil, AcadAttributeError
from sql.models import AcDbBlockReferenceBase
from pywintypes import com_error
from mylogger import logger


@dataclass
class AcDbBlockReference(AcadEntity, AcadUtil):
    """
    autoscript generated
    """

    @property
    def effective_name(self):
        return self.obj.EffectiveName

    @property
    def has_attributes(self):
        return self.obj.HasAttributes

    @property
    def insertion_point(self):
        return self.obj.InsertionPoint

    @property
    def ins_units(self):
        return self.obj.InsUnits

    @property
    def ins_units_factor(self):
        return self.obj.InsUnitsFactor

    @property
    def is_dynamic_block(self):
        return self.obj.IsDynamicBlock

    @property
    def name(self):
        return self.obj.Name

    @property
    def normal(self):
        return self.obj.Normal

    @property
    def rotation(self):
        return self.obj.Rotation

    @property
    def x_effective_scale_factor(self):
        return self.obj.XEffectiveScaleFactor

    @property
    def x_scale_factor(self):
        return self.obj.XScaleFactor

    @property
    def y_effective_scale_factor(self):
        return self.obj.YEffectiveScaleFactor

    @property
    def y_scale_factor(self):
        return self.obj.YScaleFactor

    @property
    def z_effective_scale_factor(self):
        try:
            return self.obj.ZEffectiveScaleFactor
        except com_error:
            return

    @property
    def z_scale_factor(self):
        return self.obj.ZScaleFactor

    def convert_to_anonymous_block(self):
        return self.obj.ConvertToAnonymousBlock()

    def convert_to_static_block(self, new_block_name):
        return self.obj.ConvertToStaticBlock(newBlockName=new_block_name)

    def explode(self):
        return self.obj.Explode()

    def get_attributes(self):
        try:
            raw_attrs = [ra for ra in self.obj.GetAttributes()]
            return [AcDbAttribute(com_obj=o, _block_reference_handle=self._handle_static) for o in raw_attrs]
        except AttributeError as e:
            self.attr_errors.append(AcadAttributeError(name='get_attributes', error=e))
            return

    # what are these? would we ever need to store these along with typical attributes?
    def get_constant_attributes(self):
        return self.obj.GetConstantAttributes()

    def get_dynamic_block_properties(self):
        if self.is_dynamic_block:
            return [AcadDynamicBlockReferenceProperty(o, self.handle) for o in self.obj.GetDynamicBlockProperties()]

        return

    def reset_block(self):
        return self.obj.ResetBlock()

    def db_process_in_session_(self, session, space=None):
        if not self.valid_handle():
            return

        dct = self._dict_from_shared(model=AcDbBlockReferenceBase, excludes=['handle'])
        dct['handle'] = self._handle_static

        instance = self.db_add_in_session_(model=AcDbBlockReferenceBase, session=session, space=space, dct=dct)
        if not instance:
            return

        coord_attr = 'insertion_point'
        reqd_attr = coord_attr
        coord_import = self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=coord_attr, space=space, obj_instance=instance)

        if not self.coordinate_import_ok(attrs_with_errors=coord_import, required_attrs=reqd_attr):
            logger.error(f'coordinates did not import for handle: {self._handle_static}')
            return

        attrs = self.get_attributes()
        if attrs:
            [a.db_process_in_session_(session=session, space=space) for a in attrs]

        dbp = self.get_dynamic_block_properties()
        if dbp:
            [d.db_process_in_session_(session=session, space=space) for d in dbp]

        self.db_process_bounding_box_in_session_(session=session, space=space, obj_instance=instance)
