import streamlit as st
import time
import numpy as np
import pandas as pd

from streamlit_gsheets import GSheetsConnection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Edward Ang",
    page_icon=f"assets/logo.png",
)

@st.cache_data(ttl=200)
def run_query():
    data = conn.read(worksheet = "ECommerce Sales Data", usecols=list(range(1,26)))
    return pd.DataFrame(data)


st.header('ECommerce Sales Analytics and Forecasting')

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
df = run_query()
         
tab1, tab2 = st.tabs(['Story', 'Dashboard'])
with tab1:

    st.write("""
            My friend...  
            """)

    st.write(df)

    


    with st.expander('Code'):
        code = '''def hello():
            print("Hello, Streamlit!")'''
        st.code(code, language='python')

    # Getting the min and max date 
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()
    col1, col2 = st.columns((2))
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    st.sidebar.header("Choose your filter: ")

    # Create for Region
    category = st.sidebar.multiselect("Pick your category", df["Category"].unique())
    if not category:
        df2 = df.copy()
    else:
        df2 = df[df["Category"].isin(category)]
    

    # Create for State
    state = st.sidebar.multiselect("Pick the State", df2["Sub-Category"].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2["Sub-Category"].isin(state)]

    # Create for City
    city = st.sidebar.multiselect("Pick the City",df3["Ship Mode"].unique())

    st.bar_chart(data = df2, x='State' ,y='Quantity')

    st.bar_chart(data = df2, x='Category' ,y='Quantity')

    import plotly.express as px

    category_df = df2.groupby(by = ["Category"], as_index = False)["Sales"].sum()
    filtered_df = df2.copy()


    with col1:
        st.subheader("Category wise Sales")
        fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)

    with col2:
        st.subheader("Region wise Sales")
        fig = px.pie(df2, values = "Sales", names = "Region", hole = 0.5)
        fig.update_traces(text = df2["Region"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)

    import matplotlib.pyplot as plt
    cl1, cl2 = st.columns((2))
    with cl1:
        with st.expander("Category_ViewData"):
            st.write(category_df.style.background_gradient(cmap="Blues"))
            csv = category_df.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                                help = 'Click here to download the data as a CSV file')

    with cl2:
        with st.expander("Region_ViewData"):
            region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
            csv = region.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
            
    filtered_df["month_year"] = pd.to_datetime(filtered_df["Order Date"]).dt.to_period("M")
    st.subheader('Time Series Analysis')

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
    fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
    st.plotly_chart(fig2,use_container_width=True)




    ###########

    with st.expander("View Data of TimeSeries:"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

    # Create a treem based on Region, category, sub-Category
    st.subheader("Hierarchical view of Sales using TreeMap")
    fig3 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                    color = "Sub-Category")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3, use_container_width=True)

    chart1, chart2 = st.columns((2))
    with chart1:
        st.subheader('Segment wise Sales')
        fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with chart2:
        st.subheader('Category wise Sales')
        fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
        fig.update_traces(text = filtered_df["Category"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Sub-Category Sales Summary")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
        fig = ff.create_table(df_sample, colorscale = "Cividis")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Month wise sub-Category Table")
        filtered_df["month"] = pd.to_datetime(filtered_df["Order Date"]).dt.month_name()
        sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"],columns = "month")
        st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

    # Create a scatter plot
    data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
    data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                        titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                        yaxis = dict(title = "Profit", titlefont = dict(size=19)))
    st.plotly_chart(data1,use_container_width=True)

    with st.expander("View Data"):
        st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

    # Download orginal DataSet
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")


    

    # df = pd.DataFrame(
    # np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    # columns=['lat', 'lon'])

    # st.map(df)


        





with tab2:
    st.write('Working on it')
