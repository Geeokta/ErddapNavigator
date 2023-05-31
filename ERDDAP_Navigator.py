# -*- coding: utf-8 -*-
'''
----------------------------------
This software is under MIT License 
----------------------------------

Permission is hereby granted, free of charge, \n to any person obtaining a copy 
of this software and associated documentation \n files (the "Software"), to deal 
in the Software without restriction, including \n without limitation the rights 
to use, copy, modify, merge, publish, distribute, \n sublicense, and/or sell 
copies of the Software, and to permit persons \n to whom the Software is 
furnished to do so, subject to the following \n conditions: 

The above copyright notice and this permission \n notice shall be included in all 
copies or substantial portions of the Software. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY \n OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES \n OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. \n IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY \n CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT \n OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE \n USE OR OTHER DEALINGS IN THE 
SOFTWARE.
'''

'''
Fro more informations about erddapy 
https://ioos.github.io/erddapy/01b-tabledap-output.html
'''
import tkinter
from tkinter import Tk, Label, Button, StringVar,OptionMenu,W,Entry,END,E,Text
from tkinter import scrolledtext
#Import erddap package into 
from erddapy import ERDDAP
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from tkcalendar import Calendar, DateEntry
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import messagebox
import time
import ssl
from tkinter.filedialog import asksaveasfile
#top = tkinter.Tk()
top = ThemedTk(theme="radiance")
top.title('ERDDAP Navigator')
top.option_add('*Font', 'Verdana 8')
top.geometry('750x400')
#to use unverified ssl we need to add this row
ssl._create_default_https_context = ssl._create_unverified_context

def plotData():
    
    myVar=str(clickedVars.get())
    mySecondaryVar=str(clickedSecondaryVars.get())
    
    if myVar!='' and mySecondaryVar!='':
        e = ERDDAP(
            server= str(serverURL.get()),
            protocol="tabledap",
            response="csv",
        )
        
        e.dataset_id = str(clicked.get())

        e.variables = [
            ""+myVar,
            ""+mySecondaryVar
        ]
        e.constraints = {
            "time>=": str(calStart.get_date())+"T00:00:00Z",
            "time<=": str(calEnd.get_date())+"T23:59:59Z",}
        
        try:
            url = e.get_download_url()
            
            # Convert URL to pandas dataframe
            df_MySite = e.to_pandas(  
                parse_dates=True,
            ).dropna()
            
            MyThemeTMP=MyTheme.get()
            plt.style.use(MyThemeTMP)
            MyLineTMP=MyLine.get()
            df_MySite.plot(x=df_MySite.columns[1], y=df_MySite.columns[0], kind=MyLineTMP)
            plt.show()
        except Exception as e:
            Info.insert(END, '\nWARNING! Exception ocurred:')
            messagebox.showerror(message='error: "{}"'.format(e))
    else:
        messagebox.showwarning("Message", "Please, select two params to plot (Y/X axis)")

def xlsexport():
    
    myVar=str(clickedVars.get())
    mySecondaryVar=str(clickedSecondaryVars.get())
    if myVar!='' and mySecondaryVar!='':
        e = ERDDAP(
            server= str(serverURL.get()),
            protocol="tabledap",
            response="csv",
        )
        
        e.dataset_id = str(clicked.get())
        myVar=str(clickedVars.get())
        mySecondaryVar=str(clickedSecondaryVars.get())
        e.variables = [
            ""+myVar,
            ""+mySecondaryVar
        ]
        e.constraints = {
            "time>=": str(calStart.get_date())+"T00:00:00Z",
            "time<=": str(calEnd.get_date())+"T23:59:59Z",}
        
        try:
            url = e.get_download_url()
            # Convert URL to pandas dataframe
            df_MySite = e.to_pandas(  
                parse_dates=True,
            ).dropna()
            
            files = [('Excel Document', '*.xlsx')] 
            file = asksaveasfile(filetypes = files, defaultextension = files)
                
            df_MySite.to_excel(file.name,sheet_name='Sheet_name_1')
        except:
            print("An exception occurred")
    else:
        messagebox.showwarning("Message", "Please, select two params to export")
        
        
