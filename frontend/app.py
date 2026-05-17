# frontend/app.py

import requests
import streamlit as st

st.set_option(
    'client.showErrorDetails',
    False
)

BACKEND_NAME = "Hasanah Mart RAG API"

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

API_URL = (
    "https://ecommerce-ai-assistant-rvqu.onrender.com/chat/ask/"
)


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Hasanah Mart AI",
    page_icon="💬",
    layout="centered"
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Hasanah Mart AI Assistant")

st.markdown(
    "Ask questions about Hasanah Mart products."
)


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------------------------------------
# RENDER CHAT HISTORY
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

try:

    health_response = requests.get(
        "https://ecommerce-ai-assistant-rvqu.onrender.com/health",
        timeout=10
    )

    if health_response.status_code == 200:

        st.success(
            f"{BACKEND_NAME} connected"
        )

    else:

        st.warning(
            "Backend reachable but unhealthy."
        )

except Exception:

    st.error(
        "Backend API is currently unavailable."
    )

    st.stop()

query = st.chat_input(
    "Type your question..."
)


# ---------------------------------------------------
# HANDLE CHAT
# ---------------------------------------------------

if query:

    # ---------------------------------------------
    # STORE USER MESSAGE
    # ---------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })


    # ---------------------------------------------
    # DISPLAY USER MESSAGE
    # ---------------------------------------------

    with st.chat_message("user"):

        st.markdown(query)


    # ---------------------------------------------
    # ASSISTANT RESPONSE
    # ---------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    API_URL,

                    json={
                        "query": query,
                        "top_k": 5,
                        "include_sources": True
                    },

                    timeout=60
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No answer found."
                )

                # ---------------------------------
                # DISPLAY ANSWER
                # ---------------------------------

                st.markdown(answer)


                # ---------------------------------
                # STORE ASSISTANT MESSAGE
                # ---------------------------------

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })


                # ---------------------------------
                # DISPLAY SOURCES
                # ---------------------------------

                # sources = data.get(
                #     "sources",
                #     []
                # )

                # if sources:

                #     with st.expander(
                #         "Sources"
                #     ):

                #         for source in sources:

                #             st.markdown(
                #                 f"""
                #                 ### Source Information

                #                 **Source:**  
                #                 {source['source']}

                #                 **Chunk ID:**  
                #                 {source['chunk_id']}

                #                 **Distance:**  
                #                 {source['distance']:.4f}

                #                 **Preview:**  
                #                 {source['preview']}
                #                 """
                #             )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"API Request Failed:\n\n{str(e)}"
                )

            except Exception as e:

                st.error(
                    f"Unexpected Error:\n\n{str(e)}"
                )