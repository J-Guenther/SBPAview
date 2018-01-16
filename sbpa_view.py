# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 23:19:31 2017

@author: Jannik
"""
import matplotlib
#matplotlib.use('TkAgg') # "Has no effect" warning

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from skimage.segmentation import mark_boundaries

LARGE_FONT = ("Verdana", 10)

class SbpaViewer(tk.Tk):
    
    def __init__(self, img, segments, fs_array, fs_names, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.title("SBPA Viewer")
        self.geometry("400x300")
        
        self.frames = {}
        
        frame = PlotPage(container, self, img, segments, fs, fs_array)
        
        self.frames[PlotPage] = frame
        
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(PlotPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
        
class PlotPage(tk.Frame):
    
    def __init__(self, parent, controller, img, segments, fs, fs_array):
        tk.Frame.__init__(self, parent)
        
        self.img = img
        self.segments = segments
        self.fs_names = fs_names
        self.fs_array = fs_array
        
        
        # self.label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        # self.label.pack(pady=10,padx=10)
        
        # Box where information is displayed
        self.infoBox = tk.Label(self, text="Bottom Page", font=LARGE_FONT)
        self.infoBox.pack(pady=10,padx=5, side=tk.BOTTOM)
        
        f, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(mark_boundaries(self.img, self.segments))
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#        toolbar = NavigationToolbar2TkAgg(canvas, self)
#        toolbar.update()
        
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.canvas.callbacks.connect('button_press_event', self.on_click)
        
    def on_click(self, event):
        if event.inaxes is not None:
            print(event.xdata, event.ydata)
            self.infoBox.config(text=self.create_output_string(event.xdata, event.ydata))
        else:
            print('Clicked ouside axes bounds but inside plot window')
            
    def get_segment_id(self, x, y):
        return self.segments[int(y),int(x)]
    
    def create_output_string(self, x, y):
        
        current_label = self.get_segment_id(x, y)
        
        string = ""
        string += "Superpixel: " + str(current_label) + "\n"
        
        for i, feature in enumerate(self.fs_names):
            string += feature + ": " + str(self.fs[current_label, i]) + "\n"
            
        return string
        
                