def check3():
    myVar=str(clickedVars.get())
    mySecondaryVar=str(clickedSecondaryVars.get())
    
    if myVar!='' and mySecondaryVar!='':
        e = ERDDAP(
            server= str(serverURL.get()),
            protocol="tabledap",
            response="csv",
        )
        
        e.dataset_id = str(clicked.get())
        e.variables = [
            ""+myVar,
            ""+mySecondaryVar
        ]
        e.constraints = {
            "time>=": str(calStart.get_date())+"T00:00:00Z",
            "time<=": str(calEnd.get_date())+"T23:59:59Z",}
        
        try:
            # Print the URL - check
            url = e.get_download_url()
            # Convert URL to pandas dataframe
            df_MySite = e.to_pandas(  
                parse_dates=True,
            ).dropna()
            # print the dataframe to check what data is in there specifically. 
            print(df_MySite.head())
            Info.insert(END, '\n'+str(df_MySite.head()))
            print("Number of rows: "+str(len(df_MySite.index)))
            myrows=len(df_MySite.index)
            print("Number of rows pt2: "+str(myrows))
            # print the column names
            print (df_MySite.columns)
            Info.insert(END, '\nNumber of rows: '+str(myrows))
        except Exception as e:
            Info.insert(END, '\nWARNING! Exception ocurred:')
            messagebox.showerror(message='error: "{}"'.format(e))
    else:
        messagebox.showwarning("Message", "Please, select two params")


def check():
    if serverURL.get()!='':
        clickedVars.set('')
        dropVars['menu'].delete(0, 'end')
        clickedSecondaryVars.set('')
        dropSecondaryVars['menu'].delete(0, 'end')
        
        e = ERDDAP(server=str(serverURL.get()))
        
        kw = {
            "min_time": "1900-01-01T00:00:00Z",
        }
        try:
            search_url = e.get_search_url(response="csv", **kw)
            search = pd.read_csv(search_url)
            DTSid = search["Dataset ID"].values
            DTSid_list = "\n".join(DTSid)
            msg_box = ''
            if len(DTSid)>50 :
                msg_box = messagebox.askquestion('WARNING', 'Found '+str(len(DTSid))+' datasets: Are you sure you want to continue? Too many datasets can crash the software',
                                            icon='warning')

            if msg_box == 'yes' or len(DTSid)<=50:
                clicked.set('')
                drop['menu'].delete(0, 'end')
                new_choices=[]
                for myid in DTSid:
                    new_choices.append(myid)

                for choice in new_choices:
                    drop['menu'].add_command(label=choice, command=tk._setit(clicked, choice))

            else:
                messagebox.showwarning("Message", "Ok, the operation has been stopped")

        except Exception as e:
            Info.insert(END, '\nWARNING! Exception ocurred:')
            messagebox.showerror(message='error: "{}"'.format(e))
            
    else:
        messagebox.showwarning("Message", "Please, select an URL")
                        
def changeURL(text):
    tmpURL=str(text)
    serverURL.delete(0,END)
    serverURL.insert(0,tmpURL)
    drop['menu'].delete(0, 'end')
    dropVars['menu'].delete(0, 'end')
    dropSecondaryVars['menu'].delete(0, 'end')

def check2():
    tmpDTS=str(clicked.get())
    if tmpDTS!='':

        try:
            e = ERDDAP(server=str(serverURL.get()))
            info_url = e.get_info_url(dataset_id=tmpDTS, response="csv")
            info = pd.read_csv(info_url)
            info.head()
            dropVars['menu'].delete(0, 'end')
            dropSecondaryVars['menu'].delete(0, 'end')
            rslt_df = info[info['Row Type'] == "variable"]
            print(rslt_df['Variable Name'])
            for choiceVars in rslt_df['Variable Name']:
                print(choiceVars)
                dropVars['menu'].add_command(label=choiceVars, command=tk._setit(clickedVars, choiceVars))
                dropSecondaryVars['menu'].add_command(label=choiceVars, command=tk._setit(clickedSecondaryVars, choiceVars))
                
            clickedVars.set('')
            clickedSecondaryVars.set('')
        except Exception as e:
            Info.insert(END, '\nWARNING! Exception ocurred:')
            messagebox.showerror(message='error: "{}"'.format(e))
    else:
        messagebox.showwarning("Message", "Please, select a dataset")

serverURLLabel=tkinter.Label(top, text='ServerURL (write it or use the menu)')
serverURLLabel.grid(row=0, column=0, sticky=W)
serverURL = Entry(top,width=25)
serverURL.grid(row=0, column=1, sticky=W)

