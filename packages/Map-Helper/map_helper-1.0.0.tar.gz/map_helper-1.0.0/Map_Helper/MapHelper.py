#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import all the necessary libraries. Note Haversine, Selenium
from win32com.client import Dispatch, GetActiveObject
import pythoncom
import os
from random import randrange

import pandas as pd
import haversine as hs
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from haversine import Unit

import simplekml

#import the libraries for opening and saving the FIRMette
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib
import fitz


# In[2]:


#Create function to calculate distances for later on
dist_list = []
def distance(center, coords):
    dist_list.clear()
    for i in coords:
        result = hs.haversine(center,i,unit=Unit.FEET)
        dist_list.append(result)
    
    return dist_list


# In[3]:


#Create site names for DDD, store in Dataframe imported from excel doc for now
def dataRetriever():
    getFile = input(r'Paste path to excel Input file, or press Return to open one:')
    xl = Dispatch("Excel.Application")
    xl.DisplayAlerts = False
    if getFile =="":
        xl.Visible = True
        headers = ['Site','Latitude, Start','Longitude, Start','Latitude, End','Longitude, End']   
        getFile = os.getcwd() + '\Input.xlsx'
        wb = xl.Workbooks.Add()
        sheet = xl.Worksheets(1)
        sheet.Range(sheet.Cells(1,1), sheet.Cells(1,len(headers))).Value = headers
        wb.SaveAs(getFile)
        while (True):
            try:
                xl = GetActiveObject('Excel.Application')
                wb = xl.Workbooks('Input.xlsx')
            except AttributeError:
                pass
            except pythoncom.com_error as e:
                x = getattr(e, 'message', str(e))
                if "Exception occurred." in x:
                    break
                else:
                    pass
    else:
        xl.Visible = False
        wb = xl.Workbooks.Open(getFile)
        xl.Close()
    return getFile


# In[4]:


