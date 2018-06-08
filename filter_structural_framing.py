import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
clr.AddReference("Microsoft.Office.Interop.Excel")

import Autodesk
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import *

from random import randint

from Autodesk.Revit.UI import (TaskDialog, TaskDialogCommonButtons,
                               TaskDialogCommandLinkId, TaskDialogResult)
                               
                       
                               
from System.Collections.Generic import *
from System.Collections import *
from System import *
from math import *
from System.Runtime.InteropServices import Marshal                              
                               
                               
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

structural_framing_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming)
structural_framing_instances = structural_framing_collector.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType()

#active_view_elements = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements

ids = list()

t = Transaction(doc, 'Reset HideIsolate')	
t.Start()
view.TemporaryViewModes.DeactivateAllModes()
t.Commit()

for i in structural_framing_instances:
	ids.append(i.Id)
	
idElements = List[ElementId](ids)

	
t = Transaction(doc, 'Structural Framing')
	
t.Start()	
	
view.IsolateElementsTemporary(idElements)


t.Commit()

__window__.Close()