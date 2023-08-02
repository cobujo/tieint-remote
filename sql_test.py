import win32com.client as client
from os import listdir, path
from os.path import isfile, join
from sql import engine_named, session_scope
from acad.leader import AcDbLeader
from acad.block_reference import AcDbBlockReference
from acad.spline import AcDbSpline
from acad.viewport import AcDbViewport
from acad.document import AcadDocument
from acad.wipeout import AcDbWipeout
from acad.hatch import AcDbHatch
from sql import session_scope, engine_named


def tester():
    folder = r'c:\holder'
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    dwg = [f for f in files if f.lower().endswith('.dwg')][0]

    acad_app = client.dynamic.Dispatch("AutoCAD.Application")

    # dictionary with ObjectName: dwg

    name_dwg = {}

    print(f'working {dwg}')
    file = path.join(folder, dwg)
    doc_raw = acad_app.Documents.Open(file)
    doc = AcadDocument(doc_raw)
    #
    # raw_objs = [obj for obj in doc_raw.Paperspace]
    # print(f'attempting to iterate through {len(raw_objs)} objects')
    # if raw_objs:
    #     try:
    #         for obj in raw_objs:
    #             if obj.ObjectName not in name_dwg:
    #                 name_dwg[obj.ObjectName] = dwg
    #
    #     except Exception as e:
    #         print(f'Unable to get objects from {dwg}: {e}')
    #
    #     names = [o.ObjectName for o in raw_objs]
    #
    # print('got stuff from the DWG')
    #
    # objs_raw = [o for o in raw_objs if o.ObjectName == 'AcDbBlockReference']
    # # objs_raw = [o for o in raw_objs if 'Polyline' in o.ObjectName]
    # # lst = [o.ObjectName for o in objs_raw]
    #
    # objs = [AcDbBlockReference(b) for b in objs_raw]
    # dyn = next(b for b in objs if b.is_dynamic_block)
    # return doc, raw_objs, objs
    return doc