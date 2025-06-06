import streamlit as st
import json

# Load decision tree
with open("emergency_decision_tree.json", "r") as f:
    tree = json.load(f)

# Initialize session state
if "current_node" not in st.session_state:
    st.session_state.current_node = "start"
if "history" not in st.session_state:
    st.session_state.history = []

def reset():
    st.session_state.current_node = "start"
    st.session_state.history = []

def render_node(node_key):
    node = tree[node_key]
    st.markdown("### " + node["question"])

    if "options" in node:
        for opt_key, opt in node["options"].items():
            if st.button(f"{opt_key}. {opt['label']}"):
                if "next" in opt:
                    st.session_state.current_node = opt["next"]
                    st.session_state.history.append((node_key, opt_key))
                elif "result" in opt:
                    st.session_state.current_node = "result"
                    st.session_state.result = opt["result"]
    elif node_key == "result":
        res = st.session_state.result
        st.success(f"**Condition:** {res['condition']}")
        st.info("**Assessment:** " + ", ".join(res["assessment"]))
        st.warning("**Action:** " + ", ".join(res["action"]))
        st.button("Start Over", on_click=reset)

# App Title
st.title("🩺 Emergency CDSS - Rule-Based")

# Reset button
st.button("🔁 Restart", on_click=reset)

# Render current node
render_node(st.session_state.current_node)

