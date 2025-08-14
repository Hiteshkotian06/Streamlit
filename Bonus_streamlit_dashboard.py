import streamlit as st
import pandas as pd
import plotly.express as px

# Load pre-calculated data
df = pd.read_csv('Cx Analytics Assignment Solved - Data.csv')

# Convert date columns (keeping your original calculations)
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate']) 
df['LastLogin'] = pd.to_datetime(df['LastLogin'])

# Sidebar filters
st.sidebar.header("Filters")
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique()))
plan = st.sidebar.selectbox("Select Plan", ["All"] + sorted(df["PlanType"].unique()))
status = st.sidebar.selectbox("Select Status", ["All"] + sorted(df["Status"].unique()))

# filters
filtered_df = df.copy()
if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]
if plan != "All":
    filtered_df = filtered_df[filtered_df["PlanType"] == plan]
if status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status]

# Title
st.title('Customer Subscription Analytics Dashboard')

# Key Metrics
st.subheader('Key Metrics')
total_customers = len(filtered_df)
churned_customers = len(filtered_df[filtered_df['Status'] == 'Churned'])
churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", total_customers)
col2.metric("Churn Rate", f"{churn_rate:.1f}%")
col3.metric("Avg MRR", f"${filtered_df['MonthlyRevenue'].mean():.2f}")
total_cltv_value = filtered_df['CLTV'].sum()
col4.metric("Total CLTV", f"${total_cltv_value:,.2f}")

# Visualizations
tab1, tab2, tab3 = st.tabs(["Churn Analysis", "Revenue Insights", "Customer Segments"])

# Tab 1
with tab1:
    st.subheader('Churn Distribution')
    fig1 = px.pie(
        filtered_df['Status'].value_counts().reset_index(),
        names='Status',
        values='count',
        hole=0.3,
        title='Active vs Churned Customers'
    )
    st.plotly_chart(fig1)
    
    st.subheader('Churn Reasons Analysis')
    fig2 = px.box(
        filtered_df[filtered_df['Status'] == 'Churned'],
        x='PlanType',
        y='Subscription Duration (Month)',
        color='Region',
        title='Churned Customer Duration by Plan/Region'
    )
    st.plotly_chart(fig2)

# Tab 2
with tab2:
    st.subheader('Revenue by Plan Type')
    fig3 = px.bar(
        filtered_df.groupby('PlanType')['Total Revenue'].sum().reset_index(),
        x='PlanType',
        y='Total Revenue',
        title='Total Revenue by Plan Type'
    )
    st.plotly_chart(fig3)
    
    st.subheader('MRR Distribution')
    fig4 = px.histogram(
        filtered_df,
        x='MonthlyRevenue',
        nbins=20,
        color='Status',
        title='Monthly Revenue Distribution'
    )
    st.plotly_chart(fig4)

# Tab 3
with tab3:
    st.subheader('NPS Analysis')
    fig5 = px.scatter(
        filtered_df,
        x='SupportTickets',
        y='NPS',
        color='Status',
        hover_data=['CustomerID'],
        title='Customer Satisfaction vs Support Tickets'
    )
    st.plotly_chart(fig5)
    
    st.subheader('Top Customers by CLTV')
    st.dataframe(
        filtered_df.nlargest(10, 'CLTV')[['CustomerID', 'PlanType', 'Region', 'CLTV']]
        .sort_values('CLTV', ascending=False)
        .style.format({'CLTV': '${:,.2f}'})
    )
