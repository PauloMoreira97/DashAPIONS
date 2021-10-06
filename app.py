import streamlit as st
from multiapp import MultiApp
from apps import home, dashhidrologica# import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Configuração de Conexão API/ONS", home.app)
app.add_app("Dash Hidrológica", dashhidrologica.app)
# The main app
app.run()