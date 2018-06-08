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
###################################Get Built in Categories############################################
######################################################################################################
categories_list = [    
                                'OST_Walls',
                                'OST_Floors',
                                'OST_Ceilings',
                                'OST_StructuralFraming',
                                'OST_StructuralFoundation',
                                'OST_StructuralColumns',
                                'OST_Roofs', 
                                'OST_Ramps',
                                'OST_Stairs',
                                'OST_Site',
                                'OST_DuctTerminal', 
                                'OST_Casework',
                                'OST_CableTray',
                                'OST_Conduit', 
                                'OST_ElectricalFixtures',
                                'OST_Furniture',
                                'OST_GenericModel',
                                'OST_Gutter',
                                'OST_MechanicalEquipment',
                                'OST_PlumbingFixtures',
                                'OST_Doors',
                                'OST_Windows',
                                'OST_CurtainWallMullions',
                                'OST_CurtainWallPanels',
                                'OST_RailingBalusterRail',
                                'OST_RailingBalusterRailCut',
                                'OST_RailingHandRail',
                                'OST_RailingHandRailAboveCut',
                                'OST_RailingRailPathExtensionLines',
                                'OST_RalingRailPathLines',
                                'OST_Railings',
                                'OST_RailingSystem',
                                'OST_RailingsystemBaluser'
                                
                                ]        
        
        
builtin_categories = System.Enum.GetValues(BuiltInCategory)

t1, t2 = [],[]
categories_assembly_code_list = []

for category, builtin_category in [(category,builtin_category) for category in categories_list for builtin_category in builtin_categories]:
    if category == builtin_category.ToString():
        t1.append(FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(builtin_category).ToElements())
        t2.append(builtin_category)
        
elements, categories = [], []
categories_list = []

for i in range(len(t1)):
    if t1[i]:
        elements.append(t1[i])
        categories.append(t2[i])
        
for i in elements:
    for j in i:
        categories_list.append(j)


 

######################################################################################################
##########################################Get Levels##################################################
######################################################################################################   
id_level_dict = collections.defaultdict(list)

level_list = [  'Level',
				'Base Level',
				'Reference Level',
				'Base Constraint',
				'Host',
				'Work Plane'
				]

levels_list = []
level_names_list = []

for i in categories_list:

    element_type = doc.GetElement(i.GetTypeId())
    for level_names in level_list:
    	if i.LookupParameter(str(level_names)):
    		level_names_list.append(i.LookupParameter(str(level_names)).AsValueString())
    		id_level_dict[doc.GetElement(i.Id)] = i.LookupParameter(str(level_names)).AsValueString()
    


######################################################################################################
#####################################Sort Level List##########################################
######################################################################################################
level_list    = []    

for i in set(level_names_list):
    if i != '':
        level_list.append(i)
    
sorted_level_list = sorted(level_list)


######################################################################################################
################################Graphical User Interface Class########################################
######################################################################################################
width = 500
height = 990



