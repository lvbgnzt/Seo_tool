import streamlit as st
import pandas as pd
import requests
import json

import io
from openai import OpenAI
from firecrawl import FirecrawlApp

def fetch_markdown(url, firecrawl_token):
    app = FirecrawlApp(api_key=firecrawl_token)
    result = app.scrape_url(url, formats=["markdown", "html"])
    print(f"Fetched markdown from URL: {url}")
    return result.data

def process_csv(file, firecrawl_token, chatgpt_token, additional_info, url_column):
    df = pd.read_csv(file)
    results = []
    for url in df[url_column]:
        print(f"Processing URL: {url}")
        result = fetch_markdown(url, firecrawl_token)
        results.append({
            "url": url,
            "firecrawl_raw": json.dumps(result)
        })
        print(f"Generated metadata for: {url}")
    return pd.DataFrame(results)
    

def run_metadata_workflow(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column):
    result_df = process_csv(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column)
    st.dataframe(result_df)
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Ergebnisse als CSV herunterladen", data=csv, file_name="meta_daten.csv", mime="text/csv")