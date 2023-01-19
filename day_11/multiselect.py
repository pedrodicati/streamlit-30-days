import streamlit as st

st.header("Multi-Select Box")

colors = st.multiselect(
    'Select your favorite color:',
    ['Red', 'Green', 'Blue', 'Yellow', 'Black', 'White', 'Purple'],
    ['Red', 'Green', 'Blue']
)

colors = ", ".join(colors)

st.write("Your favorite colors are:", colors)