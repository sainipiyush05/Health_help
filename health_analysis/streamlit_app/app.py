from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Blood Work Analyzer",
    page_icon="🩺",
    layout="wide"
)

# ----------------------------
# LOAD ENVIRONMENT
# ----------------------------
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

# ----------------------------
# CUSTOM CSS
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

.title {
    text-align: center;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown(
    "<h1 class='title'>🩺 Blood Work Analyzer</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Get a quick health summary and diet recommendations from your blood report.</p>",
    unsafe_allow_html=True
)

# ----------------------------
# DISCLAIMER
# ----------------------------
st.warning(
    """
    ⚠️ This tool provides educational insights only.
    It is not a substitute for professional medical advice, diagnosis, or treatment.
    """
)

# ----------------------------
# LAYOUT
# ----------------------------
left_col, right_col = st.columns([1, 1])

# ----------------------------
# LEFT COLUMN
# ----------------------------
with left_col:

    st.subheader("📋 Enter Blood Test Report")

    st.info(
        """
        Paste your complete blood report.

        Include:
        • Test names
        • Test values
        • Reference ranges

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
Paste your blood report here.

Example:

Hemoglobin: 11.2 g/dL (Reference: 13.5 - 17.5)
Vitamin D: 18 ng/mL (Reference: 30 - 100)
Total Cholesterol: 240 mg/dL (Reference: <200)
HDL Cholesterol: 35 mg/dL (Reference: >40)
Triglycerides: 190 mg/dL (Reference: <150)
Fasting Blood Sugar: 112 mg/dL (Reference: 70 - 100)
"""
    )

    analyze_clicked = st.button(
        "🔍 Analyze Blood Report",
        type="primary",
        use_container_width=True
    )

# ----------------------------
# RIGHT COLUMN
# ----------------------------
with right_col:

    st.subheader("🩺 Health Summary")

    health_box = st.empty()

    health_box.markdown(
        """
        <div class="scroll-box">
        Your health summary will appear here.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🥗 Diet & Lifestyle Recommendations")

    diet_box = st.empty()

    diet_box.markdown(
        """
        <div class="scroll-box">
        Diet recommendations will appear here.
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# ANALYSIS
# ----------------------------
if analyze_clicked:

    if not blood_report.strip():

        st.error("Please paste your blood report before analyzing.")

    else:

        with st.spinner("🔬 Analyzing blood report..."):

            # ----------------------------
            # STEP 1: Extract Abnormal Values
            # ----------------------------
            extraction_prompt = f"""
You are a medical report analyzer.

Identify ONLY abnormal values.

For each abnormal value provide:

- Test Name
- Value
- Status (HIGH or LOW)

Blood Report:

{blood_report}
"""

            extraction_response = llm.invoke(extraction_prompt)
            extracted_values = extraction_response.content

            # ----------------------------
            # STEP 2: Generate Summary
            # ----------------------------
            summary_prompt = f"""
You are a clinical nutritionist.

Respond EXACTLY in the following format.

SECTION 1 - HEALTH SUMMARY

Overall Status:
[One sentence]

Abnormal Findings:
• Finding 1
• Finding 2
• Finding 3

Key Concern:
[One sentence]

SECTION 2 - DIET PLAN

✅ Eat More:
• Food 1
• Food 2
• Food 3

❌ Reduce:
• Food 1
• Food 2
• Food 3

🏃 Lifestyle:
• Suggestion 1
• Suggestion 2

Rules:
- Maximum 100 words.
- Keep everything concise.
- No long explanations.
- No medical jargon.
- Use common Indian foods.
- Use bullet points only.

Blood Analysis:

{extracted_values}
"""

            summary_response = llm.invoke(summary_prompt)

            result = summary_response.content

        # ----------------------------
        # SPLIT RESPONSE
        # ----------------------------
        if "SECTION 2" in result:

            sections = result.split("SECTION 2")

            health_summary = (
                sections[0]
                .replace("SECTION 1 - HEALTH SUMMARY", "")
                .strip()
            )

            diet_plan = (
                "SECTION 2" + sections[1]
            )

        else:

            health_summary = result
            diet_plan = ""

        # ----------------------------
        # DISPLAY RESULTS
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