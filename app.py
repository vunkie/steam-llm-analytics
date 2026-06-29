import streamlit as st
from main import resolve_vanity_url, fetch_steam_data, fill_database, run_prompt

@st.cache_resource
def load_data(steam_id):
    data = fetch_steam_data(steam_id)
    if data is None:
        return None
    session = fill_database(data)
    return session

st.title("Steam Library Analytics")

if "session" not in st.session_state:
    with st.form("steam_form"):
        vanity = st.text_input("Type your Steam ID or URL").strip().rstrip("/").split("/")[-1]
        submitted = st.form_submit_button("Submit")

    if submitted:
        if vanity:
            if vanity.isdigit() and len(vanity) == 17:
                steam_id = vanity
            else:
                success,result = resolve_vanity_url(vanity)
                if not success:
                    st.error(result)
                    st.stop()
                else:
                    steam_id = result
                
            with st.spinner("Loading..."):
                session = load_data(steam_id)
                if session is None:
                    st.error("Steam library not found. Profile may be private or have no games.")
                else:
                    st.session_state["session"] = session
                    st.session_state["loaded"] = True
                    st.rerun()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "loaded"in st.session_state:
    st.success("Successful! You can now ask questions about your Steam library.")
    
if "session" in st.session_state:
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])

    prompt = st.chat_input("Type your prompt here")
    if prompt:
        if "loaded" in st.session_state:
            del st.session_state["loaded"]
        
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        answer = run_prompt(st.session_state["session"], prompt)
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)


