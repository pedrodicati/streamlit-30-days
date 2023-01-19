import streamlit as st

st.header('Checkbox')

st.write('O que você quer pedir?')

if st.checkbox('Pizza'):
    st.write('Hm, uma pizza é boa!')
if st.checkbox('Hamburguer'):
    st.write('Hm, um hamburguer é bom!')
if st.checkbox('Batata frita'):
    st.write('Hm, uma batata frita é boa!')
if st.checkbox('Suco'):
    st.write('Hm, um suco é bom!')
if st.checkbox('Água'):
    st.write('Hm, água é boa!')
if st.checkbox('Refrigerante'):
    st.write('Hm, um refrigerante é bom!')