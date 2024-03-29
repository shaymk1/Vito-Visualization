
from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import  nightsignal as ns
import json
import csv
import datetime
import os
from playsound import playsound
import requests
def compare():
    
    st.header("Add Your File")

    HRFile = st.file_uploader("Upload Heartrate Data", type=("csv"))

    #StepFile = st.file_uploader("Upload Step Data", type=("csv"))

    HRFileName = ""
    RiskFileName = ""
    #RiskFile = st.file_uploader("Upload Risk Data", type=("csv"))

    def processData(HRFile, RiskFile):
        df = pd.read_csv(HRFile)
        df.to_csv("/tmp/tmp.csv")
        count = df.shape[0]
        devices = []
        for i in range(count):
            devices.append("HK Apple Watch")
        df.insert(0, "Device", devices, True)
    
        df2 = DataFrame()
        i = 0
        steps = []
        start_time = []
        end_time = []
        end_date = []
        start_date = []
        for i in range(count):
            
            row = df.iloc[i]
            
            start = datetime.datetime.strptime( row.Start_Time, '%H:%M:%S' )
            endTime = start + datetime.timedelta(minutes=30)
            start = start - datetime.timedelta(minutes=30)
            
                        
            end = datetime.datetime.strptime(endTime.strftime("%H:%M:%S"), '%H:%M:%S' )
            start_time.append(start.strftime("%H:%M:%S"))
            end_time.append(endTime.strftime("%H:%M:%S"))
            steps.append(0)
            start_date.append(row.Start_Date)
            end_date.append(row.Start_Date)

            i += 1
            
        df2.insert(0, "Steps", steps, True)
        df2.insert(0, "Start_Date", start_date, True)
        df2.insert(0, "Start_Time", start_time, True)
        df2.insert(0, "End_Date", start_date, True)
        df2.insert(0, "End_Time", end_time, True)
        df2.to_csv("/tmp/tmp2.csv")
        
        ns.getScore("/tmp/tmp.csv", "/tmp/tmp2.csv")

        

        
        f = open('/tmp/NS-signals.json',)
    
    # returns JSON object as
    # a dictionary
        data = json.load(f)
        
        #st.write(data)
        alerts = data['nightsignal']
        if RiskFile is not None:
            alertVals = []
            allAlertVals = []
            allDates = []
            for item in alerts:
                #st.write(item["val"])
                allAlertVals.append(item["val"])
                allDates.append(item["date"])
                if int(item["val"]) > 0:
                    
                    alertVals.append(item["val"])
        
            nsAlertCount = len(alertVals)
            df = pd.read_csv(RiskFile)
            vitoAlertCount = len(df[df['Risk'] == 1])
            
            # st.write(nsAlertCount)
            # st.write(vitoAlertCount)
            col1, col2 = st.columns(2)
            col1.subheader("Vito Alerts: " + str(vitoAlertCount)) 
            col2.subheader("NightSignal Alerts: " + str(nsAlertCount)) 
            if nsAlertCount == vitoAlertCount:
                st.balloons()
                st.success("ALGORITHMS MATCH!!!!!!!!")
                #playsound("success.mp4")
            else:
                st.error("No Match")

        col1, col2 = st.columns(2)

        df = DataFrame()
        df.insert(0, "Date", allDates, True)
        df.insert(0, "Value", allAlertVals, True)
        col1.bar_chart(df.set_index('Value'))
            
    
        col2.table(alerts)

    def file_selector(folder_path='.', type="Heartrate"):
        filenames = os.listdir(folder_path)
        csvFiles = []
        for file in filenames:
            if "csv" in file:
                csvFiles.append(file)
        selected_filename = st.selectbox('Select ' + type, csvFiles)
        return os.path.join.join(folder_path, selected_filename)


    if HRFile is None:
        st.header("Or Select A File")
        HRFileName = file_selector(type="Health")
        st.write('HR File `%s`' % HRFileName)
        if RiskFileName:
            processData(HRFileName, RiskFileName)
            
  



        


    r = requests.get('https://api.github.com/user').json()            
    f = open('/tmp/RiskFile.txt',)
    if HRFile and f:
        f.write(r)
        processData(HRFile, f)