class LevelFilter(Form):
    def __init__(self):
        
        self.check_value = []
        self.selected_code_list = []
        
        self.BorderStyle = BorderStyle.Fixed3D
        self.Width = width
        self.Height = height
        self.Text = "Level Filter | Version 1.0"
        self.MaximizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        
        self.Controls.Add(self.header(0,0))
        self.Controls.Add(self.panel(0,80))
        self.Controls.Add(self.footer(0,930))

    
    def header(self, x, y):
        
        style = FontStyle.Bold 

        levels_selected = '-'
        objects_selected = '-'
        
        self.sublabel = Label()
        self.sublabel.Text = "Number of Levels Selected: " + str(levels_selected)
        self.sublabel.Location = Point(x+40, y+10)
        self.sublabel.Width = width-200
        self.sublabel.Font = Font("Calibri Light", 12) 
        #self.sublabel.ForeColor = Color.White
        #self.sublabel.ForeColor = Color.FromArgb(242, 112, 108)
       #self.sublabel.ForeColor = Color.Black
        
        self.sublabel_objects = Label()
        self.sublabel_objects.Text = "Number of Objects Current Selection: " + str(objects_selected)
        self.sublabel_objects.Location = Point(x+40, y+30)
        self.sublabel_objects.Width = width-200
        self.sublabel_objects.Font = Font("Calibri Light", 12) 
        #self.sublabel_objects.ForeColor = Color.White
        self.sublabel_objects.ForeColor = Color.FromArgb(242, 112, 108)
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
        
        for i in range(0, len(sorted_level_list)):
            self.checkbox = CheckBox()
            self.checkbox.Text = str(sorted_level_list[i])
            self.checkbox.Location = Point(35,j)
            j+=25
            self.checkbox.Width = width-95
            self.checkbox.Font= Font("Calibri Light",10)    
            self.panel.Controls.Add(self.checkbox)
            self.check_value.append(self.checkbox)

            
        return self.panel
            
    def footer(self, x, y):

        button_width = (500/3)-6
        
        self.button_filter_selection = Button()
        self.button_filter_selection.Text = 'Filter Selection'
        self.button_filter_selection.Location = Point(2*(button_width),0)
        self.button_filter_selection.Click += self.update
        self.button_filter_selection.Width = button_width
        self.button_filter_selection.Height = 50
        
        self.button_clear_selection = Button()
        self.button_clear_selection.Text = 'Clear Selection'
        self.button_clear_selection.Location = Point(0,0)
        self.button_clear_selection.Width = button_width
        self.button_clear_selection.Height = 50
        self.button_clear_selection.Font =  Font("Calibri Light",12)
        self.button_clear_selection.Click += self.uncheck_checkboxes
        
        self.button_objects_without_level = Button()
        self.button_objects_without_level.Text = 'Objects Without Level'
        self.button_objects_without_level.Location = Point(button_width,0)
        self.button_objects_without_level.Width = button_width
        self.button_objects_without_level.Height = 50
        self.button_objects_without_level.Click += self.check_pushbutton_empty_level
        
        self.footer = Panel()
        self.footer.Width = width-15
        self.footer.Height = 50
        self.footer.Font = Font("Calibri", 12) 
        self.footer.Location = Point(x,y-50)
        #self.footer.BackColor = Color.FromArgb(232, 52, 38)
        self.footer.Controls.Add(self.button_filter_selection)
        self.footer.Controls.Add(self.button_clear_selection)
        self.footer.Controls.Add(self.button_objects_without_level)


        return self.footer
        


    def update(self, sender, event):
        
        for f in self.check_value:
            if f.Checked == True:
                self.selected_code_list.append(f.Text)
            if f.Checked == False:
                   pass 
         
        self.check_for_selected_code(selected_code=self.selected_code_list)
        
        for f in self.check_value:
            if f.Text in self.selected_code_list:
                self.selected_code_list.remove(f.Text)
                       

                   
    def uncheck_checkboxes(self, sender, event):

        
        self.sublabel_no_selection.Text = ""
        
        for f in self.check_value:
            f.Checked = False
            
        t = Transaction(doc, 'Reset HideIsolate')    
        t.Start()        
        view.TemporaryViewModes.DeactivateAllModes()
        t.Commit()    
        
        levels_selected = '-'
        objects_selected = '-'

        self.sublabel.Text = "Number of Levels Selected: " + str(levels_selected)
        self.sublabel_objects.Text = "Number of Objects Current Selection: " + str(objects_selected)

        
    def check_pushbutton_empty_level(self, sender, args):
        self.check_empty_level(selected_code=sender.Text) 
        
    def check_empty_level(self, selected_code):
    
        self.sublabel_no_selection.Text = ""
  
        ids = list()

        element_instances = []

        for i, v in id_level_dict.iteritems():
            if v == '':
                element_instances.append(i.Id)
                ids.append(i.Id)
                    
        self.sublabel_objects.Text = "Number of Objects Current Selection: " + str(len(ids))
        levels_selected = '-'
        self.sublabel.Text = "Number of Levels Selected: " + str(levels_selected)
        
  

        #Hide Reset Active View
        t = Transaction(doc, 'Reset HideIsolate')    
        t.Start()        
        view.TemporaryViewModes.DeactivateAllModes()
        t.Commit()    

        idElements = List[ElementId](ids)
        
        #Hide Isolate Objects in Active View
        t = Transaction(doc, 'Filter Elements')
        t.Start()    
        view.IsolateElementsTemporary(idElements)
        t.Commit()

   
    def check_for_selected_code(self, selected_code):
    
        #print selected_code
        if len(selected_code) == 0:
        	
        	self.sublabel_no_selection.Text = "Please select a Level First!"
        
        if len(selected_code) > 0:

	        self.sublabel.Text = "Number of Levels Selected: " + str(len(selected_code))
	
	        ids = list()
	
	        for i, v in id_level_dict.iteritems():
	        	for code in selected_code:
	        		if v == code:
	        			ids.append(i.Id)


	                
	        self.sublabel_objects.Text = "Number of Objects Current Selection: " + str(len(ids))
	        
	        #Hide Reset Active View    
	        t = Transaction(doc, 'Reset HideIsolate')    
	        t.Start()
	        view.TemporaryViewModes.DeactivateAllModes()
	        t.Commit()    
	        
	        idElements = List[ElementId](ids)
	        
	        #Hide Isolate Objects in Active View
	        t = Transaction(doc, 'Filter Elements')    
	        t.Start()    
	        view.IsolateElementsTemporary(idElements)
	        t.Commit()



form = LevelFilter()
#Application.Run(form)
form.ShowDialog()
#form.BringToFront


__window__.Hide()
__window__.Close()