URLoptions = [
    "http://apdrc.soest.hawaii.edu/erddap",
    "https://erddap.bco-dmo.org/erddap",
    "https://canwinerddap.ad.umanitoba.ca/erddap",
    "http://rs-data1-mel.csiro.au/erddap",
    "http://erddap.emodnet-physics.eu/erddap",
    "https://catalogue.hakai.org/erddap",
    "https://erddap.griidc.org/erddap",
    "https://erddap.ichec.ie/erddap",
    "http://erddap.incois.gov.in/erddap",
    "https://jeodpp.jrc.ec.europa.eu/services/erddap",
    "https://erddap.marine.ie/erddap",
    "http://nrm-erddap.nci.org.au/erddap",
    "https://atn.ioos.us/erddap",
    "http://cwcgom.aoml.noaa.gov/erddap",
    "https://coastwatch.pfeg.noaa.gov/erddap",
    "http://erddap.sensors.ioos.us/erddap",
    "http://erddap.axiomdatascience.com/erddap",
    "https://wilson.coas.oregonstate.edu/erddap",
    "http://www.neracoos.org/erddap",
    "https://gliders.ioos.us/erddap",
    "https://pae-paha.pacioos.hawaii.edu/erddap",
    "http://sccoos.org/erddap",
    "http://erddap.secoora.org/erddap",
    "https://ecowatch.ncddc.noaa.gov/erddap",
    "https://oceanview.pfeg.noaa.gov/erddap",
    "http://osmc.noaa.gov/erddap",
    "https://polarwatch.noaa.gov/erddap",
    "https://upwell.pfeg.noaa.gov/erddap",
    "http://dap.onc.uvic.ca/erddap",
    "https://oceanobservatories.org/erddap-server",
    "https://members.oceantrack.org/erddap",
    "http://tds.marine.rutgers.edu/erddap",
    "https://spraydata.ucsd.edu/erddap",
    "https://www.smartatlantic.ca/erddap",
    "https://erddap.oa.iode.org/erddap",
    "https://salishsea.eos.ubc.ca/erddap",
    "https://data.obsea.es/erddap",
    "https://erddap.emso.eu/erddap",
    "https://erddap.emodnet.eu/erddap",
    "https://erddap.emodnet-physics.eu/erddap",
    "http://oceano.bo.ingv.it/erddap",
    "https://coastwatch.noaa.gov/erddap",
    "https://nodc.ogs.it/erddap",
    "https://data.iadc.cnr.it/erddap",
    "https://opendap.co-ops.nos.noaa.gov/erddap"
]
URLclicked = StringVar()
# Create Dropdown menu
URLdrop = OptionMenu( top , URLclicked , *URLoptions, command=changeURL)
URLdrop.config(width=25)
URLdrop.grid(row=0, column=2, sticky=W)

CheckAButton = Button(top, text="Check DATASETS",bg = "SkyBlue2",width=25, command=(check))
CheckAButton.grid(row=1, column=0, sticky=W)

CheckBButton = Button(top, text="Check dataset's PARAMS",bg = "gold",width=25, command=(check2))
CheckBButton.grid(row=1, column=1, sticky=W)

CheckCButton = Button(top, text="Check DATA",bg = "orchid1", command=(check3))
CheckCButton.grid(row=1, column=2, sticky=W)

CheckDButton = Button(top, text="Plot DATA",bg = "orchid1", command=(plotData))
CheckDButton.grid(row=1, column=3, sticky=W)

CheckEButton = Button(top, text="DATA to XLSX",bg = "orchid1", command=(xlsexport))
CheckEButton.grid(row=2, column=3, sticky=W)

# Dropdown menu options
options = [
    ""
]
clicked = StringVar()
# Create Dropdown menu
drop = OptionMenu( top , clicked , *options )
drop.config(width=25)
drop.grid(row=2, column=0, sticky=W)

XaxisLabel=tkinter.Label(top, text='X axis', fg="white", bg="black")
XaxisLabel.grid(row=2, column=1, sticky=W)
# Dropdown menu options
optionsVars = [
    ""
]
clickedVars = StringVar()
# Create Dropdown menu
dropVars = OptionMenu( top , clickedVars , *optionsVars )
dropVars.config(width=15)
dropVars.grid(row=2, column=1, sticky=E)

YaxisLabel=tkinter.Label(top, text='Y axis', fg="white", bg="black")
YaxisLabel.grid(row=2, column=2, sticky=W)
# Dropdown menu options
optionsSecondaryVars = [
    ""
]
clickedSecondaryVars = StringVar()
# Create Dropdown menu
dropSecondaryVars = OptionMenu( top , clickedSecondaryVars , *optionsSecondaryVars )
dropSecondaryVars.config(width=17)
dropSecondaryVars.grid(row=2, column=2, sticky=E)

