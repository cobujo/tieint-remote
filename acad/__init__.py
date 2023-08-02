from typing import Optional
import win32com.client as client
from typing import Union

Spaces = ('paper', 'model')

ACAD_OBJS_KEY = 'acad_objs'
NO_OBJECT_NAME_KEY = 'no_obj_name'
NO_DATABASE_OBJECT_KEY = 'no_db_obj'

ACAD_DISPATCH = "AutoCAD.Application"


def vba_array(array: Union[list, tuple]):
    return client.VARIANT(client.pythoncom.VT_ARRAY | client.pythoncom.VT_R8, array)


def init_acad():
    return client.dynamic.Dispatch(ACAD_DISPATCH)


def get_or_init_acad_raw():
    try:
        acad = client.GetActiveObject(ACAD_DISPATCH)
    except:
        acad = client.Dispatch(ACAD_DISPATCH)

    return acad


def grouper(size, iterable):
    args = [iter(iterable)] * size
    return zip(*args)


def convert_raw_objs_to_acad(objs: list) -> Optional[dict]:
    from acad.arc import AcDbArc
    from acad.block_reference import AcDbBlockReference
    from acad.circle import AcDbCircle
    from acad.ellipse import AcDbEllipse
    from acad.hatch import AcDbHatch
    from acad.leader import AcDbLeader
    from acad.line import AcDbLine
    from acad.mleader import AcDbMLeader
    from acad.mtext import AcDbMText
    from acad.point import AcDbPoint
    from acad.polyline import AcDbPolyline
    from acad.spline import AcDbSpline
    from acad.text import AcDbText
    from acad.twod_polyline import AcDb2dPolyline
    from acad.viewport import AcDbViewport
    from acad.wipeout import AcDbWipeout
    from acad.attribute_definition import AcDbAttributeDefinition
    from acad.dim_rotated import AcDbRotatedDimension

    acad_results_dict = {
        ACAD_OBJS_KEY: [],
        NO_OBJECT_NAME_KEY: [],
        NO_DATABASE_OBJECT_KEY: {}
    }

    DB_ENTITY_CLASSES = [
        AcDbArc,
        AcDbBlockReference,
        AcDbCircle,
        AcDbEllipse,
        AcDbHatch,
        AcDbLeader,
        AcDbLine,
        AcDbMLeader,
        AcDbMText,
        AcDbPoint,
        AcDbPolyline,
        AcDbSpline,
        AcDbText,
        AcDb2dPolyline,
        AcDbViewport,
        AcDbWipeout,
        AcDbAttributeDefinition,
        AcDbRotatedDimension
    ]
    DB_ENTITY_CLASSES_DICT = {c.__name__: c for c in DB_ENTITY_CLASSES}

    for raw in objs:
        object_name = None
        try:
            object_name = raw.ObjectName
        except AttributeError:
            acad_results_dict[NO_OBJECT_NAME_KEY].append(raw)

        if object_name:
            if object_name in DB_ENTITY_CLASSES_DICT:
                acad_obj = DB_ENTITY_CLASSES_DICT.get(object_name)(raw)
                acad_results_dict[ACAD_OBJS_KEY].append(acad_obj)

            else:
                # no_db_objs will have the object_name as key, and a list of raw objects as values
                if object_name not in acad_results_dict[NO_DATABASE_OBJECT_KEY]:
                    acad_results_dict[NO_DATABASE_OBJECT_KEY][object_name] = [raw]
                else:
                    acad_results_dict[NO_DATABASE_OBJECT_KEY][object_name].append(raw)

    return acad_results_dict
