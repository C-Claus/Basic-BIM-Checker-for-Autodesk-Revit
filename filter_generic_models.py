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

generic_model_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel)
generic_model_instances = generic_model_collector.OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType()


ids = list()

t = Transaction(doc, 'Reset HideIsolate')	
t.Start()
view.TemporaryViewModes.DeactivateAllModes()
t.Commit()

for i in generic_model_instances:
	ids.append(i.Id)
	
idElements = List[ElementId](ids)

	
t = Transaction(doc, 'Filter Generic Model')
	
t.Start()	
	
view.IsolateElementsTemporary(idElements)


t.Commit()

__window__.Close()