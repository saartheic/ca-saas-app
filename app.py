import streamlit as st
import pandas as pd

# ---- INIT SESSION ----
if "login" not in st.session_state:
    st.session_state["login"] = False

if "user" not in st.session_state:
    st.session_state["user"] = ""

# ---- LOGIN SCREEN ----
if not st.session_state["login"]:

    st.title("CA SaaS Login")

    users = pd.read_excel("users.xlsx")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = users[
            (users["Username"].astype(str).str.strip().str.lower() == username.strip().lower()) &
            (users["Password"].astype(str).str.strip() == password.strip())
        ]

        if not user.empty:
            st.session_state["login"] = True
            st.session_state["user"] = username.strip()
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid Login")

# ---- DASHBOARD ----
else:

    st.title("CA Dashboard")
    st.write(f"Welcome {st.session_state['user']}")

    # ---- LOAD DATA ----
    data = pd.read_excel("clients.xlsx")
    data["Due Date"] = pd.to_datetime(data["Due Date"])

    # ---- USER FILTER ----
    current_user = st.session_state["user"]

    if current_user.lower() != "admin":
        data = data[
            data["Owner"].astype(str).str.strip().str.lower() == current_user.lower()
        ]

    # ---- SHOW DATA ----
    st.write("### Client Data")
    st.dataframe(data)

    # ---- SUMMARY ----
    total = len(data)
    pending = len(data[data["Status"] == "Pending"])
    overdue = len(
        data[(data["Due Date"] < pd.Timestamp.today()) & (data["Status"] == "Pending")]
    )

    st.write("### Summary")
    st.write("Total Clients:", total)
    st.write("Pending:", pending)
    st.write("Overdue:", overdue)

    # ---- LOGOUT BUTTON ----
    if st.button("Logout"):
        st.session_state["login"] = False
        st.session_state["user"] = ""
        st.rerun()