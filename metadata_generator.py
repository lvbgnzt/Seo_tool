import streamlit as st
import pandas as pd
import requests

import io
from openai import OpenAI

def fetch_markdown(url, firecrawl_token):
    headers = {"Authorization": f"Bearer {firecrawl_token}"}
    response = requests.post("https://api.firecrawl.dev/v1/scrape", json={"url": url, "markdown": True}, headers=headers)
    print(f"Fetched markdown from URL: {url}")
    return response.json()

def generate_meta_data(firecrawl_response, additional_info, chatgpt_token, url):
    prompt = f"""Erstelle Meta-Titel und Meta-Beschreibung für folgende Seite: {url}
Firecrawl-Antwort:
{firecrawl_response}

{additional_info}
---
Gib das Ergebnis in folgendem Format zurück:
Meta-Titel: ...
Meta-Beschreibung: ..."""
    client = OpenAI(api_key=chatgpt_token)
    print("Generating meta data with GPT-4")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print("Received response from OpenAI")
    output = completion.choices[0].message.content
    title, description = "", ""
    for line in output.split("\n"):
        if line.lower().startswith("meta-titel"):
            title = line.split(":", 1)[1].strip()
        elif line.lower().startswith("meta-beschreibung"):
            description = line.split(":", 1)[1].strip()
    return title, description, prompt

def process_csv(file, firecrawl_token, chatgpt_token, additional_info, url_column):
    df = pd.read_csv(file)
    results = []
    for url in df[url_column]:
        print(f"Processing URL: {url}")
        result = fetch_markdown(url, firecrawl_token)
        title, desc, prompt = generate_meta_data(result, additional_info, chatgpt_token, url)
        results.append({
            "url": url,
            "meta_title": title,
            "meta_description": desc,
            "prompt": prompt,
            "firecrawl_raw": result
        })
        print(f"Generated metadata for: {url}")
    return pd.DataFrame(results)
    

def run_metadata_workflow(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column):
    result_df = process_csv(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column)
    st.dataframe(result_df)
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Ergebnisse als CSV herunterladen", data=csv, file_name="meta_daten.csv", mime="text/csv")