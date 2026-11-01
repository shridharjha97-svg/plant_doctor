"""Run with: streamlit run app.py"""
import hashlib

import streamlit as st

from src import config

st.set_page_config(page_title="Plant Doctor", page_icon="🌿")
st.title("🌿 Plant Doctor")

# Stop early with a readable message if .env or the model files are not set up
problems = config.problems()
if problems:
    st.error("\n\n".join(problems))
    st.stop()

from src import chat  # noqa: E402  (imports TensorFlow, so only after the check above)

if "messages" not in st.session_state:
    st.session_state.messages = []


def new_image(file, key):
    """Return the image bytes only the first time a given photo is seen.

    st.camera_input and st.file_uploader keep returning the same photo on every
    rerun, so without this a photo would be scanned again after each chat message.
    """
    if file is None:
        return None
    data = file.getvalue()
    digest = hashlib.md5(data).hexdigest()
    if st.session_state.get(key) == digest:
        return None
    st.session_state[key] = digest
    return data


# --- Scanner: the camera starts as soon as the page opens (the browser asks for permission) ---
st.subheader("Scan a leaf")
st.caption("Allow camera access, point it at one leaf and press Take Photo.")
camera_photo = st.camera_input("Camera", label_visibility="collapsed")
with st.expander("Or upload a photo instead"):
    uploaded_photo = st.file_uploader("Leaf photo", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

scan = new_image(camera_photo, "last_camera") or new_image(uploaded_photo, "last_upload")

# --- Conversation ---
st.divider()
col_title, col_clear = st.columns([4, 1])
col_title.subheader("Chat")
if col_clear.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

if not st.session_state.messages and not scan:
    st.info("Scan a leaf above, or type a farming question below.")

# Replay the conversation on every rerun
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("image"):
            st.image(m["image"], width=220)
        st.markdown(m["content"])

typed = st.chat_input("Ask a farming question...")

if scan or typed:
    text = (typed or "").strip()
    image = scan
    shown = text or "Scanned a leaf photo"

    # Text-only copy of the earlier messages, taken before adding the new one
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    st.session_state.messages.append({"role": "user", "content": shown, "image": image})
    with st.chat_message("user"):
        if image:
            st.image(image, width=220)
        st.markdown(shown)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            answer = chat.reply(text, image, history)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
