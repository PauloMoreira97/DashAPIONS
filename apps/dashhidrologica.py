import streamlit as st
import numpy as np
import pandas as pd
from data import glVar
import datetime
import time
import requests
import matplotlib.pyplot
import json



def app():
    varVerificaButton = 0 
    st.title('Visualização dados Hidrológicos')
    st.write("")
    st.write("")
    
    if glVar.strToken == "VAZIO":
        st.write("Para Continuar:      Faça o login na Pagina Configuração de Conexão API/ONS")
        st.stop()
        
    col1, col2, col3 = st.columns(3)
    with col1:
        IPTstrDateInicio = st.date_input('Data de Entrada', datetime.date(2020,1,1))
        IPTstrDateFim = st.date_input('Data Fim', datetime.date(2021,1,1))
    with col2:
        IPTstrOrigem  = st.selectbox('Origem dos dados',['TRL', 'SSC', 'FTP','ATR'])
        IPTstrIntervalo  = st.selectbox('Intervalo de consolidacao dos dados',['HO','DI'])


    with col3:
        IPTstrReservatorio = st.selectbox('Reservatório',doPegarNomesReservatorio(), index=5)
        strIdentificador= doDeterminarIdentificadorReservatorio(IPTstrReservatorio)
        IPTstrDadoBuscado = st.selectbox('Dado Desejado',['afluencia','defluencia','energiaTurbinavel','nivelJusante','nivelMontante','vazaoOutrasEstruturas','vazaoTurbinada','vazaoVertida','volumeUtil'])

    IPTstrQuantidadeDados = st.slider('Quantidade de Dados', 1, 250, 100)   
    IPTstrPagina = st.slider('Pagina de Dados', 1, 100, 1)
    
    col21, col22, col23 = st.columns(3)
    with col21:
        st.write("")
    with col22:
        if st.button('Acessar Dados'):
            varVerificaButton='1' 
    with col23:
        st.write("")
        
    if varVerificaButton=='1':
                 doAcessarDados(IPTstrDateInicio,IPTstrDateFim,IPTstrQuantidadeDados,IPTstrPagina,IPTstrIntervalo,IPTstrOrigem,strIdentificador,IPTstrDadoBuscado)
    st.stop()
    
    
    
def doPegarNomesReservatorio():
    strReservatorio = []
    url = 'https://integra.ons.org.br/api/hidrologia/reservatorios'
    headers = {"accept": "application/json","Content-Type": "application/json","Authorization":glVar.strToken,"Quantidade":"240","Pagina":"1"}
    r = requests.get(url, headers=headers)
    if str(r) == "<Response [200]>":
        data = json.loads(r.content)
        for i in range(len(data['Resultados'])):
            strReservatorio.append(data['Resultados'][i]["NomeCurto"])#Identificador
        return strReservatorio        
    else:
        strReservatorio = 'erro ao consultar reservatórios'
        return strReservatorio
    
def doDeterminarIdentificadorReservatorio(strNomeCurtoEscolhido):

    strIndex = doPegarNomesReservatorio().index(strNomeCurtoEscolhido)
    strIdentificador = []
    url = 'https://integra.ons.org.br/api/hidrologia/reservatorios'
    headers = {"accept": "application/json","Content-Type": "application/json","Authorization":glVar.strToken,"Quantidade":"240","Pagina":"1"}
    r = requests.get(url, headers=headers)
    if str(r) == "<Response [200]>":
        data = json.loads(r.content)
        for i in range(len(data['Resultados'])):
            strIdentificador.append(data['Resultados'][i]["Identificador"])
        return strIdentificador[strIndex]        
    else:
        strIdentificador = 'erro ao consultar identificador'
        return strIdentificador
    
    
def doAcessarDados(strDateInicio,strDateFim,strQuantidade,strPagina,strIntervalo,strOrigem,strIdent,strdadoEscolhido):    
    strDadosDt = []
    strDadosVl = []
    url = 'https://integra.ons.org.br/api/hidrologia/reservatorios/' + strIdent + '/'+ strdadoEscolhido +'?Inicio='+ str(strDateInicio)+'%2000%3A00%3A00'+ '&Fim=' + str(strDateFim) +'%2000%3A00%3A00' + '&Intervalo='+ strIntervalo + '&Origem=' + strOrigem
    headers = {"accept": "application/json","Content-Type": "application/json","Authorization":glVar.strToken,"Quantidade":str(strQuantidade),"Pagina":str(strPagina)}
    r = requests.get(url, headers=headers)
    if str(r) == "<Response [200]>":
        data = json.loads(r.content)
        for i in range(len(data['Resultados'])):
            strDadosDt.append(data['Resultados'][i]["Instante"])
            strDadosVl.append(data['Resultados'][i]["Valor"])
        chart_data = pd.DataFrame(strDadosVl,strDadosDt, columns= ['Valor'])
        #table_data = pd.DataFrame(strDadosVl,strDadosDt, columns = ['Período','Valor'])
        st.line_chart(chart_data)
        st.table(chart_data)
    else:
        st.write('erro ao consultar dados')