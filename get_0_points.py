"""
MIT License

Copyright (c) 2019 C. Claus 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import clr
import sys
from random import random
from random import randint
from math import *
from collections import OrderedDict
import itertools


clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("RevitAPI") 
clr.AddReference("RevitAPIUI")

import Autodesk
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import InvalidOperationException


import System
from System.Collections.Generic import *
from System.Collections import *
from System import *
from System.Drawing import Point, Icon, Color
from System.Drawing import Color, Font, FontStyle, Point
from System.Windows.Forms import (Application, BorderStyle, FormBorderStyle, Button, CheckBox, Form, Label, Panel, ToolTip, RadioButton, CheckedListBox, CheckState, PictureBox)
from System.Drawing import Icon



app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

__window__.Hide()
__window__.Close()

######################################################################################################
################################## Get Built in Categories ###########################################
######################################################################################################
                                
point_list = ['OST_ProjectBasePoint','OST_SharedBasePoint', 'OST_Site', 'OST_BasePointAxisX', 'OST_BasePointAxisY','OST_BasePointAxisZ'] 
    
builtin_categories = System.Enum.GetValues(BuiltInCategory)

  		
total_point_list=[]

for i, builtin_category in [(i, builtin_category) for i in point_list for builtin_category in builtin_categories]:
	if i == builtin_category.ToString():
		filtered_element_collector = FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(builtin_category)
		for x in filtered_element_collector.ToElements():
			if x.LookupParameter("Angle to True North") is not None:
				total_point_list.append([[str(builtin_category.ToString())[4:], ''],
											["E/W",x.LookupParameter("E/W").AsDouble()*304.8],
											["N/S",x.LookupParameter("N/S").AsDouble()*304.8],
											["Elev",x.LookupParameter("Elev").AsDouble()*304.8],
											["Pinned", x.Pinned ],
											["Angle to True North", x.LookupParameter("Angle to True North").AsValueString()],
											[' ',' ']
											])
											
			else:
				total_point_list.append([[str(builtin_category.ToString())[4:], ''],
											["E/W",x.LookupParameter("E/W").AsDouble()*304.8],
											["N/S",x.LookupParameter("N/S").AsDouble()*304.8],
											["Elev",x.LookupParameter("Elev").AsDouble()*304.8],
											["Pinned", x.Pinned ],
										
											[' ',' ']
											])
			

elements, categories = [], []
categories_list = []

######################################################################################################
############################### Graphical User Interface Class #######################################
######################################################################################################
width = 400
height = 500


class AssemblyFilter(IExternalEventHandler, Form):
    def __init__(self):
        
        self.check_value = []
        self.selected_code_list = []
        
        self.BorderStyle = BorderStyle.Fixed3D
        self.Width = width
        self.Height = height
        self.Text = "BasePoint | Version 2.0 | 2019 "
        self.MaximizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        
        
        self.Controls.Add(self.header(0,0))
        self.Controls.Add(self.panel(0,80))
        
    
    def header(self, x, y):
        
        style = FontStyle.Bold 

        assembly_codes_selected = '-'
        objects_selected = '-'
        
        self.sublabel = Label()
        self.sublabel.Text = "ProjectBasePoint (E/W, N/S, Elev)" 
        self.sublabel.Location = Point(x+40, y+10)
        self.sublabel.Width = width-200
        self.sublabel.Font = Font("Calibri Light", 12) 
        self.sublabel.Width = 400
        #self.sublabel.ForeColor = Color.White
        self.sublabel.ForeColor = Color.Black
        
        self.sublabel_objects = Label()
        self.sublabel_objects.Text = "SharedBasePoint (E/W, N/S, Elev)"
        self.sublabel_objects.Location = Point(x+40, y+30)
        self.sublabel_objects.Width = width-200
        self.sublabel_objects.Font = Font("Calibri Light", 12) 
        self.sublabel_objects.Width = 400
        #self.sublabel_objects.ForeColor = Color.White
        self.sublabel.ForeColor = Color.Black
        
        self.sublabel_no_selection = Label()
        self.sublabel_no_selection.Text = ""
        self.sublabel_no_selection.Location = Point(x+40, y+50)
        self.sublabel_no_selection.Width = width-200
        self.sublabel_no_selection.Font = Font("Calibri Light", 12, style)
        #self.sublabel_no_selection.ForeColor = Color.White 
        self.sublabel.ForeColor = Color.Black
        
        self.header = Panel()
        self.header.Width = width
        self.header.Height = 80
        self.header.AutoSize = True
        self.header.Font = Font("Calibri", 12) 
        self.header.Location = Point(x,y)
        #self.header.BackColor = Color.FromArgb(0, 0, 0)
        self.header.BackColor = Color.FromArgb(145, 201, 213)

        self.header.Controls.Add(self.sublabel)
        self.header.Controls.Add(self.sublabel_objects)
        self.header.Controls.Add(self.sublabel_no_selection)
        self.header.AutoScroll = True

    
        return self.header
        
    def panel(self, x, y):
    
        self.panel = Panel()
        self.panel.Width = width-15
        self.panel.Height = 800
        self.panel.Location = Point(x, y)
        self.panel.BorderStyle = BorderStyle.Fixed3D
        self.panel.BackColor = Color.White
        self.panel.AutoScroll = True
       
        
        j = 35
        
        for i in total_point_list:
 
        	for x in i:
	        	self.label = Label()
	        	
	        	if (len(x)) > 1 :
	        		if x[1] is not None:
			        	self.label.Text = str(x[0]) + "  " + str(x[1])
			        	self.label.Location = Point(35,j)
			        	self.label.Width = 400
			        	self.label.Font = Font("Calibri Light", 12)
			        	self.panel.Controls.Add(self.label)
        		j += 25
        
        return self.panel	
  

        



form = AssemblyFilter()

#form.BringToFront

#form.ShowDialog()
#form.BringToFront
external_event = ExternalEvent.Create(form)
Application.Run(form)


#__window__.Hide()
#__window__.Close()