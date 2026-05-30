from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# ----------------------------
# Configuration
# ----------------------------
st.set_page_config(
    page_title="Blood Work Analyzer",
    page_icon="🩺",
    layout="wide"
)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.scroll-box {
    height: 280px;
    overflow-y: auto;
    padding: 15px;
    border: 1px solid #444;
    border-radius: 10px;
    background-color: #1e1e1e;
    line-height: 1.6;
}

.section-card {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #333;
    background-color: #111;
}

.big-title {
    text-align: center;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #b0b0b0;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown(
    "<h1 class='big-title'>🩺 Blood Work Analyzer</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Understand your blood test results with AI-powered health insights and Indian diet recommendations.</p>",
    unsafe_allow_html=True
)

# ----------------------------
# Disclaimer
# ----------------------------
st.warning(
    """
    ⚠️ **Important Disclaimer**

    This tool provides AI-generated educational insights only.
    It is NOT a medical diagnosis and should not replace professional medical advice.

    Please consult a qualified healthcare professional before making any medical decisions.
    """
)

# ----------------------------
# Layout
# ----------------------------
left_col, right_col = st.columns([1, 1])

# ----------------------------
# LEFT SIDE
# ----------------------------
with left_col:

    st.subheader("📋 Enter Blood Test Report")

    st.info(
        """
        Paste your complete blood report below.

        Include:
        - Test names
        - Measured values
        - Reference ranges

        The more complete the report, the more accurate the analysis.
        """
    )

    sample_report = """
Hemoglobin: 11.2 g/dL (Reference: 13.5 - 17.5)
Vitamin D: 18 ng/mL (Reference: 30 - 100)
Total Cholesterol: 240 mg/dL (Reference: <200)
HDL Cholesterol: 35 mg/dL (Reference: >40)
Triglycerides: 190 mg/dL (Reference: <150)
Fasting Blood Sugar: 112 mg/dL (Reference: 70 - 100)
"""

    if st.button("📄 Load Sample Report"):
        st.session_state["blood_report"] = sample_report

    blood_report = st.text_area(
        "Blood Report",
        value=st.session_state.get("blood_report", ""),
        height=500,
        placeholder="""
Paste your blood report here...

Example:

Hemoglobin: 11.2 g/dL (Reference: 13.5 - 17.5)
Vitamin D: 18 ng/mL (Reference: 30 - 100)
Total Cholesterol: 240 mg/dL (Reference: <200)
HDL Cholesterol: 35 mg/dL (Reference: >40)
Triglycerides: 190 mg/dL (Reference: <150)
        """
    )

    analyze_clicked = st.button(
        "🔍 Analyze Blood Report",
        type="primary",
        use_container_width=True
    )

# ----------------------------
# RIGHT SIDE
# ----------------------------
with right_col:

    st.subheader("🩺 Health Summary")

    health_box = st.empty()

    health_box.markdown(
        """
        <div class="scroll-box">
        Analysis will appear here after you click Analyze.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🥗 Recommended Indian Diet Plan")

    diet_box = st.empty()

    diet_box.markdown(
        """
        <div class="scroll-box">
        Personalized dietary recommendations will appear here.
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# ANALYSIS
# ----------------------------
if analyze_clicked:

    if not blood_report.strip():

        st.error(
            "Please paste your blood report before clicking Analyze."
        )

    else:

        with st.spinner("🔬 Analyzing blood report..."):

            # ----------------------------
            # Step 1: Extract Values
            # ----------------------------
            extraction_prompt = f"""
You are a medical data extraction assistant.

Analyze the blood report and identify every test result.

For each test provide:

- Test Name
- Result Value
- Status (HIGH / LOW / NORMAL)
- Reference Range

Blood Report:

{blood_report}
"""

            extraction_response = llm.invoke(extraction_prompt)

            extracted_values = extraction_response.content

            # ----------------------------
            # Step 2: Generate Summary
            # ----------------------------
            summary_prompt = f"""
You are an experienced clinical nutritionist.

Based on the blood report analysis below, generate two sections.

SECTION 1 - HEALTH SUMMARY

- Explain the patient's overall health in simple language.
- Mention major abnormalities.
- Explain possible implications.
- Keep it easy to understand.

SECTION 2 - INDIAN DIET PLAN

Provide:

Foods to Eat More:
- Bullet points

Foods to Reduce/Avoid:
- Bullet points

Lifestyle Suggestions:
- Bullet points

Blood Analysis:

{extracted_values}
"""

            summary_response = llm.invoke(summary_prompt)

            full_response = summary_response.content

        # ----------------------------
        # Split Sections
        # ----------------------------
        if "SECTION 2" in full_response:

            parts = full_response.split("SECTION 2")

            health_summary = (
                parts[0]
                .replace("SECTION 1 - HEALTH SUMMARY", "")
                .replace("SECTION 1", "")
                .strip()
            )

            diet_plan = (
                parts[1]
                .replace("- INDIAN DIET PLAN", "")
                .strip()
            )

        else:

            health_summary = full_response
            diet_plan = full_response

        # ----------------------------
        # Display Results
        # ----------------------------
        health_box.markdown(
            f"""
            <div class="scroll-box">
            {health_summary}
            </div>
            """,
            unsafe_allow_html=True
        )

        diet_box.markdown(
            f"""
            <div class="scroll-box">
            {diet_plan}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("✅ Analysis completed successfully!")