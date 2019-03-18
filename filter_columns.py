import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 

import Autodesk
from Autodesk.Revit.DB import *   
                          
from System.Collections.Generic import *
                     
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

__window__.Hide()

column_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Columns)
column_instances = column_collector.OfCategory(BuiltInCategory.OST_Columns).WhereElementIsNotElementType()

structural_column_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns)
structural_column_instances = structural_column_collector.OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType()

ids = list()

t = Transaction(doc, 'Reset HideIsolate')	
t.Start()
view.TemporaryViewModes.DeactivateAllModes()
t.Commit()

column_list = zip(column_instances, structural_column_instances)
for i in structural_column_instances:
	ids.append(i.Id)
	
idElements = List[ElementId](ids)

t = Transaction(doc, 'Filter Columns')
t.Start()	
view.IsolateElementsTemporary(idElements)
t.Commit()

__window__.Close()