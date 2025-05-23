# app.py
import streamlit as st

# Seiten-Titel
st.title("SEO Content Assistant")

# Sidebar mit Auswahlmenü
option = st.sidebar.selectbox(
    "Welche Funktion möchtest du nutzen?",
    ("Meta-Daten erstellen", "Alt-Texte erstellen", "Content erstellen")
)

# Dynamisches Laden des passenden Moduls
if option == "Meta-Daten erstellen":
    st.header("Meta-Daten Generator")
    title = st.text_input("Seitentitel")
    description = st.text_area("Beschreibung")
    if st.button("Meta-Daten generieren"):
        # Platzhalter für Logik
        st.success(f"Meta Title: {title[:60]}...")
        st.info(f"Meta Description: {description[:160]}...")

elif option == "Alt-Texte erstellen":
    st.header("Alt-Text Generator")
    image_desc = st.text_area("Bildbeschreibung oder Bildinhalt eingeben")
    if st.button("Alt-Text generieren"):
        # Platzhalter für Logik
        st.success(f"Alt-Text: Ein Bild von {image_desc.lower()}")

elif option == "Content erstellen":
    st.header("Content Generator")
    topic = st.text_input("Thema oder Keyword")
    if st.button("Content generieren"):
        # Platzhalter für Logik
        st.write("Hier könnte dein AI-generierter Text erscheinen...")