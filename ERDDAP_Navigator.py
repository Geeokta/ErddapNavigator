# -*- coding: utf-8 -*-
'''
https://ioos.github.io/erddapy/01b-tabledap-output.html
'''
import tkinter
from tkinter import Tk, Label, Button, StringVar,OptionMenu,W,Entry,END,E,Text
from tkinter import scrolledtext
#Import erddap package into 
from erddapy import ERDDAP
import numpy as np
import matplotlib.pyplot as plt
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


#https://gliders.ioos.us/erddap
    
#server = "https://data.obsea.es/erddap"
#server = "https://gliders.ioos.us/erddap"

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
        #myVar=str(clickedVars.get())
        #mySecondaryVar=str(clickedSecondaryVars.get())
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
            #print(url)
            
            # Convert URL to pandas dataframe
            df_MySite = e.to_pandas(  
                parse_dates=True,
            ).dropna()
            
            # print the dataframe to check what data is in there specifically. 
            #print(df_MySite.head())
            
            #print("Number of rows: "+str(len(df_MySite.index)))
            # print the column names
            #print (df_MySite.columns)
            # make data
            
            #execute the plot (to decomment)
            #NOTE: add a option menu for the plot type choice
            df_MySite.plot(x=df_MySite.columns[1], y=df_MySite.columns[0], kind='scatter')
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
            # Print the URL - check
            url = e.get_download_url()
            #print(url)
            
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
        #myVar=str(clickedVars.get())
        #mySecondaryVar=str(clickedSecondaryVars.get())
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
            print(url)
            
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
        # make data
        except Exception as e:
            Info.insert(END, '\nWARNING! Exception ocurred:')
            messagebox.showerror(message='error: "{}"'.format(e))
        #execute the plot (to decomment)
        #NOTE: add a option menu for the plot type choice
        #df_MySite.plot(x=df_MySite.columns[1], y=df_MySite.columns[0], kind='scatter')
        #plt.show()
        '''
        df_MySite['time (UTC)']
        
        
        df_MySite.plot (
            x='time (UTC)',
            y=myVar)
        plt.tick_params(axis='x', labelrotation=45)
        plt.show()
        '''
    else:
        #messagebox.showwarning("Message", "Please, select two params to plot (Y/X axis)")
        messagebox.showwarning("Message", "Please, select two params")


