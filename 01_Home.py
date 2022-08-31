import gc
import os
import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from datetime import datetime

PAGE_CONFIG = {"page_title": "IRAP Data Revision",
               "page_icon": "chart_with_upwards_trend", "layout": "wide"}

st.set_page_config(**PAGE_CONFIG)


st.title("Revision Data")

FOLDER = ['IRAP_PUBLIC_AD','IRAP_PUBLIC_CN','IRAP_PUBLIC_EM','IRAP_PUBLIC_EU','IRAP_PUBLIC_IN','IRAP_PUBLIC_NA']

option = st.sidebar.selectbox("Region Selection", FOLDER)

# path = r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result'
# pdInput = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/IRAP_PUBLIC_NA/PD_Input/PD_Input_ready.csv')
# df = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/IRAP_PUBLIC_NA/PD_Individual/PD_Individual_ready.csv')
# mdf = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/IRAP_PUBLIC_NA/MDF_Individual/MDF_Individual_ready.csv')
companyInfo = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/PD_Model/IRAP_CompanyInfo.csv')
unitLink = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/PD_Model/unit_sector_region_link.csv')


@st.cache
def get_data(options=option):
    pdInput = pd.read_csv(f'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/{options}/PD_Input/PD_Input_ready.csv')
    pdInput = pd.merge(pdInput, companyInfo, on='CompanyCode', how='left')
    pdInd = pd.read_csv(f'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/{options}/PD_Individual/PD_Individual_ready.csv')
    pdInd = pd.merge(pdInd, companyInfo, on='CompanyCode', how='left')
    mdf = pd.read_csv(f'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/{options}/MDF_Individual/MDF_Individual_ready.csv')
    gc.collect()
    return pdInput, pdInd, mdf

pdInput, pdInd, mdf = get_data()

companyCode = pdInd['CompanyName'].drop_duplicates().to_list()
companyCodeoption = st.sidebar.selectbox("Company Code", companyCode)

pdInputList = pdInput['RFID'].drop_duplicates().to_list()
pdInputListoption = st.sidebar.selectbox("Risk Factor", pdInputList, index=9)

button = st.sidebar.button("Validated")

if button:
    path = r"E:\instances\Irap_refersh_code\Data_Revision\data_revision\Result"
    df = pd.DataFrame(list())
    df.to_csv(os.path.join(path, 'starting.csv'), index=False)
    st.sidebar.write("Status trigger file is generated")


pdInputFiltered = pdInput.loc[(pdInput['CompanyName'] == companyCodeoption) & (pdInput['RFID'] == pdInputListoption)]
pdInputFiltered = pdInputFiltered[['CompanyCode', 'DataDate', 'RFID', 'RFValue', 'RFPercentile']]


@st.cache
def data_filter_process(dataframe, options=companyCodeoption):
    filteredPD = dataframe.loc[dataframe['CompanyName'] == options]
    filteredPD = filteredPD.loc[filteredPD['Horizon'] == '12M']
    filteredPD['PD'] = filteredPD['PD'] * 10000
    filteredPD = filteredPD[['CompanyCode', 'DataDate', 'Horizon', 'ForwardPoint', 'PD', 'AnnPD', 'UnconPD', 'AnnUnconPD']]
    filteredPD['DataDate'] =  pd.to_datetime(filteredPD['DataDate'])
    
    return filteredPD


filteredPD = data_filter_process(pdInd)


# Plot
pdPlot = alt.Chart(filteredPD).mark_line(point=alt.OverlayMarkDef(color="blue")).encode(
    x=alt.X('DataDate', axis=alt.Axis(title="", ticks=False, domain=False)),
    y = alt.Y('PD', axis=alt.Axis(title='PD Individual')),
    tooltip=['DataDate', 'PD']
).configure_axis(
    grid=False
).properties(title = companyCodeoption).interactive()

st.header("Max PD Input by company")

pdInput = pdInput.loc[pdInput['RFID'] == 'SIZE_LEVEL']
maxPDInput = pdInput.sort_values('DataDate').groupby('CompanyCode').last().reset_index()


st.table(maxPDInput[['CompanyCode','CompanyName','DataDate', 'RFValue']].sort_values('RFValue', ascending=False))

st.altair_chart(pdPlot, use_container_width=True)


# Dataframe
st.header("PD Input")
st.table(pdInputFiltered)


