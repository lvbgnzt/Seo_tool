# app.py
import streamlit as st
from metadata_generator import process_csv
import pandas as pd
import io

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
    st.subheader("Was soll generiert werden?")
    generate_title = st.checkbox("Meta-Titel", value=True)
    generate_description = st.checkbox("Meta-Beschreibung", value=True)
    uploaded_file = st.file_uploader("CSV-Datei mit URLs hochladen", type="csv")
    additional_info = st.text_area("Zusätzliche Informationen (optional)")
    if uploaded_file is not None:
        df_input = pd.read_csv(uploaded_file)
        st.subheader("Vorschau der hochgeladenen Datei")
        st.dataframe(df_input.head())

        url_column = st.selectbox("Wähle die Spalte mit den URLs", df_input.columns)

        if st.button("Meta-Daten generieren"):
            if firecrawl_token and chatgpt_token:
                st.info("Meta-Daten werden generiert...")
                df_results = process_csv(
                    io.StringIO(df_input.to_csv(index=False)),
                    firecrawl_token,
                    chatgpt_token,
                    additional_info,
                    url_column,
                    generate_title,
                    generate_description
                )
                st.success("Meta-Daten erfolgreich generiert!")
                st.dataframe(df_results)

                csv = df_results.to_csv(index=False).encode('utf-8')
                st.download_button("Ergebnisse als CSV herunterladen", csv, "meta_daten.csv", "text/csv")
            else:
                st.warning("Bitte gib beide Tokens ein.")

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