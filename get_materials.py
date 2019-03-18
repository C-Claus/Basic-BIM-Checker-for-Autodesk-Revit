"""
MIT License

Copyright (c) 2018 C. Claus 

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
import collections
from collections import OrderedDict
from collections import defaultdict


clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("RevitAPI") 
clr.AddReference("RevitAPIUI")

import Autodesk
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent


import System
from System.Collections.Generic import *
from System.Collections import *
from System import *
from System.Drawing import Point, Icon, Color
from System.Drawing import Color, Font, FontStyle, Point
from System.Windows.Forms import (Application, BorderStyle, FormBorderStyle, Button, CheckBox, Form, Label, Panel, ToolTip, RadioButton, CheckedListBox, CheckState)
from System.Drawing import Icon



app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView


__window__.Hide()
__window__.Close()
     
######################################################################################################
######################################### Get Revit Materials ########################################
######################################################################################################       
id_level_dict = collections.defaultdict(list)

materials_list = ['OST_Materials']        
material_categories = System.Enum.GetValues(BuiltInCategory)

t3, t4 = [],[]
categories_assembly_code_list = []

for material_category, builtin_material_category in [(material_category,builtin_material_category) for material_category in materials_list for builtin_material_category in material_categories]:
    if material_category == builtin_material_category.ToString():
        t3.append(FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(builtin_material_category).ToElements())
        t4.append(builtin_material_category)
        

material_elements, categories = [], []
material_elements_list = []

for i in range(len(t3)):
    if t3[i]:
    	print t3
        material_elements.append(t3[i])
        categories.append(t4[i])
        
for i in material_elements:
    for j in i:
        material_elements_list.append(j)   
       
sorted_material_list = sorted(material_elements_list)

######################################################################################################
############################### Graphical User Interface Class #######################################
######################################################################################################
width = 500
height = 990


class MaterialFilter(IExternalEventHandler, Form):
    def __init__(self):
        
        self.check_value = []
        self.selected_code_list = []
        
        self.BorderStyle = BorderStyle.Fixed3D
        self.Width = width
        self.Height = height
        self.Text = "Basic BIM Checker | Materials"
        self.MaximizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        
        self.Controls.Add(self.header(0,0))
        self.Controls.Add(self.panel(0,80))
        #self.Controls.Add(self.footer(0,930))

    
    def header(self, x, y):
        
        style = FontStyle.Bold 

        levels_selected = '-'
        objects_selected = '-'
        
        self.sublabel = Label()
        self.sublabel.Text = "Materials"
        self.sublabel.Location = Point(x+40, y+10)
        self.sublabel.Width = width-200
        self.sublabel.Font = Font("Calibri Light", 12) 
        #self.sublabel.ForeColor = Color.White
        #self.sublabel.ForeColor = Color.FromArgb(242, 112, 108)
        #self.sublabel.ForeColor = Color.Black
        
        self.sublabel_objects = Label()
        self.sublabel_objects.Text = "List of all materials in the project"
        self.sublabel_objects.Location = Point(x+40, y+30)
        self.sublabel_objects.Width = width-200
        self.sublabel_objects.Font = Font("Calibri Light", 12) 
        self.sublabel_objects.ForeColor = Color.White
        #self.sublabel_objects.ForeColor = Color.FromArgb(242, 112, 108)
        self.sublabel_objects.ForeColor = Color.Black
        
        self.sublabel_no_selection = Label()
        self.sublabel_no_selection.Text = ""
        self.sublabel_no_selection.Location = Point(x+40, y+50)
        self.sublabel_no_selection.Width = width-200
        self.sublabel_no_selection.Font = Font("Calibri Light", 12)
        #self.sublabel_no_selection.ForeColor = Color.White 
        self.sublabel_no_selection.ForeColor = Color.FromArgb(242, 112, 108)
        self.sublabel_no_selection.ForeColor = Color.Black
        
        self.header = Panel()
        self.header.Width = width
        self.header.Height = 80
        self.header.AutoSize = True
        self.header.Font = Font("Calibri", 12) 
        self.header.Location = Point(x,y)
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

        j=30
        
        for x in sorted_material_list:
        	self.checkbox =Label()
        	self.checkbox.Text = str(x.Name)
        	self.checkbox.Location = Point(35, j)
        	j+=25
        	
        	self.checkbox.Width = width-95
        	self.checkbox.Font = Font("Calibri Light",10)
        	self.panel.Controls.Add(self.checkbox)
        	
        return self.panel
            



form = MaterialFilter()

#form.BringToFront
#Application.Run(form)
#form.ShowDialog()
#form.BringToFront
#external_event = ExternalEvent.Create(form)
form.ShowDialog()
#Application.Run(form)
#Application.Run(form)


__window__.Hide()
__window__.Close()