def check():
    if serverURL.get()!='':
        e = ERDDAP(server=str(serverURL.get()))
        
        kw = {
            "min_time": "1900-01-01T00:00:00Z",
            #"max_time": "2017-02-10T00:00:00Z",
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
            
                print(f"Found {len(DTSid)} Datasets:\n{DTSid_list}")
                
                #drop.delete(0, END)
                clicked.set('')
                drop['menu'].delete(0, 'end')
                new_choices=[]
                for myid in DTSid:
                    
                    # Reset var and delete all old options
                    
                
                    # Insert list of new options (tk._setit hooks them up to var)
                    new_choices.append(myid)
                    
                    
                    #info_url = e.get_info_url(dataset_id=myid, response="csv")
                    #print(info_url)
                    #info = pd.read_csv(info_url)
                    #info.head()
                    #print(info.head)
                #clicked = StringVar()
                    
                
                for choice in new_choices:
                    drop['menu'].add_command(label=choice, command=tk._setit(clicked, choice))
            
                #options.set(new_choices[0]) # default value set
                '''
                for choice in new_choices:
                    
                    #drop['menu'].add_command(label=choice, command=(clicked,*choice))
                    drop['menu'].add_command(label=choice, command=lambda value=choice: clicked.set(choice))
                '''
            else:
                messagebox.showwarning("Message", "Ok, the operation has been stopped")
                
                
        except Exception as e:
            Info.insert(END, '\nWARNING! Exception ocurred:')
            messagebox.showerror(message='error: "{}"'.format(e))
            
    else:
        messagebox.showwarning("Message", "Please, select an URL")
                        
def changeURL(text):
    tmpURL=str(text)
    #print("test")
    serverURL.delete(0,END)
    serverURL.insert(0,tmpURL)
    #return

def check2():
    tmpDTS=str(clicked.get())
    if tmpDTS!='':
        #for myid in DTSid:
        
        # Reset var and delete all old options
        
    
        # Insert list of new options (tk._setit hooks them up to var)
        #new_choices.append(tmpDTS)
        try:
            #server = "https://data.obsea.es/erddap"
            e = ERDDAP(server=str(serverURL.get()))
            info_url = e.get_info_url(dataset_id=tmpDTS, response="csv")
            #print(info_url)
            info = pd.read_csv(info_url)
            info.head()
            dropVars['menu'].delete(0, 'end')
            dropSecondaryVars['menu'].delete(0, 'end')
            #print(info.head)
            #variables="".join(info.loc[info["Row Type"] == "variable", "Value"])
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
    #clicked = StringVar()
    else:
        messagebox.showwarning("Message", "Please, select a dataset")




# initial menu text

serverURLLabel=tkinter.Label(top, text='ServerURL (write it or use the menu)')
serverURLLabel.grid(row=0, column=0, sticky=W)
serverURL = Entry(top,width=25)
serverURL.grid(row=0, column=1, sticky=W)

URLoptions = [
    "https://data.obsea.es/erddap",
    "https://gliders.ioos.us/erddap",
    "https://erddap.emso.eu/erddap",
    "https://polarwatch.noaa.gov/erddap",
    "https://erddap.emodnet.eu/erddap",
    "https://erddap.emodnet-physics.eu/erddap",
    "http://oceano.bo.ingv.it/erddap",
    "https://salishsea.eos.ubc.ca/erddap",
    "https://coastwatch.noaa.gov/erddap",
    "https://nodc.ogs.it/erddap",
    "https://data.iadc.cnr.it/erddap",
    "https://opendap.co-ops.nos.noaa.gov/erddap"
]
# datatype of menu text
URLclicked = StringVar()
# Create Dropdown menu
URLdrop = OptionMenu( top , URLclicked , *URLoptions, command=changeURL)
URLdrop.config(width=25)
#drop.pack(padx=10, pady=10)
URLdrop.grid(row=0, column=2, sticky=W)




CheckAButton = Button(top, text="Check DATASETS",bg = "moccasin",width=25, command=(check))
CheckAButton.grid(row=1, column=0, sticky=W)

CheckBButton = Button(top, text="Check dataset's PARAMS",bg = "moccasin",width=25, command=(check2))
CheckBButton.grid(row=1, column=1, sticky=W)

CheckCButton = Button(top, text="Check DATA",bg = "moccasin", command=(check3))
CheckCButton.grid(row=1, column=2, sticky=W)

CheckDButton = Button(top, text="Plot DATA",bg = "moccasin", command=(plotData))
CheckDButton.grid(row=1, column=3, sticky=W)


CheckEButton = Button(top, text="DATA to XLSX",bg = "moccasin", command=(xlsexport))
CheckEButton.grid(row=2, column=3, sticky=W)
#tkinter.Button(top, text ="check", command = check).pack(padx=10, pady=10)
#tkinter.Button(top, text ="check2", command = check2).pack(padx=10, pady=10)
#tkinter.Button(top, text ="MyTest", command = check3).pack(padx=10, pady=10)

# Dropdown menu options
options = [
    ""
]
# datatype of menu text
clicked = StringVar()
# Create Dropdown menu
drop = OptionMenu( top , clicked , *options )
drop.config(width=25)
#drop.pack(padx=10, pady=10)
drop.grid(row=2, column=0, sticky=W)


# Dropdown menu options
optionsVars = [
    ""
]
# datatype of menu text
clickedVars = StringVar()
# Create Dropdown menu
dropVars = OptionMenu( top , clickedVars , *optionsVars )
dropVars.config(width=25)
#dropVars.pack(padx=10, pady=10)
dropVars.grid(row=2, column=1, sticky=W)



# Dropdown menu options
optionsSecondaryVars = [
    ""
]
# datatype of menu text
clickedSecondaryVars = StringVar()
# Create Dropdown menu
dropSecondaryVars = OptionMenu( top , clickedSecondaryVars , *optionsSecondaryVars )
dropSecondaryVars.config(width=25)
#dropVars.pack(padx=10, pady=10)
dropSecondaryVars.grid(row=2, column=2, sticky=W)

StartLabel=tkinter.Label(top, text='Start date')
StartLabel.grid(row=3, column=0, sticky=W)
calStart = DateEntry(top, width=25, background="black", disabledbackground="black", bordercolor="blue", 
               headersbackground="black", normalbackground="black", 
               normalforeground='white', headersforeground='white',
            foreground='white', borderwidth=2)
calStart.grid(row=4, column=0, sticky=W)

EndLabel=tkinter.Label(top, text='End date')
EndLabel.grid(row=3, column=1, sticky=W)
calEnd = DateEntry(top, width=25, background="black", disabledbackground="black", bordercolor="blue", 
               headersbackground="black", normalbackground="black", 
               normalforeground='white', headersforeground='white',
            foreground='white', borderwidth=2)
calEnd.grid(row=4, column=1, sticky=W)


#Info = Text(top, height=45, width=100)
Info = scrolledtext.ScrolledText(top, height=20, width=100)
Info.grid(row=5, column=0, columnspan=4, sticky=W)

top.mainloop()
