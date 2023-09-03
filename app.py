
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import plotly.express as px

DATA_FILE = 'rfm.csv'

st.title("Interactive Plot to Analysis Final RFM Segments")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_FILE)
    data = data[(data['Item Price'] > 0) & (data['Grand Total'] <=360) & (data['LBP Rate'] <= 100)]
    return data

data = load_data()
segments = data['Category Cut'].unique()

#build app filters
column = st.sidebar.multiselect('Select Segments', segments)
Grand Total = st.sidebar.number_input('Smaller Than Recency', 0, 360, 360)
LBP Rate = st.sidebar.number_input('Smaller Than Frequency', 0, 100, 100)
Item Price = st.sidebar.number_input('Smaller Than Monetary Value', 0, 100000, 100000)

data = data[(data['Grand Total']<=Grand Total) & (data['LBP Rate']<=LBP Rate) & (data['Item Price']<=Item Price)]

#manage the multiple field filter
if column == []:
    data = data
else:
    data = data[data['Customer Segment'].isin(column)]

data

st.subheader('RFM Scatter Plot')
#scatter plot
fig_scatter = px.scatter(data, x="Grand Total", y="LBP Rate", color="Item Price",
                 size='Grand Total', hover_data=['Total Discount', 'Coupon Code', 'Shipping Fees'])

st.plotly_chart(fig_scatter)

#show distribution of values
#recency
fig_r = px.histogram(data, x="Grand Total", y="Order ID", marginal="box", # or violin, rug
                   hover_data=data.columns, title='Total Plot')
st.plotly_chart(fig_r)

#frequency
fig_f = px.histogram(data, x="LBP Rate", y="Order ID", marginal="box", # or violin, rug
                   hover_data=data.columns, title='Rate Plot')
st.plotly_chart(fig_f)

#monetary value
fig_m = px.histogram(data, x="Item Price", y="Order ID", marginal="box", # or violin, rug
                   hover_data=data.columns, title='Item  Plot')
st.plotly_chart(fig_m)
