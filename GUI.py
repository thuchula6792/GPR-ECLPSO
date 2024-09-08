# -*- coding: utf-8 -*-
"""
Created on Tue May 28 01:12:58 2024
Author:  Dr. Thu Huynh Van, Assoc. Prof. Cao Hung Pham
#   Emails:  thuxd11@gmail.com, caohung.pham@sydney.edu.au
#            School of Civil Engineering, The University of Sydney, NSW 2006, Australia
@author: oxnh0
"""
import pandas as pd
import numpy as np
import pickle
from PIL import Image, ImageOps, ImageTk
import matplotlib.pyplot as plt
import PySimpleGUI as sg

left_col = [
    [sg.Text("Enter dh:"), sg.InputText(key='-VF-')],
    [sg.Text("Enter s:"), sg.InputText(key='-FY-')],
    [sg.Text("Enter t:"), sg.InputText(key='-FCO-')],
    [sg.Text("Enter e1:"), sg.InputText(key='-ROHSY-')],
    [sg.Text("Enter e2:"), sg.InputText(key='-FO-')],
    [sg.Button("Predict")]]

parameters = ['t', 'dh', 'e1', 's', 'e2']
sg.theme('DefaultNoMoreNagging')
# %%   
layout = [
    [sg.Text('Define the input parameters', text_color='blue', font=(''))],
    [sg.Column(layout=[
            [sg.Frame(layout=[
                [sg.Text('Thickness of CSF channel, t (mm)', size=(38, 1)), sg.Input(key='-FCO-', size=(10, 1), enable_events=True)],
                [sg.Text('Diameter of the hole, dh (mm)', size=(38, 1)), sg.Input(key='-VF-', size=(10, 1), enable_events=True)],
                [sg.Text('End distance, e1 (mm)', size=(38, 1)), sg.Input(key='-ROHSY-', size=(10, 1), enable_events=True)],
                [sg.Text('Shear distance, s (mm)', size=(38, 1)), sg.Input(key='-FY-', size=(10, 1), enable_events=True)],
                [sg.Text('Edge distance, e2 (mm)', size=(38, 1)), sg.Input(key='-FO-', size=(10, 1), enable_events=True)]],
            title='Input parameters')], ], justification='left'),
    ],
    [sg.Button('Predict'), sg.Button('Cancel')],
    [sg.Frame(layout=[
    [sg.Text('Shear strength, P (kN)'), sg.Input(key='-FP-', size=(30, 1), enable_events=True)]],title='Output')]]
img2 = Image.open('Thu_Huynh.jpeg')
img3 = Image.open('Cao_Hung.jpg')
img4 = Image.open('Logo.jpg')
widths = [img2.width]
heights = [img2.height]
min_width = min(widths)
min_height = min(heights)

widths_4 = [img4.width]
heights_4 = [img4.height]
min_width_4 = min(widths_4)
min_height_4 = min(heights_4)

img2 = ImageOps.fit(img2, (min_width, min_height))
img3 = ImageOps.fit(img3, (min_width, min_height))
img4 = ImageOps.fit(img4, (min_width_4, min_height_4))
scale_factor = 0.11
img2 = img2.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img3 = img3.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img4 = img4.resize((int(min_width_4 * 0.3), int(min_height_4 * 0.3)))
img2.save('image22.png')
img3.save('image33.png')
img4.save('image44.png')
fig2 = sg.Image(filename='image22.png', key='-fig2-', size=(min_width * scale_factor, min_height * scale_factor))
fig3 = sg.Image(filename='image33.png', key='-fig3-', size=(min_width * scale_factor, min_height * scale_factor))
fig4 = sg.Image(filename='image44.png', key='-fig4-', size=(min_width_4 * 0.3, min_height_4 * 0.3))

layout += [
    [sg.Text('')],
    [sg.Column([[sg.Text('Authors: Dr. Van Thu Huynh' + '\n'
             '             Assoc. Prof. Cao Hung Pham' + '\n'
             '             The University of Sydney')],
    [sg.Column([[fig4]], element_justification='right')],
    ],element_justification='center'), sg.Column([[fig2, fig3],], element_justification='right')],]
window = sg.Window('Strength of shear beam-end bolted connections in CFS channel', layout)
predictions_made = False
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break 
    if event == 'Predict':
        
        if values['-FCO-'] == '' or values['-VF-'] == '' or values['-ROHSY-'] == '' or values['-FY-'] == '' or values['-FO-'] == '':

            window['-FP-'].update('Please fill all the input parameters')

        else:
            input_data1 = np.array([
                float(values['-FCO-']),
                float(values['-VF-']),
                float(values['-ROHSY-']),
                float(values['-FY-']),
                float(values['-FO-'])]).reshape(1, -1)
            input_data = pd.DataFrame(input_data1, columns=['t', 'dh', 'e1', 's', 'e2'])
            Xmin = np.array([1.2, 9, 20, 20, 15])
            Xmax = np.array([1.5, 14, 25, 50, 30])
            input_data = (input_data - Xmin)/(Xmax - Xmin)
            with open('model.pkl', 'rb') as f:
                gpr = pickle.load(f)             
            gpr_pred = gpr.predict(input_data)
            window['-FP-'].update(np.round((gpr_pred[0]),4))
window.close()
