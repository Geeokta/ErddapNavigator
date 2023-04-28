# -*- coding: utf-8 -*-
'''
https://ioos.github.io/erddapy/01b-tabledap-output.html
'''
import tkinter
from tkinter import Tk, Label, Button, StringVar,OptionMenu
#Import erddap package into 
from erddapy import ERDDAP
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkcalendar import Calendar, DateEntry
import tkinter as tk

top = tkinter.Tk()
top.geometry('750x400')

def esegui():
    
    
    e = ERDDAP(
        server= "https://data.obsea.es/erddap",
        protocol="tabledap",
        response="csv",
    )
    
    e.dataset_id = str(clicked.get())
    myVar=str(clickedVars.get())
    e.variables = [
        "time",
        ""+myVar
    ]
    e.constraints = {
        "time>=": str(calStart.get_date())+"T00:00:00Z",
        "time<=": str(calEnd.get_date())+"T23:59:59Z",}
    
    
    # Print the URL - check
    url = e.get_download_url()
    print(url)
    
    # Convert URL to pandas dataframe
    df_MySite = e.to_pandas(  
        parse_dates=True,
    ).dropna()
    
    # print the dataframe to check what data is in there specifically. 
    print(df_MySite.head())
    
    print("Number of rows: "+str(len(df_MySite.index)))
    # print the column names
    print (df_MySite.columns)
    # make data
    
    #execute the plot (to decomment)
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

def check():
    #https://gliders.ioos.us/erddap
    
    server = "https://data.obsea.es/erddap"
    e = ERDDAP(server=server)
    
    kw = {
        "min_time": "2016-07-10T00:00:00Z",
        "max_time": "2017-02-10T00:00:00Z",
    }
    
    search_url = e.get_search_url(response="csv", **kw)
    search = pd.read_csv(search_url)
    DTSid = search["Dataset ID"].values
    
    DTSid_list = "\n".join(DTSid)
    print(f"Found {len(DTSid)} Datasets:\n{DTSid_list}")
    
    
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
def check2():
    tmpDTS=str(clicked.get())
    if tmpDTS!='':
        #for myid in DTSid:
        
        # Reset var and delete all old options
        
    
        # Insert list of new options (tk._setit hooks them up to var)
        #new_choices.append(tmpDTS)
        
        server = "https://data.obsea.es/erddap"
        e = ERDDAP(server=server)
        info_url = e.get_info_url(dataset_id=tmpDTS, response="csv")
        #print(info_url)
        info = pd.read_csv(info_url)
        info.head()
        #print(info.head)
        #variables="".join(info.loc[info["Row Type"] == "variable", "Value"])
        rslt_df = info[info['Row Type'] == "variable"]
        print(rslt_df['Variable Name'])
        for choiceVars in rslt_df['Variable Name']:
            print(choiceVars)
            dropVars['menu'].add_command(label=choiceVars, command=tk._setit(clickedVars, choiceVars))
    #clicked = StringVar()



# Dropdown menu options
options = [
    "MAMBO1_TS",
    "MAMBO2_TS",
    "MAMBO3_TS",
    "E2M3A_TS"
]
# datatype of menu text
clicked = StringVar()
# initial menu text
#clicked.set( "MAMBO1_TS" )


tkinter.Button(top, text ="check", command = check).pack(padx=10, pady=10)
tkinter.Button(top, text ="check2", command = check2).pack(padx=10, pady=10)
tkinter.Button(top, text ="MyTest", command = esegui).pack(padx=10, pady=10)

# Create Dropdown menu
drop = OptionMenu( top , clicked , *options )
drop.pack(padx=10, pady=10)


# Dropdown menu options
optionsVars = [
    ""
]
# datatype of menu text
clickedVars = StringVar()
# Create Dropdown menu
dropVars = OptionMenu( top , clickedVars , *optionsVars )
dropVars.pack(padx=10, pady=10)



tkinter.Label(top, text='Start date').pack(padx=10, pady=10)
calStart = DateEntry(top, width=12, background="black", disabledbackground="black", bordercolor="blue", 
               headersbackground="black", normalbackground="black", 
               normalforeground='white', headersforeground='white',
            foreground='white', borderwidth=2)
calStart.pack(padx=10, pady=10)

tkinter.Label(top, text='End date').pack(padx=10, pady=10)
calEnd = DateEntry(top, width=12, background="black", disabledbackground="black", bordercolor="blue", 
               headersbackground="black", normalbackground="black", 
               normalforeground='white', headersforeground='white',
            foreground='white', borderwidth=2)
calEnd.pack(padx=10, pady=10)

top.mainloop()
