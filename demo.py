import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
data_pret = pd.read_csv('Pepsico_pretzels_UPCs_with_COGS_zero_discount_V2.csv')
data_tort = pd.read_csv('Pepsico_tortillas_UPCs_with_COGS_zero_discount_V3.csv')

# concatenate the two datasets at the row level
data = pd.concat([data_pret, data_tort], axis=0)

data['WEEK_START_parsed'] = pd.to_datetime(data['WEEK_START_parsed']).dt.strftime('%Y-%m-%d')

holiday_weeks = ['2010-12-27', '2011-01-03', '2011-12-19', '2011-12-26']

# Sidebar - Filters
week = st.sidebar.selectbox(
    'Select Week', 
    sorted(data['WEEK_START_parsed'].unique()), 
    format_func=lambda x: f"{x} (HOLIDAY)" if x in holiday_weeks else x
)


companies = st.sidebar.multiselect('Select Company', sorted(data['Parent_Company'].unique()), default=sorted(data['Parent_Company'].unique())[0])
product_type = st.sidebar.selectbox('Select Product Type', sorted(data['PRODUCT_TYPE'].unique()))

# Filtering data based on selections
filtered_data = data[(data['WEEK_START_parsed'] == week) & 
                     (data['Parent_Company'].isin(companies)) & 
                     (data['PRODUCT_TYPE'] == product_type)]

# Color palette (you can choose a different palette)
color_palette = px.colors.qualitative.Dark24

# Plotting with Plotly
fig = px.scatter(filtered_data, x='Incr.Revenue', y='Incr. Gross Profit',
                 color='Parent_Company', hover_data=['UPC'],
                 color_discrete_sequence=color_palette)

fig.update_layout(
    title='Incr. Revenue vs Incr. Gross Profit',
    xaxis_title='Incr.Revenue',
    yaxis_title='Incr. Gross Profit',
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

# Define manual ranges for the axes (you may adjust these based on your data)
x_range = [filtered_data['Incr.Revenue'].min() - 50, filtered_data['Incr.Revenue'].max() + 50]
y_range = [filtered_data['Incr. Gross Profit'].min() - 50, filtered_data['Incr. Gross Profit'].max() + 50]

# Highlighting x=0 and y=0 axes across the entire plot
fig.add_shape(type="line", x0=0, y0=y_range[0], x1=0, y1=y_range[1],
              line=dict(color="red", width=2))
fig.add_shape(type="line", x0=x_range[0], y0=0, x1=x_range[1], y1=0,
              line=dict(color="red", width=2))

# Show plot in Streamlit
st.plotly_chart(fig)
