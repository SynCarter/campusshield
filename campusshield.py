import streamlit as st
import json
import os
import uuid
from datetime import datetime

DATA_FILE = "data.json"

# Ensure file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("✅ Data successfully written to", DATA_FILE)
    except Exception as e:
        print("❌ Failed to write data:", e)

# UI Starts
st.title("🛡️ CampusShield – Anonymous Complaint Portal")
st.markdown("Welcome to **CampusShield** 👋\n\n_An anonymous platform to safely report campus issues like harassment, ragging, or mental health concerns._\n\nYour identity is never tracked.")

# Complaint form
with st.form("complaint_form", clear_on_submit=True):
    category = st.selectbox("Category", ["Harassment", "Ragging", "Mental Health", "Discrimination", "Other"])
    details = st.text_area("What happened?")
    submit = st.form_submit_button("🚨 Submit Complaint")

    if submit:
        if details.strip() == "":
            st.warning("Please enter some details.")
        else:
            complaint = {
                "id": str(uuid.uuid4())[:8],
                "category": category,
                "details": details.strip(),
                "timestamp": str(datetime.now())
            }
            data = load_data()
            data.append(complaint)
            save_data(data)
            st.success(f"✅ Complaint submitted successfully! Reference ID: `{complaint['id']}`")
            st.json(complaint)

# Show recent complaints
st.markdown("---")
st.subheader("📂 Recent Complaints (Anonymous View)")

all_complaints = load_data()
if not all_complaints:
    st.info("No complaints submitted yet.")
else:
    for c in reversed(all_complaints[-5:]):
        st.markdown(f"**🗂️ Category:** {c['category']}  \n🕒 _{c['timestamp']}_  \n🆔 ID: `{c['id']}`")
        st.code(c['details'])
        st.markdown("---")

# Footer
st.markdown("---")
st.caption("🔒 Made with ❤️ for the VibeCode Hackathon 2025")