def sortData(getFile):
    df = pd.read_excel(getFile)
    df['SiteName'] = ""
    
    df.loc[pd.isnull(df.loc[:, 'Latitude, End']), 'SiteName'] = 'Site ' + df['Site'].astype(str) + " (" + round(df['Latitude, Start'], 6).astype(str) + ',' + round(df['Longitude, Start'], 6).astype(str) + ')'
    df.loc[pd.notnull(df.loc[:, 'Latitude, End']), 'SiteName'] = 'Site ' + df['Site'].astype(str) + ' (Start: ' + round(df['Latitude, Start'], 6).astype(str) + ',' + round(df['Longitude, Start'], 6).astype(str) + "; End: " + round(df['Latitude, End'], 6).astype(str) + ',' + round(df['Longitude, End'], 6).astype(str) + ')'
    
    df2 = pd.DataFrame(columns=['Name','nameShort','Latitude','Longitude','Icon','Folder'])
    #Iterates through rows of excel doc and converts information into things usable by Pandas, Earthpoint
    for index, row in df.iterrows():
        #Place coordinates into dataframe
        latitudeS = str(round(row['Latitude, Start'], 6))
        longitudeS = str(round(row['Longitude, Start'],6))
        latitudeE = str(round(row['Latitude, End'],6))
        longitudeE = str(round(row['Longitude, End'],6))
        
        #Divides into start and end points, if applicable.
        if pd.notnull(row.loc['Latitude, End']):
            nameShort = 'Site ' + str(row['Site']) + ", Start" 
            name = nameShort + " (" + latitudeS + ',' + longitudeS + ')'
            name2Short = 'Site ' + str(row['Site']) + ", End"
            name2 = name2Short + " (" + latitudeE + ',' + longitudeE + ')'
            df3  = pd.DataFrame([[name, nameShort, latitudeS, longitudeS]],
                                columns = ['Name','nameShort','Latitude','Longitude'])
            df4  = pd.DataFrame([[name2, name2Short, latitudeE, longitudeE]],
                                columns = ['Name','nameShort','Latitude','Longitude'])
            df2 = pd.concat([df2,df3], sort=False)
            df2 = pd.concat([df2,df4], sort=False)
        else: 
            nameShort = 'Site ' + str(row['Site']) 
            name = nameShort + " (" + latitudeS + ',' + longitudeS + ')'
            
            df3  = pd.DataFrame([[name, nameShort, latitudeS, longitudeS]],
                                columns = ['Name', 'nameShort','Latitude','Longitude'])
            df2 = pd.concat([df2,df3], sort=False)
            
    #converts strings into floats, resets df2 index
    df2['Latitude'] = pd.to_numeric(df2['Latitude'], downcast ="float")
    df2['Longitude'] = pd.to_numeric(df2['Longitude'], downcast ="float")
    df2 = df2.reset_index(drop=True)
    #creates coords lists for distance function
    coords = df2[['Latitude','Longitude']]
    coords = list(coords.itertuples(index=False, name=None))
    
    #finds centerpoint of group
    x = df2['Latitude'].mean()
    y = df2['Longitude'].mean()
    center1=(x,y)
    #creates dataframe for centerpoints, adds centerpoint
    dfc = pd.DataFrame([[x, y]],
                       columns = ['Latitude','Longitude'])
    #creates dataframe to store distances from centerpoints
    dfd = pd.DataFrame()
    #runs centerpoint through distance function, returns results to above dfd dataframe
    dfd['Distance1'] = distance(center1, coords)
    #distance column added to df2 to record minimun distance to centerpoint
    df2['Distance'] = dfd['Distance1']
    #folder column added to group points to nearest centerpoints
    df2['Folder'] = 'Group 1'
    dfc['Folder'] = 'Group 1'
    
    i = 1
    while (df2['Distance'] > 1500).any():
    
        #Drop out temp center points that are already in groups
        dfx = df2['Distance'] < 1500
        indices = []
        dfd2 = pd.DataFrame()
        for q in range(len(dfx)):
            if dfx[q] == True:
                indices.append(q)
        dfd2 = dfd.drop(indices) 
        #Sum and find average distance of points from centers
        dfd2['sum'] = dfd2.sum(axis=1)
        dfd2['avg'] = dfd2['sum']/(i)
        #load point that is farthest avg distance from centers
        x = df2.iloc[dfd2['avg'].idxmax(), 2]
        y = df2.iloc[dfd2['avg'].idxmax(), 3]
        tempCenter = (x,y)
        #add row to column using loaded point as temporary center for distances
        dist2 = 'Distance' + str(i+1)
        dfd[dist2] = distance(tempCenter, coords)
        #sort into groups based on distances
        df2['Folder'] = dfd.idxmin(axis = 1)
        #reset center dataframe
        dfc = pd.DataFrame()
        dfc['Latitude'] = df2.groupby('Folder')['Latitude'].mean()
        dfc['Longitude'] = df2.groupby('Folder')['Longitude'].mean()
        #reset dfd dataframe for next run
        dfd = pd.DataFrame()
        #recalculate distances from new centerpoints
        for index, row in dfc.iterrows():
            x2 = row['Latitude']
            y2 = row['Longitude']
            center2 = (x2,y2)
            dfd[index] = distance(center2, coords)
        #reload into df2, re-check if it fits into maps
        df2['Distance'] = dfd.min(axis = 1)
        i+= 1
        
    df2['Folder'] = df2['Folder'].replace({'Distance' : 'Group '},regex=True)
    
    #gives groups unique pin colors, unless there is more than 10
    
    
    df2 = df2.drop(columns=['Distance'])
    dfddd = pd.DataFrame(df['SiteName'])
    dfc = dfc.reset_index()
    try:
        dfc['Folder'] = dfc['Folder'].replace({'Distance' : 'Group '},regex=True)
    except KeyError:
        raise Warning('Please enter data into Input file and restart')
        
    return dfddd, df2, dfc


# In[5]:


