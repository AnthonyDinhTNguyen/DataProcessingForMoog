import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from tkinter import messagebox
import os
import sys
from tkinter import *
 

#bounds checking for when the parameter is inches
def processInch(dataList):
    avg = dataList[4]
    high = dataList[3]
    low =  dataList[2]
    if((abs(float(avg)-float(high))>=.03)or (abs(float(avg)-float(low))>=.03)):
        return("FAILED")
    else:
        return("PASSED")

#bounds checking for when the parameter is degrees
def processDegrees(dataList,scalingDict):
    avg = float(dataList[4]) #avg value from results txt file
    high = float(dataList[3]) #max value
    low =  float(dataList[2]) #min value

    #get test name to get the scaling factor
    testParameterList = dataList[0].strip().split("/")
    testParameterID = testParameterList[-1].strip()

    #multiply by scaling factor and do the bounds checking
    if testParameterID in scalingDict:#get the scaling factor from the dictionary
        scalingFactor = float(scalingDict[testParameterID])
        #scale all of the values
        avgScaled = avg*scalingFactor
        highScaled = high*scalingFactor
        lowScaled = low*scalingFactor

        #bounds checking 
        if((abs(avgScaled-highScaled)>=.03)or(abs(avgScaled-lowScaled)>=.03)):#check bounds with scaled values
            return("FAILED")
        else:
            return("PASSED")
    return("N/A")
        

#parse excel file and add scaling factors to a dictionary mapped to the test name
def createScalingDict(scalingPath):
    df = pd.read_excel(scalingPath)
    tempDict={}
    scale = df['Scaling']
    parameterNames = df['SSW Parameter Names (Columns)']
    for i in range(len(scale)):
        if(scale[i]!='None'):
            parameterPath=parameterNames[i].strip().split("/")
            testName = parameterPath[-1].split('[')[0].strip()
            tempDict[testName] = scale[i]
    return tempDict

#write the results, formatted, to the output file
def formatOutput(result, dataList,outputFile):
    outputFile.write("%s %s\t%s\t%s\t%s\t%s\n" %(dataList[0],dataList[1],dataList[2],dataList[3],dataList[4],result))
    
#Process all results files under a directory
def processFromDirectory():   
    #open and set up input and output files
    window.destroy() #get rid of selection window
    root = tk.Tk()
    root.withdraw()
    #get the results text file to process
    #messagebox.showinfo("Instructions","On the next window, select the ROOT DIRECTORY")
    directoryPath= filedialog.askdirectory(title = "Please Select the DIRECTORY to process")
    #get the parameters excel file for the scaling factor
    #messagebox.showinfo("Instructions","On the next window, select the PARAMETERS EXCEL FILE with Scaling Factors")
    scalingPath = filedialog.askopenfilename(title = "Please Select the PARAMETERS EXCEL FILE with Scaling Factors")
    #scalingPath="C:/Users/anguyen4/DataProcessing/E175_Parameters_for_Data_Processing_DE_20190412.xlsx"
    scalingDict=createScalingDict(scalingPath)
    for root, dirs, files in os.walk(directoryPath):
        for name in files:
            '''if "revised" in name:
                try:
                    deleteMe = os.path.join(root,name)
                    os.remove(deleteMe)
                except OSError as e:
                    print("Failed with:", e.strerror)'''
            if ".txt" in name and "revised" not in name:
                dataStart = 0;
                fileToProcess=os.path.join(root, name)
                outputName = "revised_"+name
                outputPath = os.path.join(root, outputName)
                f = open(fileToProcess)
                outputFile = open(outputPath, "w")
                for l in f.readlines():
                    dataList = l.strip().split()
                    if(len(dataList)>0and(dataList[0] == '________________RFM')):
                        dataStart = 1;
                        outputFile.write(l+"\n")
                        continue                    
                    if(len(dataList)!=6):#hacky workaround to the insufficient data output
                        outputFile.write(l+"\n")
                        continue
                    if(dataStart ==0):
                        outputFile.write(l+"\n")
                    if(dataStart ==1):
                        if(len(dataList)==6):
                            result = dataList[5]
                            #process the inches tests
                            if(dataList[1] == '[INCH]'):
                                result = processInch(dataList)
                        #process the degrees tests
                            elif(dataList[1] =='[DEGREES]'):
                                result = processDegrees(dataList,scalingDict)
                            formatOutput(result,dataList,outputFile)
                            
                f.close()
                outputFile.close()
    messagebox.showinfo("Information","Finished")

def processSingleFile():   
    #open and set up input and output files
    window.destroy() #get rid of selection window
    root = tk.Tk()
    root.withdraw()
    #get the results text file to process
    #messagebox.showinfo("Instructions","On the next window, select the ROOT DIRECTORY")
    file_path= filedialog.askopenfilename(title = "Please Select the RESULTS TEXT FILE to process")
    file_name = file_path.strip().split("/")[-1].split(".")[0]
    #get the parameters excel file for the scaling factor
    #messagebox.showinfo("Instructions","On the next window, select the PARAMETERS EXCEL FILE with Scaling Factors")
    scalingPath = filedialog.askopenfilename(title = "Please Select the PARAMETERS EXCEL FILE with Scaling Factors")
    scalingDict=createScalingDict(scalingPath)
    s = "/"
    outputPath=s.join(file_path.strip().split("/")[:-1])
    outputFile = open(outputPath+"/revised_"+file_name+".txt", "w")
    f = open(file_path)
    dataStart = 0;
    #start reading in data and processing it
    for l in f.readlines():
        dataList = l.strip().split()
        if(len(dataList)>0and(dataList[0] == '________________RFM')):
            dataStart = 1;
            outputFile.write(l+"\n")
            continue        
        if(len(dataList)!=6):#hacky workaround to the insufficient data output
            outputFile.write(l+"\n")
            continue
        if(dataStart ==0):
            outputFile.write(l+"\n")
        if(dataStart ==1):
            if(len(dataList)==6):
                result = dataList[5]
                #process the inches tests
                if(dataList[1] == '[INCH]'):
                    result = processInch(dataList)
                #process the degrees tests
                elif(dataList[1] =='[DEGREES]'):
                    result = processDegrees(dataList,scalingDict)
                formatOutput(result,dataList,outputFile)
                
    f.close()
    outputFile.close()
    messagebox.showinfo("Information","Finished")


window = Tk()
window.title("Select if you want to process a single file or an entire directory")
window.geometry('350x200')  
btn = Button(window, text="Select a Single File to Process", command=processSingleFile)
btn.grid(column=0, row=0)
btn2 = Button(window, text="Select a Directory to Process", command=processFromDirectory)
btn2.grid(column = 0, row = 1)

