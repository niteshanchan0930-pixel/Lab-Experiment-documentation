import streamlit as st
import pandas as pd

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

# ==========================================
# SECTION 2: RESULTS & DATA UPLOAD
# ==========================================
elif page == "2. Results & Data Upload":
    st.header("📊 Results & Data Upload (Word / Excel)")
    
    uploaded_file = st.file_uploader("Upload Experimental Data (Excel .xlsx, CSV, or Word .docx)", type=["xlsx", "csv", "docx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.session_state["results_df"] = df
            st.success("CSV file successfully loaded!")
            st.dataframe(df)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
            st.session_state["results_df"] = df
            st.success("Excel file successfully loaded!")
            st.dataframe(df)
        else:
            st.info("Word document (.docx) attached. File uploaded successfully for evaluation.")
    else:
        st.info("No file uploaded yet. You can manually edit the sample dataset below:")
        sample_data = pd.DataFrame({
            "Time (hr)": [1, 2, 4, 6, 8, 10, 12],
            "% Drug Released": [15.0, 32.0, 58.0, 81.0, 105.0, 122.0, 138.0]
        })
        edited_df = st.data_editor(sample_data, num_rows="dynamic")
        st.session_state["results_df"] = edited_df

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

# ==========================================
# SECTION 4: PRINT / SUBMISSION PREVIEW
# ==========================================
elif page == "4. Print & Submission Preview":
    st.header("📄 Experiment Report Preview")
    st.write("Review the complete practical document before final submission.")
    
    st.markdown("---")
    st.markdown(f"### *Aim:*\n{st.session_state['aim']}")
    
    st.markdown("### *Systematic Literature Search & Scope:*")
    st.markdown(f"- *Search Query:* {st.session_state['lit_query']}")
    st.markdown(f"- *Databases:* {st.session_state['lit_databases']}")
    st.markdown(f"- *Model Drugs:* {st.session_state['lit_drugs']}")
    st.markdown(f"- *Formulation Types:* {st.session_state['lit_formulations']}")
    st.markdown(f"- *Target Indications:* {st.session_state['lit_diseases']}")
    st.markdown(f"- *Criteria:*\n{st.session_state['lit_criteria']}")
    st.markdown(f"- *Findings & Theory:*\n{st.session_state['lit_summary']}")
    st.markdown(f"- *Research Gaps Identified:*\n{st.session_state['lit_gaps']}")
    st.markdown(f"- *Future Prospects:*\n{st.session_state['lit_prospects']}")
    
    st.markdown(f"### *Materials:*\n{st.session_state['materials']}")
    st.markdown(f"### *Method:*\n{st.session_state['method']}")
    
    st.markdown("### *Results & Data:*")
    if "results_df" in st.session_state:
        st.dataframe(st.session_state["results_df"])
        st.line_chart(st.session_state["results_df"].set_index(st.session_state["results_df"].columns[0]))
    else:
        st.write("No data uploaded.")
        
    st.markdown("---")
    st.markdown(f"*Mentor Status:* {st.session_state['mentor_status']}")
    st.markdown(f"*Mentor Comments:* {st.session_state['mentor_comments']}")

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