import tkinter as tk
from tkinter import filedialog

def processInch(dataList):
    avg = dataList[4]
    high = dataList[3]
    low =  dataList[2]
    if((abs(float(avg)-float(high))>=.03)or (abs(float(avg)-float(low))>=.03)):
        return("FAILED")
    else:
        return("PASSED")
def processDegrees(dataList):
    avg = dataList[4]
    high = dataList[3]
    low =  dataList[2]
    testParameterList = dataList[0].strip().split("/")
    testParameterID = testParameterList[-1] #last element
    #read from excel, do same split, compare last elements, get scaling factor
    #multiply scaling factro, then do same as above
    
    
    
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
f = open(file_path)
dataStart = 0;
for l in f.readlines():
    dataList = l.strip().split()
    if(len(dataList)>0and(dataList[0] == '________________RFM')):
        dataStart = 1;
        continue
    if(dataStart ==1):
        result = "N/A"
        if(dataList[1] == '[INCH]'):
            result = processInch(dataList)
        elif(dataList[1] =='[DEGREES]'):
            result = processDegrees(dataList)
        print(result)
            
f.close()
