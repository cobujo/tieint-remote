from dataclasses import dataclass, field
import win32com.client as client
from mylogger import logger
from sql.models import ObjectCoordinates
from sql.helpers import db_add_or_merge
from sqlalchemy.exc import IntegrityError
from acad import Spaces, grouper
from typing import Optional, Union
from pywintypes import com_error
import warnings
from acad.comwrapper import ComWrapper


def _tuple_2d_or_3d(coords: Union[str, list]) -> Optional[int]:
    if not coords:
        raise ValueError('expecting tuple or list of coordinates but received None')

    if len(coords) % 2 and len(coords) % 3:
        z = coords[2::3]
        if all(n == 0 for n in z):
            return 3
        # if z values are all the same but != 0, most likely 3D coordinates with Z on same plane
        elif all(n == z[0] for n in z):
            logger.warning(f'coordinates appear to be 3D, z values are {z[0]}')
            return 3
        else:
            return 2

    elif len(coords) % 2:
        return 2

    elif len(coords) % 3:
        return 3

    else:
        raise ValueError(f'coordinates ({type(coords)}) has {len(coords)} elements, unable to determine dimensionality')


@dataclass
class AcadObject(object):
    """
    autoscript generated
    """
    com_obj: client.CDispatch
    obj: ComWrapper = field(init=False)
    _handle_static: Optional[str] = None

    def __post_init__(self):
        self.obj = ComWrapper(self.com_obj)

    @property
    def application(self):
        return self.obj.Application

    @property
    def document(self):
        from acad.document import AcadDocument
        return AcadDocument(self.obj.Document)

    @property
    def handle(self) -> str:
        return self.obj.Handle

    @property
    def has_extension_dictionary(self):
        return self.obj.HasExtensionDictionary

    @property
    def object_id(self):
        return self.obj.ObjectID

    @property
    def object_name(self):
        return self.obj.ObjectName

    @property
    def owner_id(self):
        return self.obj.OwnerID

    def delete(self) -> None:
        return self.obj.Delete()

    def get_extension_dictionary(self):
        return self.obj.GetExtensionDictionary()

    def get_x_data(self, app_name, x_data_type, x_data_value):
        return self.obj.GetXData(AppName=app_name, XDataType=x_data_type, XDataValue=x_data_value)

    def set_x_data(self, x_data_type, x_data_value):
        return self.obj.SetXData(XDataType=x_data_type, XDataValue=x_data_value)

    def _db_process_prop_nd_coordinates_array_in_session(self, session, attr_name, group_size: int,
                                                         space: Optional[str] = None, index: Optional[int] = None,
                                                         args: Optional[tuple] = None, obj_instance=None):
        group_sizes = (2, 3)
        if group_size not in group_sizes:
            raise ValueError(f'group size for coordinates must be one of these: {group_sizes}, you put: {group_size}')

        if isinstance(args, tuple):
            if not args:
                grouped = grouper(size=group_size, iterable=getattr(self, attr_name)())
            else:
                grouped = grouper(size=group_size, iterable=getattr(self, attr_name)(*args))
        elif args is None:
            grouped = grouper(size=group_size, iterable=getattr(self, attr_name))
        else:
            raise ValueError(f'unable to complete function given args value: {args}')

        # as of now we're still using the process 3d coord function, and fudging in z=None when given 2d coordinates only
        attr_issues = []
        for order, coord in enumerate(grouped):
            if group_size == 2:
                coord = (coord[0], coord[1], None)

            attr_issues.append(
                self.db_process_prop_3d_coordinates_in_session_(session=session, attr_name=attr_name, space=space,
                                                                index=index, order=order, coords=coord, args=args,
                                                                obj_instance=obj_instance))

        return attr_issues

    def db_process_prop_3d_coordinates_array_in_session_(self, session, attr_name: str, space: Optional[str] = None,
                                                         index: Optional[int] = None, args: Optional[tuple] = None,
                                                         obj_instance=None):

        self._db_process_prop_nd_coordinates_array_in_session(
            session=session,
            attr_name=attr_name,
            group_size=3,
            space=space,
            index=index,
            args=args,
            obj_instance=obj_instance)

    def db_process_prop_2d_coordinates_array_in_session_(self, session, attr_name: str, space: Optional[str] = None,
                                                         index: Optional[int] = None, args: Optional[tuple] = None,
                                                         obj_instance=None):

        self._db_process_prop_nd_coordinates_array_in_session(
            session=session,
            attr_name=attr_name,
            group_size=2,
            space=space,
            index=index,
            args=args,
            obj_instance=obj_instance)

    def db_process_prop_3d_coordinates_in_session_(self, session, attr_name, space: Optional[str] = None,
                                                   index: Optional[int] = None, order: Optional[int] = None,
                                                   coords: Optional[tuple] = None, args: Optional[tuple] = None,
                                                   obj_instance=None):
        if not coords:
            coord_input_msg = f'{self.__class__.__name__}.{attr_name}'
            try:
                if isinstance(args, tuple):  # attr_name is for a method, not property
                    if not args:  # empty tuple -> method with no args
                        coords = getattr(self, attr_name)()
                    else:
                        coords = getattr(self, attr_name)(*args)

                elif args is None:
                    coords = getattr(self, attr_name)
                else:
                    raise ValueError(f'unable to complete function given args value: {args}')

            except AttributeError:
                logger.error(f'{self.__class__.__name__} has no attribute: {attr_name}')
                return attr_name
        else:
            coord_input_msg = 'coords arg'

        if not isinstance(coords, tuple):
            logger.error(f'expected {coord_input_msg} to be tuple, instead is: {type(coords)}')
            return

        co = ObjectCoordinates(
            document_name=self.document.name,
            handle_id=self._handle_static,
            property=attr_name,
            class_name=self.__class__.__name__,
            x=coords[0],
            y=coords[1],
            z=coords[2],
            order=order,
            index=index
        )
        if space in Spaces:
            co.space = space
        else:
            warnings.warn(f'Expecting value for space to be one of: {Spaces}, instead received {space}')

        if obj_instance:
            co.object = obj_instance

        db_add_or_merge(instance=co, session_scope=session)

    @staticmethod
    def coordinate_import_ok(attrs_with_errors: Union[list, str], required_attrs: Union[list, str]) -> bool:
        """
        basic function to take returned attr_names when
        :param attrs_with_errors:
        :param required_attrs:
        :return:
        """
        if not attrs_with_errors:
            return True

        if isinstance(attrs_with_errors, str):
            attrs_with_errors = [attrs_with_errors]

        if not any(attrs_with_errors):
            return True

        if isinstance(required_attrs, str):
            required_attrs = [required_attrs]

        # we know our class has handle attribute, but in these cases usually there's no handle, need to test
        # handle = getattr(self, 'handle', None)
        fatal_coord_errors = list(set(attrs_with_errors) & set(required_attrs))
        if fatal_coord_errors:
            # TODO: Mild -> eventually import these errors to db (pass session to function) instead of just logging?
            # logger.error(f'{self.object_name} (handle: {handle}) can not be imported due to coordinate error on: {fatal_coord_errors}, attempting to proceed...')
            logger.error(
                f'*something* can not be imported due to coordinate error on: {fatal_coord_errors}, attempting to proceed...')
            return False

        else:
            # logger.warning(f'{self.object_name} (handle: {handle}) has coordinate error on: {attrs_with_errors}, but not fatal, attempting to import...')
            logger.warning(
                f'*something* has coordinate error on: {attrs_with_errors}, but not fatal, attempting to import...')

        return True

    def valid_handle(self, verbose=False):
        """
        basic function to check if handle is None
        - if it is None, will most likely cancel any attempt at db import as this is an essential attribute and most likely
          indicates a bad object
        :return:
        """
        try:
            name = self.object_name
        except (AttributeError, com_error):
            name = '*bad name*'

        handle = self.handle
        if not handle:
            logger.error(f'{name} has no handle! Will not proceed with db imports')
            return

        self._handle_static = handle
        if verbose:
            logger.info(f'{name} handle appears ok: {handle}')

        return True
