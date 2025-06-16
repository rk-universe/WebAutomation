import streamlit as st
from dotenv import load_dotenv
import os
from Modules.BrowserDriver import connect_to_existing_chrome_session
from Modules.GetHTML import fetch_html_content, get_page_description
from Modules.ClickOnElements import perform_action
from Modules.Langchain import format_prompt
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser

# Set Streamlit page config
st.set_page_config(page_title="LLM Browser Agent", layout="wide")

# Initialize session state
if "memory_data" not in st.session_state:
    st.session_state.memory_data = []
if "running" not in st.session_state:
    st.session_state.running = False
if "driver" not in st.session_state:
    st.session_state.driver = None

load_dotenv(dotenv_path="apikey.env")
# LangChain setup
model = ChatNVIDIA(model="meta/llama3-70b-instruct")
parser = StrOutputParser()

# App UI
st.title("🧠 LLM Browser Automation Agent")
user_prompt = st.text_input("📌 Enter your goal (e.g., 'Open Gmail and login')")

col1, col2 = st.columns([1, 1])
start_clicked = col1.button("🚀 Start Automation", use_container_width=True)
stop_clicked = col2.button("🛑 Force Stop", use_container_width=True)

# Handle start
if start_clicked and user_prompt:
    st.session_state.running = True
    st.session_state.user_prompt = user_prompt
    st.session_state.memory_data = []

    if not st.session_state.driver:
        with st.spinner("Connecting to Chrome..."):
            st.session_state.driver = connect_to_existing_chrome_session(os.getenv("BROWSER"))
        st.success("Connected to browser!")
        
    try:
        st.session_state.driver.get("https://www.google.com")
        st.toast("🌐 Navigated to Google.com", icon="🌍")
    except Exception as e:
        st.error(f"Failed to load Google: {e}")

# Handle force stop
if stop_clicked:
    st.session_state.running = False
    st.warning("⛔ Force stop activated.")

# Perform one iteration of the loop
if st.session_state.running:
    driver = st.session_state.driver
    user_prompt = st.session_state.user_prompt

    with st.spinner("🔍 Fetching page content..."):
        stored_results = fetch_html_content(driver)
        current_page = get_page_description(driver)

    prompt_text = format_prompt(
        user_prompt=user_prompt,
        stored_results=stored_results,
        current_page=current_page,
        memory_data="\n".join(f"{m['page_title']} -> {m['actions']}" for m in st.session_state.memory_data)
    )

    with st.expander("🧾 Prompt Sent to Model"):
        st.code(prompt_text)

    response = model.invoke(prompt_text)
    parsed = parser.invoke(response)

    st.info(f"🤖 Model Response: `{parsed}`")

    # If model says "done", stop loop
    if "done" in parsed.lower():
        st.success("✅ Goal achieved. Stopping automation.")
        st.session_state.running = False
    else:
        perform_action(driver, parsed)
        st.session_state.memory_data.append({
            "page_title": current_page,
            "actions": parsed
        })
        st.toast(f"✅ Action performed: {parsed}", icon="🖱️")

    # Automatically rerun the next step
    st.rerun()
