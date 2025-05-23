import streamlit as st
import pandas as pd
import requests
import openai
import io

def fetch_markdown(url, firecrawl_token):
    headers = {"Authorization": f"Bearer {firecrawl_token}"}
    response = requests.post("https://api.firecrawl.dev/v1/scrape", json={"url": url, "markdown": True}, headers=headers)
    print(f"Fetched markdown from URL: {url}")
    return response.json().get("markdown", "")

def generate_meta_data(markdown_text, additional_info, chatgpt_token):
    prompt = f"""Erstelle Meta-Titel und Meta-Beschreibung für folgende Seite:
{additional_info}
---
{markdown_text}
---
Gib das Ergebnis in folgendem Format zurück:
Meta-Titel: ...
Meta-Beschreibung: ..."""
    openai.api_key = chatgpt_token
    print("Generating meta data with GPT-4")
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    print("Received response from OpenAI")
    output = completion["choices"][0]["message"]["content"]
    title, description = "", ""
    for line in output.split("\n"):
        if line.lower().startswith("meta-titel"):
            title = line.split(":", 1)[1].strip()
        elif line.lower().startswith("meta-beschreibung"):
            description = line.split(":", 1)[1].strip()
    return title, description

def process_csv(file, firecrawl_token, chatgpt_token, additional_info):
    df = pd.read_csv(file)
    results = []
    for url in df['url']:
        print(f"Processing URL: {url}")
        md = fetch_markdown(url, firecrawl_token)
        title, desc = generate_meta_data(md, additional_info, chatgpt_token)
        results.append({"url": url, "meta_title": title, "meta_description": desc})
        print(f"Generated metadata for: {url}")
    return pd.DataFrame(results)

def run_metadata_workflow(uploaded_file, firecrawl_token, chatgpt_token, additional_info):
    result_df = process_csv(uploaded_file, firecrawl_token, chatgpt_token, additional_info)
    st.dataframe(result_df)
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Ergebnisse als CSV herunterladen", data=csv, file_name="meta_daten.csv", mime="text/csv")