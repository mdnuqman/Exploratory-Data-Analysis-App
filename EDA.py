import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Exploratory Data Analysis (EDA)", page_icon="📊", layout="wide")

st.markdown("""
<style>
    /* Main background and font */
    .main { background-color: #f8f9fb; }
    
    /* Custom header */
    .eda-header {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
    }
    .eda-header h1 { font-size: 2rem; font-weight: 700; margin: 0; color: white; }
    .eda-header p  { font-size: 1rem; margin: 0.4rem 0 0; opacity: 0.85; }

    /* Section headings */
    .section-heading {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a73e8;
        border-left: 4px solid #1a73e8;
        padding-left: 10px;
        margin: 1.5rem 0 0.8rem;
    }

    /* Metric cards */
    .metric-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 1.5rem; }
    .metric-card {
        flex: 1; min-width: 140px;
        background: white;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-top: 4px solid #1a73e8;
        text-align: center;
    }
    .metric-card.green  { border-top-color: #34a853; }
    .metric-card.amber  { border-top-color: #fbbc04; }
    .metric-card.red    { border-top-color: #ea4335; }
    .metric-card .val   { font-size: 1.8rem; font-weight: 700; color: #202124; }
    .metric-card .label { font-size: 0.78rem; color: #5f6368; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }

    /* Info / warning boxes */
    .info-box {
        background: #e8f0fe;
        border-left: 4px solid #1a73e8;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #1a73e8;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .warn-box {
        background: #fef9e7;
        border-left: 4px solid #fbbc04;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #856404;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background: #e6f4ea;
        border-left: 4px solid #34a853;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #1e6b36;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .error-box {
        background: #fce8e6;
        border-left: 4px solid #ea4335;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #c5221f;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* Badge pills */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-blue   { background: #e8f0fe; color: #1a73e8; }
    .badge-green  { background: #e6f4ea; color: #34a853; }
    .badge-red    { background: #fce8e6; color: #ea4335; }
    .badge-amber  { background: #fef9e7; color: #856404; }

    /* Chart section card */
    .chart-card {
        background: white;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }

    /* Divider */
    .eda-divider {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 1.5rem 0;
    }

    /* Upload area hint */
    .upload-hint {
        background: white;
        border: 2px dashed #1a73e8;
        border-radius: 14px;
        padding: 2rem;
        text-align: center;
        color: #5f6368;
        margin-bottom: 1rem;
    }
    .upload-hint span { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }
    .upload-hint p    { margin: 0; font-size: 0.95rem; }

    /* Streamlit default tweaks */
    div[data-testid="stFileUploader"] { border-radius: 12px; }
    div[data-testid="metric-container"] { background: white; border-radius: 12px; padding: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    .stSelectbox label, .stMultiSelect label, .stSlider label { font-weight: 600; color: #3c4043; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="eda-header">
    <h1>📊 Exploratory Data Analysis</h1>
    <p>Upload a CSV or Excel file to explore your data interactively</p>
</div>
""", unsafe_allow_html=True)