def printTheMasks(df2, dfc):
    labelmaker = input('Add labels to FIRMette masks? (y/n)')
    applic = input('Applicant Name: ')
    woNum = 'WO#' + input('WO#00000: ')
    diNum = 'DI#' + input('DI#0000000: ')
    drNum = 'DR' + input('DR0000: ')
    stCo = '-' + input('State Abr, XX: ')
    for i, row in dfc.iterrows():
        #loads points for each group, and grabs the center point.
        group = row['Folder']
        xs = list(df2.loc[df2['Folder']==group,'Latitude'])
        ys = list(df2.loc[df2['Folder']==group,'Longitude'])
        xcen = float(dfc.loc[i,'Latitude']) #literally just use row['Latitude'], dumb ass
        ycen = float(dfc.loc[i,'Longitude']) #same
        xs.append(xcen)
        ys.append(ycen)
        #setting the dimensions for the eventual plot. This was a stupid way to do this probs, but it works.
        yx = ycen-.00475
        yr = ycen+.00475
        xx = xcen-.00373
        xr = xcen+.00373
        
        #I don't understand how GPS coordinates map to Euclidean plains, and at this point it's too late to learn
        #I know x/y are backwards, and have been this whole time, but I didn't realize until here. It's easier this way.
        #But generally, this maps the points to a scatter plot and gets the plot formatted
        fig, ax = plt.subplots()
        ax.scatter(ys,xs)
        ax.set_xlim((yx,yr))
        ax.set_ylim((xx,xr))
        x0,x1 = ax.get_xlim()
        y0,y1 = ax.get_ylim()
        ax.set_aspect(abs(x0-x1)/abs(y0-y1))
        ax.scatter(ys,xs, c = 'red')
        plt.axis('off')
        
        #Creates labels for the FIRMette, if y was selected above.
        if labelmaker == 'y':
            textstr = '\n'.join((woNum,diNum))
            
            Title1 = plt.text(.01,.99,applic, fontsize=14, ha='left', va='top', transform=ax.transAxes)
            renderer1 = plt.gcf().canvas.get_renderer()
            text_bbox1 = Title1.get_window_extent(renderer1)
            text_bbox1 = text_bbox1.transformed(ax.transAxes.inverted())
            dx = .01 + (text_bbox1.width * .6)
            height1 = text_bbox1.height
            
            Title2 = plt.text(.008,.95,textstr, fontsize=11, ha='left', va='top', transform=ax.transAxes)
            text_bbox2 = Title2.get_window_extent(renderer1)
            text_bbox2 = text_bbox2.transformed(ax.transAxes.inverted())
            xmin = text_bbox2.xmin-.01
            ymin = text_bbox2.ymin
            height2 = text_bbox2.height
            dy = height1 + height2
            
            rect = Rectangle((xmin,.9), dx, .1, fc='white', ec='black', transform=ax.transAxes)
            ax.add_patch(rect)
            
            #Works~But not quite the way I want it to
            n = list(df2.loc[df2['Folder']==group,'Name'])
            for i, txt in enumerate(n):
                ax.annotate(txt, (ys[i],xs[i]), 
                            xytext=(30,30), textcoords ='offset points',
                            bbox=dict(boxstyle='square', fc='w', ec='red'),
                            arrowprops = dict(arrowstyle='wedge',relpos=(0.,0.),connectionstyle='arc3',fc='tab:red',ec='tab:red'))
                
        #print masks to the same folder
        fig.set_size_inches(13,11.5)
        fig.savefig(group,bbox_inches='tight',pad_inches=0,transparent=True)
        plt.close(fig)
    finalName = drNum + stCo + ' - ' + applic + ' - ' + woNum + ' - '+ diNum + ' - FIRMette.pdf'
    return finalName


# In[6]:


