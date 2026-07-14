import streamlit as st
import google.genai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="FocusTutor AI", page_icon="📚", layout="centered")

# --- 2. SIDEBAR: THE CONTEXT MENU ---
st.sidebar.title("⚙️ Tutor Settings")

academic_phase = st.sidebar.selectbox(
    "Current Academic Phase",
    ["Class 11", "Class 12", "Dropper"]
)

primary_goal = st.sidebar.selectbox(
    "Primary Target",
    ["Board Exams", "JEE Mains", "JEE Advanced"]
)

tutor_persona = st.sidebar.selectbox(
    "Teaching Style",
    ["Hint Mode (Socratic)", "Explain Like I'm 5", "Strict Coach"]
)

# --- 3. MAIN UI: INITIALIZATION ---
st.title("📚 FocusTutor AI")
st.write(f"**Mode:** {academic_phase} | {primary_goal} | {tutor_persona}")
st.markdown("---")

# --- 4. THE BRAIN CONNECTION ---
api_key = st.text_input("Enter your Google Gemini API Key to activate the AI:", type="password")

if api_key:
    client = genai.Client(api_key=api_key) 

    # --- 5. THE CHAT INTERFACE ---
    user_question = st.text_area("Ask your physics, chemistry, or math question:")
    
    if st.button("Ask Tutor") and user_question:
        
        # --- 6. THE BOUNCER LOGIC ---
        system_rules = f"""
        You are a highly focused, expert tutor for an Indian student in {academic_phase} preparing for {primary_goal}.
        Your teaching style must strictly be: {tutor_persona}.
        
        CRITICAL RULES:
        1. You are strictly an academic tutor. 
        2. You must ONLY answer questions related to Physics, Chemistry, and Mathematics.
        3. If the user asks about movies, video games, general chatting, code formatting, or anything outside the PCM syllabus, you must aggressively refuse and tell them to get back to studying.
        """
        
        combined_prompt = f"{system_rules}\n\nStudent Question: {user_question}"
        
        # --- 7. TALKING TO THE AI ---
        with st.spinner("Analyzing question..."):
            try:
                response = client.models.generate_content(model= 'gemini-2.5-flash',contents=user_question)
                st.markdown("### 💡 Tutor Response:")
                st.info(response.text)
            except Exception as e:
                st.error(f"API Error. Check your key or try again. Details: {e}")
else:
    st.warning("Please enter your API key to wake up the AI tutor.")