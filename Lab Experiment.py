import streamlit as st
import pandas as pd
import requests 
# Page Configuration
st.set_page_config(
    page_title="Experiment Dashboard - Practicals",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Experiment Dashboard: Practicals")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to Section",
    [
        "1. Protocol & Systematic Literature Search",
        "2. Results & Data Upload",
        "3. Checker / Mentor Review",
        "4. Print & Submission Preview",
        "5. Power BI Analytics"
    ]
)

# Initialize Session State Variables
if "aim" not in st.session_state:
    st.session_state["aim"] = "Design and evaluation of modified release dosage forms."

# Systematic Literature Search & Research Scope State
if "lit_query" not in st.session_state:
    st.session_state["lit_query"] = "(\"modified release\" OR \"sustained release\") AND (\"dissolution kinetics\" OR \"Korsmeyer-Peppas\")"
if "lit_databases" not in st.session_state:
    st.session_state["lit_databases"] = "PubMed, ScienceDirect, Google Scholar"
if "lit_drugs" not in st.session_state:
    st.session_state["lit_drugs"] = "Metoprolol Succinate, Curcumin, Diltiazem HCl"
if "lit_formulations" not in st.session_state:
    st.session_state["lit_formulations"] = "Hydrophilic Matrix Tablets, Solid Dispersions, Floating Microballoons"
if "lit_diseases" not in st.session_state:
    st.session_state["lit_diseases"] = "Hypertension, Inflammatory Bowel Disease (IBD), Cardiovascular Disorders"
if "lit_criteria" not in st.session_state:
    st.session_state["lit_criteria"] = "Inclusion: Peer-reviewed articles (2015-2026), English language.\nExclusion: Non-oral dosage forms, missing kinetic parameters."
if "lit_summary" not in st.session_state:
    st.session_state["lit_summary"] = "Identified key formulation parameters influencing polymer matrix hydration and release rates."
if "lit_gaps" not in st.session_state:
    st.session_state["lit_gaps"] = "Limited in vivo correlation for high-variability gastrointestinal transit times; lack of standardized release kinetics models for complex multi-polymer matrices."
if "lit_prospects" not in st.session_state:
    st.session_state["lit_prospects"] = "Application of 3D printing for personalized controlled release doses and integration of Machine Learning (QbD) for automated dissolution modeling."

# Protocol & Review State
if "materials" not in st.session_state:
    st.session_state["materials"] = "Active Pharmaceutical Ingredient (API), Hydrophilic Polymers, Excipients, Buffer Solution (pH 6.8)."
if "method" not in st.session_state:
    st.session_state["method"] = "1. Prepare formulation powder blend.\n2. Compress tablets using rotary press.\n3. Perform dissolution testing (USP Type II Apparatus)."
if "mentor_status" not in st.session_state:
    st.session_state["mentor_status"] = "Pending Review"
if "mentor_comments" not in st.session_state:
    st.session_state["mentor_comments"] = ""


# ==========================================
# SECTION 1: PROTOCOL & SYSTEMATIC LITERATURE SEARCH
# ==========================================
if page == "1. Protocol & Systematic Literature Search":
    st.header("📋 Experiment Protocol & Research Scope")
    
    st.subheader("Aim")
    st.session_state["aim"] = st.text_area("State the Aim of the Experiment", value=st.session_state["aim"], height=80)
    
    st.subheader("🔍 Systematic Literature Search")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["lit_query"] = st.text_input("Search Strategy / Keywords", value=st.session_state["lit_query"])
        st.session_state["lit_drugs"] = st.text_input("Target Model Drugs (APIs)", value=st.session_state["lit_drugs"])
        st.session_state["lit_diseases"] = st.text_input("Target Diseases / Indications", value=st.session_state["lit_diseases"])
    with col2:
        st.session_state["lit_databases"] = st.text_input("Databases Searched", value=st.session_state["lit_databases"])
        st.session_state["lit_formulations"] = st.text_input("Dosage Forms / Formulations", value=st.session_state["lit_formulations"])
        
    st.session_state["lit_criteria"] = st.text_area("Inclusion & Exclusion Criteria", value=st.session_state["lit_criteria"], height=100)
    st.session_state["lit_summary"] = st.text_area("Key Literature Findings / Theory Overview", value=st.session_state["lit_summary"], height=120)
    
    st.subheader("💡 Research Gap & Future Prospects")
    st.session_state["lit_gaps"] = st.text_area("Identified Research Gaps", value=st.session_state["lit_gaps"], height=100)
    st.session_state["lit_prospects"] = st.text_area("Future Prospects & Directions", value=st.session_state["lit_prospects"], height=100)

    st.subheader("Materials & Reagents")
    st.session_state["materials"] = st.text_area("List Materials & Equipment Used", value=st.session_state["materials"], height=100)
    
    st.subheader("Method / Methodology")
    st.session_state["method"] = st.text_area("Step-by-Step Procedure", value=st.session_state["method"], height=120)