def printTheMaps(dfc,fileName):
    #printmaker = input('Print FIRMette PDFs? (y/n)')
    #if printmaker == 'y':
        fileList = []
        for i, row in dfc.iterrows():
            #Use Selenium to initiate an Edge browser and download corresponding FIRMette
            driver = webdriver.Edge()
            url = 'https://msc.fema.gov/portal/firmette?latitude='+str(round(row['Latitude'], 7))+'&longitude='+str(round(row['Longitude'], 7))
            try:
                driver.get(url)
                WebDriverWait(driver, 10)
                WebDriverWait(driver, 90).until(lambda driver: driver.current_url != url)
            except TimeoutException as ex:
                print('No map found for (lat,lon)' + str(round(row['Latitude'], 7)) + ',' + str(round(row['Longitude'], 7)))
                pass
                
            if driver.current_url.endswith('.pdf'):
                    pdf_url = driver.current_url
                    driver.get(pdf_url)
                    group = row['Folder']
                    name = group + '.pdf'
                    urllib.request.urlretrieve(pdf_url, name)
                    
                    maskName = group + '.png'
                    img = fitz.Pixmap(maskName)
                    height = 570 - (img.height * .5763)
                    width = 33 + (img.width * .5763)
                    image_rectangle = fitz.Rect(33,height,width,570)
            
                    file_handle = fitz.open(name)
                    first_page = file_handle[0]
                    first_page.wrap_contents()
            
                    first_page.insert_image(image_rectangle, keep_proportion=True, filename=maskName)

                    appName = 'Applied_' + name
                    file_handle.save(appName, deflate=True)
                    fileList.append(appName)
                    file_handle.close()
            driver.close()
                
        doc = fitz.open()
        for files in fileList:
            doc.insert_file(files)
            os.remove(files)
        doc.save(fileName)
        doc.close()


# In[25]:


def printTheEarth(df,fileName):
    kml = simplekml.Kml()
    pins = input('Color solid, random, or by FIRM? ')
    long = input('Lat/Lon in label (y/n)? ')
    colors = ['ff00ffff','ff000080','ffffffff','ff60a4f4','ff808000','ff0000ff',
              'ff00a5ff','ff00ff00','ff008000','ffffff00','ffff0000','ff800080','ff000000',
              'ffff00ff','ff808080','ff008080','ffb9daff','fffae6e6','ffcbc0ff','ff800000']
    for grp, sub in df.groupby('Folder'):
        fol = kml.newfolder(name=grp)
        for i, row in sub.iterrows():
            if long == 'y':
                pnt = fol.newpoint(name=row['Name'], coords=[(row['Longitude'],row['Latitude'])])
            else: 
                pnt = fol.newpoint(name=row['nameShort'], coords=[(row['Longitude'],row['Latitude'])])
            
            pnt.style.iconstyle.icon.href = 'https://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png'
            if pins == 'random' or pins == 'r':
                pnt.style.iconstyle.color = colors[(i%20)]
            elif pins == 'FIRM' or pins == 'f':
                num = int(grp[6:])-1
                pnt.style.iconstyle.color = colors[(num%20)]
            else:
                pnt.style.iconstyle.color = simplekml.Color.yellow
            
    kml.save(fileName)


# In[8]:


def Printer(dataf):
    fileName = input('Unique file name?')
    if 'SiteName' in dataf.columns:
        if fileName == '':
            fileName = 'DDD_Names.xlsx'
        else:
            fileName = fileName + '.xlsx'
        dataf.to_excel(fileName)
    elif 'Name' in dataf.columns:
        if fileName == '':
            fileName = 'Earth.kml'
        else:
            fileName = fileName + '.kml'
        printTheEarth(dataf,fileName)


# In[9]:


def main():
    Data = dataRetriever()
    DDD, KML, Centers = sortData(Data)
    printOut = input('Print: DDD, KML, FIRM? ')
    while (True):
        try:
            if printOut == 'DDD' or printOut == 'd':
                Printer(DDD)
            elif printOut == 'KML' or printOut == 'k':
                Printer(KML)
            elif printOut == 'FIRM' or printOut == 'f':
                fileName = printTheMasks(KML, Centers)
                printTheMaps(Centers, fileName)
            elif printOut == 'QUIT' or printOut == 'q':
                try:
                    os.remove('Input.xlsx')
                except:
                    pass
                break
            else:
                raise Exception
            printOut = input("Print again: DDD, KML, FIRM? ")
            pass
        
        except:
            printOut = input('Please enter a valid print: DDD, KML, FIRM? ')
            pass


# In[24]:


if __name__ == "__main__":
    main()


# In[ ]:




