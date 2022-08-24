import gc

import altair as alt
import pandas as pd
import streamlit as st

PAGE_CONFIG = {"page_title": "IRAP Data Revision",
               "page_icon": "chart_with_upwards_trend", "layout": "centered"}

st.set_page_config(**PAGE_CONFIG)


st.title("MDF Plot")

FOLDER = ['IRAP_PUBLIC_AD','IRAP_PUBLIC_CN','IRAP_PUBLIC_EM','IRAP_PUBLIC_EU','IRAP_PUBLIC_IN','IRAP_PUBLIC_NA']

option = st.sidebar.selectbox("Database Selection", FOLDER)

companyInfo = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/PD_Model/IRAP_CompanyInfo.csv')
unitLink = pd.read_csv(r'E:/instances/Irap_refersh_code/Data_Revision/data_revision/PD_Model/unit_sector_region_link.csv')


@st.cache
def get_data(options=option):
    mdf = pd.read_csv(f'E:/instances/Irap_refersh_code/Data_Revision/data_revision/Result/{options}/MDF_Individual/MDF_Individual_ready.csv')
    mdf = pd.merge(mdf, companyInfo, on='CompanyCode', how='left')
    gc.collect()
    return mdf

mdf = get_data()

companyCode = mdf['CompanyName'].drop_duplicates().to_list()
companyCodeoption = st.sidebar.selectbox("Company Code", companyCode)

filteredMDF = mdf.loc[mdf['CompanyName'] == companyCodeoption]
filteredMDF = filteredMDF[['CompanyCode', 'DataDate', 'Horizon', 'MDFType', 'VariableID', 'MDFValue']]


mdfplot = alt.Chart(filteredMDF).mark_bar().encode(
    x='MDFValue',
    y="VariableID"
).properties(title = companyCodeoption).interactive()


st.altair_chart(mdfplot, use_container_width=True)
st.dataframe(filteredMDF)

# alt.Chart(source).mark_bar().encode(
#     x='wheat:Q',
#     y="year:O"
# ).properties(height=700)


# pdPlot = alt.Chart(filteredPD).mark_line(point=alt.OverlayMarkDef(color="blue")).encode(
#     x = 'DataDate',
#     y = 'PD',
#     tooltip=['DataDate', 'PD']
# ).configure_axis(
#     grid=False
# ).properties(title = companyCodeoption).interactive()
