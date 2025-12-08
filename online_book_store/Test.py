import streamlit as st

# This goes in the main body
st.write("This is the main content area.")

# These go in the sidebar
st.sidebar.title("My Sidebar")
st.sidebar.button("Click Me")

with st.sidebar:
    st.radio("Choose an option", ["A", "B", "C"])
