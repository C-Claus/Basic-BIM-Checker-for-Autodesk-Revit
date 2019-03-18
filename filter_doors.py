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

door_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors)
door_instances = door_collector.OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType()

ids = list()

t = Transaction(doc, 'Reset HideIsolate')	
t.Start()
view.TemporaryViewModes.DeactivateAllModes()
t.Commit()

for i in door_instances:
	ids.append(i.Id)
	
idElements = List[ElementId](ids)

t = Transaction(doc, 'Filter Doors')
t.Start()	
view.IsolateElementsTemporary(idElements)
t.Commit()

__window__.Close()