# ── Upload hint + widget ─────────────────────────────────────────────────────
st.markdown("""
<div class="upload-hint">
    <span>📂</span>
    <p>Drag &amp; drop your file below, or click <strong>Browse files</strong></p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload A CSV Or An Excel File", type=["csv", "xlsx"])

# ── Main logic ───────────────────────────────────────────────────────────────
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        bool_cols = data.select_dtypes(include=["bool"]).columns
        data[bool_cols] = data[bool_cols].astype("str")
    except Exception as e:
        st.markdown('<div class="error-box">❌ Could not read the file. Please check the format.</div>', unsafe_allow_html=True)
        st.exception(e)
        st.stop()

    st.markdown('<div class="success-box">✅ File uploaded successfully!</div>', unsafe_allow_html=True)

    # ── Metric cards ─────────────────────────────────────────────────────────
    missing_total = int(data.isnull().sum().sum())
    dup_total     = int(data.duplicated().sum())
    missing_class = "amber" if missing_total > 0 else "green"
    dup_class     = "red"   if dup_total     > 0 else "green"

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="val">{data.shape[0]:,}</div>
            <div class="label">Rows</div>
        </div>
        <div class="metric-card">
            <div class="val">{data.shape[1]}</div>
            <div class="label">Columns</div>
        </div>
        <div class="metric-card {missing_class}">
            <div class="val">{missing_total:,}</div>
            <div class="label">Missing values</div>
        </div>
        <div class="metric-card {dup_class}">
            <div class="val">{dup_total:,}</div>
            <div class="label">Duplicates</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Data preview ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">🔍 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(data.head(), use_container_width=True)

    # ── Missing values ───────────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">⚠️ Missing Values</div>', unsafe_allow_html=True)
    if missing_total > 0:
        missing = data.isnull().sum()
        missing = missing[missing > 0].reset_index()
        missing.columns = ["Column", "Missing Values"]
        st.dataframe(missing, use_container_width=True)
    else:
        st.markdown('<div class="success-box">✅ No missing values found in this dataset.</div>', unsafe_allow_html=True)

    # ── Dataset info ─────────────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📋 Dataset Info</div>', unsafe_allow_html=True)
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())

    # ── Statistical summaries ────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📐 Statistical Summary — Numerical</div>', unsafe_allow_html=True)
    st.dataframe(data.describe(), use_container_width=True)

    st.markdown('<div class="section-heading">🔤 Statistical Summary — Non-Numerical</div>', unsafe_allow_html=True)
    non_num = data.select_dtypes(include=["bool", "object"])
    if non_num.empty:
        st.markdown('<div class="info-box">ℹ️ No non-numerical columns found.</div>', unsafe_allow_html=True)
    else:
        st.dataframe(non_num.describe(), use_container_width=True)

    # ── Correlation heatmap ──────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🌡️ Correlation Heatmap</div>', unsafe_allow_html=True)
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.empty:
        st.markdown('<div class="warn-box">⚠️ No numerical columns found for correlation.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        correlation = numeric_data.corr()
        im = ax.imshow(correlation, cmap="coolwarm", aspect="auto")
        plt.colorbar(im, ax=ax)
        ax.set_xticks(range(len(correlation.columns)))
        ax.set_yticks(range(len(correlation.columns)))
        ax.set_xticklabels(correlation.columns, rotation=45, ha="right")
        ax.set_yticklabels(correlation.columns)
        ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold", pad=12)
        fig.patch.set_facecolor("white")
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Column selector ──────────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🎯 Select Columns For Analysis</div>', unsafe_allow_html=True)
    selected_columns = st.multiselect("Choose Columns", data.columns.tolist())
    if selected_columns:
        st.dataframe(data[selected_columns].head(), use_container_width=True)
    else:
        st.markdown('<div class="info-box">ℹ️ No columns selected — showing full dataset.</div>', unsafe_allow_html=True)
        st.dataframe(data.head(), use_container_width=True)

    # ── Filter ───────────────────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🔎 Filter Data By Value</div>', unsafe_allow_html=True)
    filter_col = st.selectbox("Select Column To Filter", options=data.columns.tolist())

    if pd.api.types.is_numeric_dtype(data[filter_col]):
        min_val = float(data[filter_col].min())
        max_val = float(data[filter_col].max())
        filter_range = st.slider("Select Range", min_value=min_val, max_value=max_val, value=(min_val, max_val))
        filtered_data = data[(data[filter_col] >= filter_range[0]) & (data[filter_col] <= filter_range[1])]
    else:
        unique_vals = data[filter_col].dropna().unique().tolist()
        selected_vals = st.multiselect("Select Values", options=unique_vals, default=unique_vals)
        filtered_data = data[data[filter_col].isin(selected_vals)]

    st.markdown(f'<div class="info-box">📄 Showing <strong>{len(filtered_data):,}</strong> of <strong>{len(data):,}</strong> rows after filtering.</div>', unsafe_allow_html=True)
    st.dataframe(filtered_data, use_container_width=True)

    # ── Data visualisation ───────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 Data Visualisation</div>', unsafe_allow_html=True)

    columns = data.columns.tolist()
    col_x, col_y = st.columns(2)
    with col_x:
        x_axis = st.selectbox("X Axis", options=columns)
    with col_y:
        y_axis = st.selectbox("Y Axis", options=[c for c in columns if c != x_axis])

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: line_btn    = st.button("📈 Line")
    with col2: scatter_btn = st.button("🔵 Scatter")
    with col3: bar_btn     = st.button("📊 Bar")
    with col4: histo_btn   = st.button("📉 Histogram")
    with col5: box_btn     = st.button("📦 Box Plot")

    def show_chart(fig, title):
        st.markdown(f'<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)
        fig.patch.set_facecolor("white")
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    if line_btn:
        if not pd.api.types.is_numeric_dtype(data[y_axis]):
            st.markdown('<div class="error-box">❌ Y-axis must be a numerical column for a line chart.</div>', unsafe_allow_html=True)
        else:
            plot_data = data[[x_axis, y_axis]].dropna()
            fig, ax = plt.subplots()
            ax.plot(plot_data[x_axis], plot_data[y_axis], color="#1a73e8", linewidth=2)
            ax.set_xlabel(x_axis); ax.set_ylabel(y_axis)
            ax.set_title(f"Line Chart: {x_axis} vs {y_axis}", fontweight="bold")
            ax.grid(True, alpha=0.3); ax.spines[["top","right"]].set_visible(False)
            show_chart(fig, f"📈 Line Chart — {x_axis} vs {y_axis}")

    if scatter_btn:
        if not pd.api.types.is_numeric_dtype(data[y_axis]):
            st.markdown('<div class="error-box">❌ Y-axis must be a numerical column for a scatter plot.</div>', unsafe_allow_html=True)
        else:
            plot_data = data[[x_axis, y_axis]].dropna()
            fig, ax = plt.subplots()
            ax.scatter(plot_data[x_axis], plot_data[y_axis], color="#1a73e8", alpha=0.6, edgecolors="white", linewidth=0.5)
            ax.set_xlabel(x_axis); ax.set_ylabel(y_axis)
            ax.set_title(f"Scatter Plot: {x_axis} vs {y_axis}", fontweight="bold")
            ax.grid(True, alpha=0.3); ax.spines[["top","right"]].set_visible(False)
            show_chart(fig, f"🔵 Scatter Plot — {x_axis} vs {y_axis}")

    if bar_btn:
        if data[x_axis].nunique() > 50:
            st.markdown('<div class="warn-box">⚠️ Too many unique values for a bar chart. Try a different column.</div>', unsafe_allow_html=True)
        else:
            plot_data = data[[x_axis, y_axis]].dropna()
            fig, ax = plt.subplots()
            ax.bar(plot_data[x_axis], plot_data[y_axis], color="#1a73e8", alpha=0.8, edgecolor="white")
            ax.set_xlabel(x_axis); ax.set_ylabel(y_axis)
            ax.set_title(f"Bar Chart: {x_axis} vs {y_axis}", fontweight="bold")
            plt.xticks(rotation=45, ha="right")
            ax.grid(True, axis="y", alpha=0.3); ax.spines[["top","right"]].set_visible(False)
            show_chart(fig, f"📊 Bar Chart — {x_axis} vs {y_axis}")

    if histo_btn:
        if not pd.api.types.is_numeric_dtype(data[x_axis]):
            st.markdown('<div class="error-box">❌ X-axis must be a numerical column for a histogram.</div>', unsafe_allow_html=True)
        else:
            plot_data = data[[x_axis]].dropna()
            fig, ax = plt.subplots()
            ax.hist(plot_data[x_axis], bins=20, color="#1a73e8", edgecolor="white", alpha=0.85)
            ax.set_xlabel(x_axis); ax.set_ylabel("Frequency")
            ax.set_title(f"Histogram: {x_axis}", fontweight="bold")
            ax.grid(True, axis="y", alpha=0.3); ax.spines[["top","right"]].set_visible(False)
            show_chart(fig, f"📉 Histogram — {x_axis}")

    if box_btn:
        if not pd.api.types.is_numeric_dtype(data[x_axis]):
            st.markdown('<div class="error-box">❌ X-axis must be a numerical column for a box plot.</div>', unsafe_allow_html=True)
        else:
            plot_data = data[[x_axis]].dropna()
            fig, ax = plt.subplots()
            bp = ax.boxplot(plot_data[x_axis], patch_artist=True,
                            boxprops=dict(facecolor="#e8f0fe", color="#1a73e8"),
                            medianprops=dict(color="#ea4335", linewidth=2),
                            whiskerprops=dict(color="#1a73e8"),
                            capprops=dict(color="#1a73e8"),
                            flierprops=dict(markerfacecolor="#fbbc04", marker="o"))
            ax.set_ylabel(x_axis)
            ax.set_title(f"Box Plot: {x_axis}", fontweight="bold")
            ax.grid(True, axis="y", alpha=0.3); ax.spines[["top","right"]].set_visible(False)
            show_chart(fig, f"📦 Box Plot — {x_axis}")

    # ── Outlier detection ────────────────────────────────────────────────────
    st.markdown('<hr class="eda-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🚨 Outlier Detection (IQR Method)</div>', unsafe_allow_html=True)
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.empty:
        st.markdown('<div class="info-box">ℹ️ No numerical columns found for outlier detection.</div>', unsafe_allow_html=True)
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

        # Colour-code the Total Outliers column
        def highlight_outliers(val):
            if isinstance(val, int):
                color = "#fce8e6" if val > 0 else "#e6f4ea"
                return f"background-color: {color}"
            return ""

        st.dataframe(
            outlier_df.style.applymap(highlight_outliers, subset=["Total Outliers"]),
            use_container_width=True
        )
