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

structuralframing_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming)
structuralframing_instances = structuralframing_collector.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType()

ids = list()

t = Transaction(doc, 'Reset HideIsolate')	
t.Start()
view.TemporaryViewModes.DeactivateAllModes()
t.Commit()

for i in structuralframing_instances:
	ids.append(i.Id)
	
idElements = List[ElementId](ids)

t = Transaction(doc, 'Filter Structural Framing')
t.Start()	
view.IsolateElementsTemporary(idElements)
t.Commit()

__window__.Close()