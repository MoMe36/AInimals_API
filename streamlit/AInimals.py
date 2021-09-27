from os import path
import streamlit as st
import random
import numpy as np
from PIL import Image

st.title('AInimals &#128038')

st.subheader('Upload du fichier sonore')
file = st.file_uploader("Choisis un fichier .wav")

if file != None:
    st.subheader('Votre enregistrement &#127908')
    audio_bytes = file.read()
    st.audio(audio_bytes, format='audio/wav')

st.subheader('Sélection des paramètres')
window = st.slider('Taille de la fenêtre', 1, 10, 5)  # min: 0h, max: 23h, default: 17h
start = st.slider('Position de départ', 0.0, 300.0, 150.0, 0.1)  # min: 0h, max: 23h, default: 17h

st.subheader('Prédictions')

#model = m.AInimalsModel()
#pred = model.get_preds(audio_path=file, start_at=start, window=window)

pred = [random.randint(0,100) for i in range(15)]

st.bar_chart(pred)

image = Image.open('800px-Turaco_crestimorado_(Tauraco_porphyreolophus),_parque_nacional_Kruger,_Sudáfrica,_2018-07-26,_DD_33.jpg')

st.subheader('Votre oiseau &#128064')

st.image(image, caption='Tauraco porphyreolophus')