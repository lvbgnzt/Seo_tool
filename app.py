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
    firecrawl_token = st.text_input("Firecrawl API Token", type="password")
    chatgpt_token = st.text_input("OpenAI GPT Token", type="password")
    uploaded_file = st.file_uploader("CSV-Datei mit URLs hochladen", type="csv")
    title = st.text_input("Seitentitel")
    description = st.text_area("Beschreibung")
    if st.button("Meta-Daten generieren"):
        if uploaded_file is not None and firecrawl_token and chatgpt_token:
            st.info("Meta-Daten werden generiert...")
            # Hier wird später die Meta-Daten-Logik integriert
        else:
            st.warning("Bitte lade eine CSV hoch und gib beide Tokens ein.")

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