# ==============================================================================
# SECTION 2: RESULTS & DATA UPLOAD
# ==============================================================================
elif page == "2. Results & Data Upload":
    st.header("📊 Results & Data Upload")
    
    # File uploader widget
    uploaded_file = st.file_uploader("Upload Custom Experimental Data (Excel or CSV)", type=["csv", "xlsx"])
    
    # DEFAULT FILE NAME (Must match the exact filename committed to your GitHub repo)
    DEFAULT_EXCEL_FILE = "Diclofenac_Sodium_SR_Dissolution_Clean.xlsx"

    # --------------------------------------------------------------------------
    # 1. CASE A: User uploads a custom file via the uploader widget
    # --------------------------------------------------------------------------
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                xls = pd.ExcelFile(uploaded_file)
                # Auto-detect clean summary sheet if available
                sheet_to_load = "Summary_Data" if "Summary_Data" in xls.sheet_names else 0
                df = pd.read_excel(uploaded_file, sheet_name=sheet_to_load)
            else:
                df = pd.read_csv(uploaded_file)
            
            st.session_state["results_df"] = df
            st.success("Custom file uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

    # --------------------------------------------------------------------------
    # 2. CASE B: Auto-load default dataset from GitHub repository if no file is uploaded
    # --------------------------------------------------------------------------
    elif "results_df" not in st.session_state or st.session_state["results_df"] is None:
        try:
            xls = pd.ExcelFile(DEFAULT_EXCEL_FILE)
            sheet_to_load = "Summary_Data" if "Summary_Data" in xls.sheet_names else 0
            df_default = pd.read_excel(DEFAULT_EXCEL_FILE, sheet_name=sheet_to_load)
            
            st.session_state["results_df"] = df_default
            st.info("ℹ️ Loaded default dataset: Diclofenac Sodium SR Dissolution Profile")
        except Exception as e:
            st.warning("No default dataset found in repository. Please upload an Excel/CSV file above.")

    # --------------------------------------------------------------------------
    # 3. DISPLAY TABLE AND PLOT CHART
    # --------------------------------------------------------------------------
    if "results_df" in st.session_state and st.session_state["results_df"] is not None:
        df = st.session_state["results_df"].copy()
        
        st.subheader("📋 Experimental Data Table")
        st.dataframe(df, use_container_width=True)
        
        # Clean dataframe for plotting
        df_clean = df.dropna(how="all").dropna(axis=1, how="all")
        numeric_df = df_clean.select_dtypes(include=["number"])
        
        if not numeric_df.empty:
            st.subheader("📈 Interactive Dissolution / Calibration Curve")
            
            possible_x = [col for col in df_clean.columns if any(k in str(col).lower() for k in ["time", "conc", "min", "hr", "ug"])]
            
            if possible_x:
                x_col = possible_x[0]
                plot_data = numeric_df.copy()
                plot_data[x_col] = pd.to_numeric(df_clean[x_col], errors="coerce")
                plot_data = plot_data.dropna(subset=[x_col]).set_index(x_col)
                st.line_chart(plot_data)
            else:
                st.line_chart(numeric_df)
        else:
            st.warning("No numeric data columns found to render a chart.")
# ==========================================
# SECTION 3: CHECKER / MENTOR
# ==========================================
elif page == "3. Checker / Mentor Review":
    st.header("👨‍🏫 Checker / Mentor Verification")
    
    st.session_state["mentor_status"] = st.selectbox(
        "Verification Status",
        ["Pending Review", "Approved", "Needs Revision", "Rejected"],
        index=["Pending Review", "Approved", "Needs Revision", "Rejected"].index(st.session_state["mentor_status"])
    )
    
    st.session_state["mentor_comments"] = st.text_area(
        "Mentor / Checker Feedback",
        value=st.session_state["mentor_comments"],
        placeholder="Enter evaluation remarks here..."
    )
    
    if st.button("Save Evaluation"):
        st.success(f"Status updated to: {st.session_state['mentor_status']}")

# ==============================================================================
# SECTION 4: PRINT & SUBMISSION PREVIEW
# ==============================================================================
elif page == "4. Print & Submission Preview":
    st.header("🖨️ Print & Submission Preview")
    
    st.markdown(f"Aim: {st.session_state.get('aim', 'N/A')}")
    st.markdown(f"Materials: {st.session_state.get('materials', 'N/A')}")
    st.markdown(f"Method: {st.session_state.get('method', 'N/A')}")

    # Line 190 - Make sure there are 4 spaces before st.markdown
    st.markdown("### Results & Data:")
    
    if "results_df" in st.session_state and st.session_state["results_df"] is not None:
        df = st.session_state["results_df"].copy()
        
        st.dataframe(df, use_container_width=True)
        
        df_clean = df.dropna(how="all").dropna(axis=1, how="all")
        numeric_df = df_clean.select_dtypes(include=["number"])
        
        if not numeric_df.empty:
            possible_x = [col for col in df_clean.columns if any(k in str(col).lower() for k in ["time", "conc", "min", "hr", "ug"])]
            
            if possible_x:
                x_col = possible_x[0]
                plot_data = numeric_df.copy()
                plot_data[x_col] = pd.to_numeric(df_clean[x_col], errors="coerce")
                plot_data = plot_data.dropna(subset=[x_col]).set_index(x_col)
                st.line_chart(plot_data)
            else:
                st.line_chart(numeric_df)
    else:
        st.write("No data uploaded.")
# ==============================================================================
    # EXPORT / SAVE REPORT FEATURE
    # ==============================================================================
    st.markdown("---")
    st.subheader("💾 Export & Save Record")
    st.write("Download a permanent copy of your compiled practical logbook and evaluation report.")

    # 1. Compile all Session State entries into a clean text document
    compiled_report = f"""
================================================================================
                    PHARMACEUTICS PRACTICAL LOGBOOK & REPORT
================================================================================

1. EXPERIMENTAL PROTOCOL
--------------------------------------------------------------------------------
Aim:
{st.session_state.get('aim', 'N/A')}

Target Drug(s) / APIs:
{st.session_state.get('lit_drugs', 'N/A')}

2. SYSTEMATIC LITERATURE SEARCH & GAP ANALYSIS
--------------------------------------------------------------------------------
Search Query / Keywords:
{st.session_state.get('lit_query', 'N/A')}

Literature Summary:
{st.session_state.get('lit_summary', 'N/A')}

Identified Research Gaps & Rationale:
{st.session_state.get('lit_gaps', 'N/A')}

3. MENTOR REVIEW & VERIFICATION STATUS
--------------------------------------------------------------------------------
Verification Status : {st.session_state.get('mentor_status', 'Pending Review')}
Mentor Comments     : {st.session_state.get('mentor_comments', 'No comments added.')}

================================================================================
Generated via Pharmaceutics Practical Dashboard
================================================================================
"""

    # 2. Add Download Buttons for TXT and CSV summary formats
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        st.download_button(
            label="📄 Download Full Report (.txt)",
            data=compiled_report,
            file_name="Pharmaceutics_Practical_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col_dl2:
        # Create a summary CSV format for record keeping
        summary_data = {
            "Field": ["Aim", "Target Drugs", "Literature Summary", "Research Gaps", "Mentor Status"],
            "Value": [
                st.session_state.get('aim', 'N/A'),
                st.session_state.get('lit_drugs', 'N/A'),
                st.session_state.get('lit_summary', 'N/A'),
                st.session_state.get('lit_gaps', 'N/A'),
                st.session_state.get('mentor_status', 'Pending Review')
            ]
        }
        df_summary = pd.DataFrame(summary_data)
        csv_data = df_summary.to_csv(index=False)

        st.download_button(
            label="📊 Download Summary Table (.csv)",
            data=csv_data,
            file_name="Pharmaceutics_Practical_Summary.csv",
            mime="text/csv",
            use_container_width=True
        )
# ==========================================
# SECTION 5: POWER BI INTEGRATION
# ==========================================
elif page == "5. Power BI Analytics":
    st.header("📈 Power BI Analytics Integration")
    st.write("Embed your live Power BI report or view interactive analytical dashboards.")
    
    powerbi_url = st.text_input("Enter Power BI Embed URL / Share Link:", value="")
    
    if powerbi_url:
        st.components.v1.iframe(powerbi_url, width=1000, height=600, scrolling=True)
    else:
        st.info("Paste a public Power BI embed link above to view your embedded dashboard.")
