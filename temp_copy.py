import win32com.client as client
from os import listdir, path
from os.path import isfile, join
from acad.document import AcadDocument
from win32com.client import Dispatch, VARIANT
from pythoncom import VT_VARIANT
import collections

def variant(data):
    return VARIANT(VT_VARIANT, data)


def vararr(*data):
    if len(data) == 1 and isinstance(data, collections.Iterable):
        data = data[0]
    return map(variant, data)


folder = r'c:\holder'
source_dwg = 'drawing1.dwg'
dest_dwg = 'drawing2.dwg'

acad_app = client.dynamic.Dispatch("AutoCAD.Application")

source_file = path.join(folder, source_dwg)
doc_source_raw = acad_app.Documents.Open(source_file)
doc_source = AcadDocument(doc_source_raw)

dest_file = path.join(folder, dest_dwg)
doc_dest_raw = acad_app.Documents.Open(dest_file)
doc_dest = AcadDocument(doc_dest_raw)
