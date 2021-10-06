import streamlit as st
import pandas as pd
import numpy as np
import time
from data import glVar
import MySQLdb
import matplotlib.pyplot as plt
import requests
import json


def app():
    glVar.initialize()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:   
        st.title('API ONS')
        st.write("")
        st.write("")
        st.write("Dados para conexão na API")
        st.write("")
        st.write("")
        glVar.strUser = st.text_input('Usuário')
        glVar.strPass = st.text_input('senha', type="password")
        
        if st.button("Login", key=None, help=None, on_click=None, args=None, kwargs=None):
            doAutenticar()
        else:
            st.caption('Faça Login')
    with col3: 
        st.write("")
        
    st.stop()

def doAutenticar():
    url = 'https://integra.ons.org.br/api/autenticar'
    payload = {"usuario": glVar.strUser,"senha": glVar.strPass}
    headers = {"accept": "application/json","Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    if str(r) == "<Response [200]>":
        data = json.loads(r.content)
        glVar.strToken = "bearer " + data['access_token']
        glVar.strRefreshToken = (data['refresh_token'])
        st.write("")
        st.write("")
        st.write("Seu Token Foi Gerado Com Sucesso")
    else:
        st.write("ERROR no login")



    
 