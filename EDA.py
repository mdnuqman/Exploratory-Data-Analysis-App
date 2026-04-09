import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
st.set_page_config(page_title="Exploratory Data Analysis (EDA)",page_icon="📊",layout="wide")
st.title("Exploratory Data Analysis (EDA)")
st.write("Upload A **CSV** Or An **Excel** File To Explore Data Interactively!")

# for uploading file
uploaded_file = st.file_uploader("Upload A CSV Or An Excel File",type=["csv","xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        # converting bool columns [True/False] into str
        bool_cols = data.select_dtypes(include=["bool"]).columns
        data[bool_cols] = data[bool_cols].astype("str")
    except Exception as e:
        st.error("Could Not Read Excel / CSV File. Please Check The File Format")
        st.exception(e)
        st.stop()
    st.success("File Uploaded Successfully!")
    st.write("### Preview Of Data")
    st.dataframe(data.head())

    st.write("### Data Overview")
    st.write("Number Of Rows :",data.shape[0])
    st.write("Number Of Columns :",data.shape[1])
    st.write("Number Of Missing Values :",data.isnull().sum().sum())
    if data.isnull().sum().sum() > 0:
        st.write("### Missing Values Per Column")
        missing = data.isnull().sum()
        missing = missing[missing > 0].reset_index()
        missing.columns = ["Column","Missing Values"]
        st.dataframe(missing)
    else:
        st.info("No Missing Values Found In This Dataset")
    st.write("Number Of Duplicated Records :",data.duplicated().sum())

    st.write("### Complete Summary Of Dataset")
    buffer = io.StringIO()
    data.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)

    st.write("### Statistical Summary Of Dataset")
    st.dataframe(data.describe())

    st.write("### Statistical Summary For Non-Numerical Features Of Dataset")
    non_num = data.select_dtypes(include=["bool", "object"])
    if non_num.empty:
        st.info("No Non-Numerical Columns Found In This Dataset")
    else:
        st.dataframe(non_num.describe())

    st.write("### Correlation Heatmap")
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.empty:
        st.info("No Numerical Column Found For Correlation")
    else:
        fig, ax = plt.subplots(figsize=(10,6))
        correlation = numeric_data.corr()
        im = ax.imshow(correlation, cmap="coolwarm", aspect="auto")
        plt.colorbar(im, ax=ax)
        ax.set_xticks(range(len(correlation.columns)))
        ax.set_yticks(range(len(correlation.columns)))
        ax.set_xticklabels(correlation.columns, rotation=45, ha="right")
        ax.set_yticklabels(correlation.columns)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)

    st.write("### Select The Desired Columns For Analysis")
    selected_columns = st.multiselect("Choose Columns",data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info("No Columns Selected. Showing Full Dataset")
        st.dataframe(data.head())

    st.write("### Filter Data By Value")
    filter_col = st.selectbox("Select Column To Filter", options=data.columns.tolist())

    if pd.api.types.is_numeric_dtype(data[filter_col]):
        min_val = float(data[filter_col].min())
        max_val = float(data[filter_col].max())
        filter_range = st.slider(
            "Select Range",
            min_value = min_val,
            max_value = max_val,
            value = (min_val, max_val)
        )
        filtered_data = data[(data[filter_col] >= filter_range[0]) & (data[filter_col] <= filter_range[1])]
    else:
        unique_vals = data[filter_col].dropna().unique().tolist()
        selected_vals = st.multiselect("Select Values", options=unique_vals, default=unique_vals)
        filtered_data = data[data[filter_col].isin(selected_vals)]
    
    st.write(f"### Filtered Data ({len(filtered_data)} rows)")
    st.dataframe(filtered_data)


    st.write("## Data Visualization")
    st.write("Select **Columns** For Data Visualization")
    columns = data.columns.tolist()
    x_axis = st.selectbox("Select Column For X-Axis",options=columns)
    y_axis = st.selectbox("Select Column For Y-Axis",options=[c for c in columns if c != x_axis])

    # Creating Buttons For Diff Diff Charts
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        line_btn = st.button("Click Here To Generate The Line Graph")
    with col2:
        scatter_btn = st.button("Click Here To Generate the Scatter Plot")
    with col3:
        bar_btn = st.button("Click Here To Generate The Bar Graph")
    with col4:
        histo_btn = st.button("Click Here To Generate The Histogram")
    with col5:
        box_btn = st.button("Click Here To Generate The Box Plot")
    
    if line_btn:
        if not pd.api.types.is_numeric_dtype(data[y_axis]):
            st.error("Y-axis must be a numerical column for this chart!")
        else:
            plot_data = data[[x_axis,y_axis]].dropna()
            st.write("### Showing Line Graph")
            fig,ax = plt.subplots()
            ax.plot(plot_data[x_axis],plot_data[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Line Graph Of {x_axis} Vs {y_axis}")
            st.pyplot(fig,width=1000) # show the graph
    if scatter_btn:
        if not pd.api.types.is_numeric_dtype(data[y_axis]):
            st.error("Y-axis must be a numerical column for this chart!")
        else:
            plot_data = data[[x_axis,y_axis]].dropna()
            st.write("### Showing Scatter Graph")
            fig,ax = plt.subplots()
            ax.scatter(plot_data[x_axis],plot_data[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Scatter Graph Of {x_axis} Vs {y_axis}")
            st.pyplot(fig,width=1000) # show the graph
    if bar_btn:
        if data[x_axis].nunique()>50:
            st.warning("Too many unique values for a bar chart. Try a different column!")
        else:
            plot_data = data[[x_axis,y_axis]].dropna()
            st.write("### Showing Bar Graph")
            fig,ax = plt.subplots()
            ax.bar(plot_data[x_axis],plot_data[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Bar Graph Of {x_axis} Vs {y_axis}")
            st.pyplot(fig,width=1000) # show the graph
    if histo_btn:
        if not pd.api.types.is_numeric_dtype(data[x_axis]):
            st.error("X-Axis must be a numerical column for a histogram!")
        else:
            plot_data = data[[x_axis]].dropna()
            st.write("### Showing Histogram")
            fig, ax = plt.subplots()
            ax.hist(plot_data[x_axis], bins=20, color="steelblue", edgecolor="black")
            ax.set_xlabel(x_axis)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Histogram Of {x_axis}")
            st.pyplot(fig, width=1000)
    if box_btn:
        if not pd.api.types.is_numeric_dtype(data[x_axis]):
            st.error("X-Axis must be a numerical column for a box plot!")
        else:
            plot_data = data[[x_axis]].dropna()
            st.write("### Showing Box Plot")
            fig, ax = plt.subplots()
            ax.boxplot(plot_data[x_axis])
            ax.set_ylabel(x_axis)
            ax.set_title(f"Box Plot Of {x_axis}")
            st.pyplot(fig, width=1000)
    st.write("### Outlier Detection")
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.empty:
        st.info("No Numerical Columns Found For Outlier")
    else:
        outlier_summary = []
        for col in numeric_data.columns:
            Q1 = numeric_data[col].quantile(0.25)
            Q3 = numeric_data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = numeric_data[(numeric_data[col] < lower) | (numeric_data[col] > upper)]
            outlier_summary.append({
                "Column": col,
                "Total Outliers": len(outliers),
                "Lower Bound": round(lower, 2),
                "Upper Bound": round(upper, 2)
            })
        outlier_df = pd.DataFrame(outlier_summary)
        st.dataframe(outlier_df)