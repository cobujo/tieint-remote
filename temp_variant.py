import pythoncom
from win32com.client import VARIANT


com_obj = 'representative of the COMObject from paperspace or modelspace'
# value can be list of one or many
var = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, ([com_obj]))

doc_com_obj = 'representative of COMObject for acad document (drawing)'
sset = doc_raw.SelectionSets('myset')

sset.AddItems(var)

