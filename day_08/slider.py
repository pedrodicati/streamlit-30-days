import streamlit as st
from datetime import time, datetime

st.header('st.slider()')

st.subheader('Slider')
age = st.slider('How old are you?', 0, 130, 25) # mensagem, min, max, default
st.write("I'm ", age, 'years old') # escreve a idade

st.subheader('Range Slider')

values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0) # mensagem, min, max, default (defino dois padrões então é um range)
)
st.write('Values:', values)

st.subheader('Range Time Slider')

appointments = st.slider(
    'Schedulet your appointment',
    value=(time(11, 30), time(12, 45)), # mensagem, default (defino dois padrões então é um range)
)
st.write("You're scheduled for", appointments)

st.subheader('Datetime slider')

start_time = st.slider(
    "When do you start?",
    value = datetime(2023, 1, 1, 9, 30),
    format="DD/MM/YY - hh:mm"
)
st.write("Start time:", start_time)

