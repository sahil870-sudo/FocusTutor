import streamlit as st
from google import genai

# --- CONFIGURATION ---
st.set_page_config(page_title="FocusTutor AI", page_icon="🤖", layout="centered")

# --- SIDEBAR: THE CONTEXT MENU ---
st.sidebar.title("⚙️ Tutor Settings")

academic_phase = st.sidebar.selectbox(
    "Current Academic Phase",
    ["Class 11", "Class 12", "Dropper"]
)

primary_target = st.sidebar.selectbox(
    "Primary Target",
    ["Board Exams", "JEE Mains", "JEE Advanced"]
)

teaching_style = st.sidebar.selectbox(
    "Teaching Style",
    ["Hint Mode (Socratic)", "Direct Answer"]
)

# --- MAIN INTERFACE ---
st.title("FocusTutor AI")

user_question = st.text_area("Ask your physics, chemistry, or math question:")

system_rules = f"""
You are an expert tutor for {academic_phase} students in India preparing for {primary_target}.
The student wants you to use the teaching style: {teaching_style}.
If the style is Socratic, guide them with hints rather than giving direct formulas or answers immediately.
Keep your tone encouraging, supportive, and scientifically accurate.
"""

if st.button("Ask Tutor"):
    if not user_question.strip():
        st.warning("Please type a question first!")
    else:
        try:
            with st.spinner("Tutor is thinking..."):
                api_key = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=user_question,
                    config={
                        'system_instruction': system_rules
                    }
                )
                
                st.subheader("Tutor Response:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"API Error. Check your key or try again. Details: {e}")