StartLabel=tkinter.Label(top, text='Start date', fg="white", bg="black")
StartLabel.grid(row=3, column=0, sticky=W)
calStart = DateEntry(top, width=25, background="black", disabledbackground="black", bordercolor="blue", 
               headersbackground="black", normalbackground="black", 
               normalforeground='white', headersforeground='white',
            foreground='white', borderwidth=2)
calStart.grid(row=4, column=0, sticky=W)

EndLabel=tkinter.Label(top, text='End date', fg="white", bg="black")
EndLabel.grid(row=3, column=1, sticky=W)
calEnd = DateEntry(top, width=25, background="black", disabledbackground="black", bordercolor="blue", 
               headersbackground="black", normalbackground="black", 
               normalforeground='white', headersforeground='white',
            foreground='white', borderwidth=2)
calEnd.grid(row=4, column=1, sticky=W)

buttonShowDarkest = Label(top, text ="Choose the plot theme", fg="white", bg="black")
buttonShowDarkest.grid(row=5, column=0, sticky=W)

buttonShowLine = Label(top, text ="Choose the plot Style", fg="white", bg="black")
buttonShowLine.grid(row=5, column=1, sticky=W)

# Dropdown menu options
optionsTheme = [
    "default",
    "classic",
    "dark_background",
    "Solarize_Light2",
    "fast",
    "fivethirtyeight",
    "bmh",
    "ggplot",
    "grayscale",
]
# datatype of menu text
MyTheme = StringVar()
# initial menu text
MyTheme.set( "default" )
# Create Dropdown menu
dropTheme = OptionMenu(top,MyTheme,*optionsTheme )
dropTheme.grid(row=6, column=0, sticky=W)

optionsLine = [
    "scatter",
    "barh",
    "hist",
    "box",
    "area",
    "pie",
]
# datatype of menu text
MyLine = StringVar()
# initial menu text
MyLine.set( "scatter" )
# Create Dropdown menu
dropLine = OptionMenu(top,MyLine,*optionsLine )
dropLine.grid(row=6, column=1, sticky=W)

Info = scrolledtext.ScrolledText(top, height=15, width=100)
Info.grid(row=7, column=0, columnspan=4, sticky=W)
Info.insert(END, '\n ------------------------------------ ')
Info.insert(END, '\n Welcome to ERDDAP Navigator \n(pythonopenprojects@gmail.com)')
Info.insert(END, '\n ------------------------------------ ')


import matplotlib.cm as cm
import matplotlib.font_manager
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.text import TextPath
import matplotlib.transforms as mtrans
MPL_BLUE = '#11557c'

def get_font_properties():
    # The original font is Calibri, if that is not installed, we fall back
    # to Carlito, which is metrically equivalent.
    if 'Calibri' in matplotlib.font_manager.findfont('Calibri:bold'):
        return matplotlib.font_manager.FontProperties(family='Calibri',
                                                      weight='bold')
    if 'Carlito' in matplotlib.font_manager.findfont('Carlito:bold'):
        #print('Original font not found. Falling back to Carlito. '
        #      'The logo text will not be in the correct font.')
        return matplotlib.font_manager.FontProperties(family='Carlito',
                                                      weight='bold')
    #print('Original font not found. '
    #      'The logo text will not be in the correct font.')
    return None

def create_text_axes(fig, height_px):
    """Create an Axes in *fig* that contains 'matplotlib' as Text."""
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_aspect("equal")
    ax.set_axis_off()

    path = TextPath((0, 0), "ERDDAP Navigator", size=height_px * 0.8,
                    prop=get_font_properties())

    angle = 4.25  # degrees
    trans = mtrans.Affine2D().skew_deg(angle, 0)

    patch = PathPatch(path, transform=trans + ax.transData, color=MPL_BLUE,
                      lw=0)
    ax.add_patch(patch)
    ax.autoscale()

def splash_screen(height_px, lw_bars, lw_grid, lw_border, rgrid, with_text=False):
    
    dpi = 100
    height = height_px / dpi
    figsize = (5 * height, height) if with_text else (height, height)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0)

    if with_text:
        create_text_axes(fig, height_px)
    ax_pos = (0.535, 0.12, .17, 0.75) if with_text else (0.03, 0.03, .94, .94)

    return fig, ax_pos
splash_screen(height_px=110, lw_bars=0.7, lw_grid=0.5, lw_border=1,
          rgrid=[1, 3, 5, 7], with_text=True)
plt.show()


top.mainloop()
