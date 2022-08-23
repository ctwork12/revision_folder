import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data
import plotly.express as px
import gc

PAGE_CONFIG = {"page_title": "IRAP Data Revision",
               "page_icon": "chart_with_upwards_trend", "layout": "centered"}

st.set_page_config(**PAGE_CONFIG)


st.title("Revision Plot")

FOLDER = ['IRAP_PUBLIC_AD','IRAP_PUBLIC_CN','IRAP_PUBLIC_EM','IRAP_PUBLIC_EU','IRAP_PUBLIC_IN','IRAP_PUBLIC_NA']

option = st.sidebar.selectbox("Database Selection", FOLDER)

# path = r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result'
# pdInput = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/IRAP_PUBLIC_NA/PD_Input/PD_Input_ready.csv')
# df = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/IRAP_PUBLIC_NA/PD_Individual/PD_Individual_ready.csv')
# mdf = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/IRAP_PUBLIC_NA/MDF_Individual/MDF_Individual_ready.csv')
companyInfo = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/PD_Model/IRAP_CompanyInfo.csv')
unitLink = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/PD_Model/unit_sector_region_link.csv')


@st.cache
def get_data(options=option):
    pdInput = pd.read_csv(f'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/{options}/PD_Input/PD_Input_ready.csv')
    pdInd = pd.read_csv(f'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/{options}/PD_Individual/PD_Individual_ready.csv')
    mdf = pd.read_csv(f'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/{options}/MDF_Individual/MDF_Individual_ready.csv')
    gc.collect()
    return pdInput, pdInd, mdf

pdInput, pdInd, mdf = get_data()

companyCode = pdInd['CompanyCode'].drop_duplicates().to_list()
companyCodeoption = st.sidebar.selectbox("Company Code", companyCode)

pdInputList = pdInput['RFID'].drop_duplicates().to_list()
pdInputListoption = st.sidebar.selectbox("Risk Factor", pdInputList, index=9)

pdInputFiltered = pdInput.loc[(pdInput['CompanyCode'] == companyCodeoption) & (pdInput['RFID'] == pdInputListoption)]
pdInputFiltered = pdInputFiltered[['CompanyCode', 'DataDate', 'RFID', 'RFValue', 'RFPercentile']]

filteredPD = pdInd.loc[pdInd['CompanyCode'] == companyCodeoption]
filteredPD = filteredPD.loc[filteredPD['Horizon'] == '12M']
filteredPD['PD'] = filteredPD['PD'] * 10000
filteredPD = filteredPD[['CompanyCode', 'DataDate', 'Horizon', 'ForwardPoint', 'PD', 'AnnPD', 'UnconPD', 'AnnUnconPD']]
filteredPD['DataDate'] =  pd.to_datetime(filteredPD['DataDate'])

pdPlot = alt.Chart(filteredPD).mark_line(point=alt.OverlayMarkDef(color="blue")).encode(
    x = 'DataDate',
    y = 'PD',
    tooltip=['DataDate', 'PD']
).configure_axis(
    grid=False
).properties(title = companyCodeoption).interactive()

st.dataframe(pdInputFiltered)
st.dataframe(filteredPD)
st.altair_chart(pdPlot, use_container_width=True)
#st.dataframe(mdf)

# display = ("male", "female")

# options = list(range(len(display)))

# value = st.sidebar.selectbox("gender", options, format_func=lambda x: display[x])

# st.write(value)


@st.cache
def data_filter_process(options=companyCodeoption):
    pass


# for i in df['CompanyCode'].drop_duplicates():
#     pdInputCopy = pdInput.copy()
    
#     pdInputCopy = pdInputCopy.loc[(pdInputCopy['CompanyCode'] == i) & (pdInputCopy['RFID'] == "SIZE_LEVEL")]
#     pdInputCopy = pdInputCopy.loc[pdInputCopy['DataDate'] == pdInputCopy['DataDate'].max()]


#     filteredPD = df.loc[df['CompanyCode'] == i]
#     filteredPD = filteredPD.loc[filteredPD['Horizon'] == '12M']
#     filteredPD['PD'] = filteredPD['PD'] * 10000
#     regionIndustry = pd.merge(filteredPD, unitLink, on='CompanyCode', how='left')
#     companyName = pd.merge(regionIndustry, companyInfo, on='CompanyCode', how='left')
#     sizeMerge = pd.merge(companyName, pdInputCopy, on='CompanyCode', how='left')
#     title = sizeMerge[['CompanyName']].drop_duplicates()
#     subtitle = sizeMerge['IndustryName'].drop_duplicates().to_string(header=False,index=False) + '_' +  sizeMerge['RegionName'].drop_duplicates().to_string(header=False,index=False) + '_' + sizeMerge['RFValue'].drop_duplicates().to_string(header=False,index=False)
#     # fig = plt.figure(figsize=[16,12])
#     # fig.patch.set_facecolor('white')
#     # #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
#     # #plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
#     # plt.xticks(rotation = 45)
#     # plt.title(title.to_string(header=False,index=False))
#     # plt.suptitle(subtitle)
#     # plt.plot(filteredPD['DataDate'], filteredPD['PD'])
#     # plt.savefig(os.path.join(path, i))
#     # plt.clf()







df = pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.altair_chart(c, use_container_width=True)


x = np.arange(100)
source = pd.DataFrame({
  'x': x,
  'f(x)': np.sin(x / 5)
})

d = alt.Chart(source).mark_line().encode(
    x='x',
    y='f(x)'
)

st.altair_chart(d, use_container_width=True)


temps = data.seattle_temps()


temps = temps[temps.date < '2010-01-15']

e = alt.Chart(temps).mark_line().encode(
    x='date:T',
    y='temp:Q'
)


st.altair_chart(e, use_container_width=True)


a = alt.Chart(temps).mark_rect().encode(
    alt.X('hoursminutes(date):O', title='hour of day'),
    alt.Y('monthdate(date):O', title='date'),
    alt.Color('temp:Q', title='temperature (F)')
)

st.altair_chart(a, use_container_width=True)
