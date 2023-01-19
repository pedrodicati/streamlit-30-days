import streamlit as st

st.header("Select Box")

color = st.selectbox(
    'Select your favorite color:',
    ['Red', 'Green', 'Blue', 'Yellow', 'Black', 'White', 'Purple']
)

st.write("Your favorite color is:", color)
