import streamlit as st

st.title("🧪 Simple Test App")
st.write("If you can see this, Streamlit is working!")
st.success("✅ Basic Streamlit functionality confirmed")

if st.button("Test Button"):
    st.balloons()
    st.write("Button clicked successfully!")