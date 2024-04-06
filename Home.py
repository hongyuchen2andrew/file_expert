import streamlit as st
import openai
import os
from streamlit_chatbox import *
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

with st.sidebar:
    st.subheader('Start to chat with ReadingExpert!')
    in_expander = st.checkbox('show messages in expander', True)
    show_history = st.checkbox('show history', False)
    st.divider()
    btns = st.container()
    OPENAI_API_KEY = st.text_area(label = 'OPENAI_API_KEY', placeholder = 'Please enter your OpenAI API key...')
    FILE_PATH = st.text_area(label = 'FILE_PATH', placeholder = 'Please enter your file path...')

st.session_state.OPENAI_API_KEY = OPENAI_API_KEY
st.session_state.FILE_PATH = FILE_PATH


if (st.session_state.OPENAI_API_KEY == '') or (st.session_state.FILE_PATH == ''):
    st.error("Please input your API Key and file path in the sidebar")
    st.stop()
else:
    documents = SimpleDirectoryReader(FILE_PATH).load_data()
    index = VectorStoreIndex.from_documents(documents)

    st.title("ReadingExpert")
    chat_box = ChatBox()

    chat_box.init_session()
    chat_box.output_messages()

    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        chat_box.ai_say(
            [
                Markdown(response, in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )

    if btns.button("Clear history"):
        chat_box.init_session(clear=True)
        st.rerun()

    if btns.button("Start a new conversation"):
        chat_box.init_session(clear=True)
        st.session_state.recording = []
        st.rerun()

    if show_history:
        st.write(chat_box.history)