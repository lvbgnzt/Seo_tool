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
    return result

def process_csv(file, firecrawl_token, chatgpt_token, additional_info, url_column):
    df = pd.read_csv(file)
    app = FirecrawlApp(api_key=firecrawl_token)
    results = []
    for url in df[url_column]:
        print(f"Processing URL: {url}")
        result = app.scrape_url(url, formats=["markdown", "html"])
        print(result)
        prompt = f"Erstelle einen Meta-Titel und eine Meta-Beschreibung für die folgende Seite:\n\n{result.markdown}"
        client = OpenAI(api_key=chatgpt_token)
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        text = completion.choices[0].message.content
        title, description = text.split("Meta-Beschreibung:", 1)
        title = title.replace("Meta-Titel:", "").strip()
        description = description.strip()
        results.append({
            "url": url,
            "markdown": result.markdown,
            "meta_title": title,
            "meta_description": description
        })
    return pd.DataFrame(results)
    

def run_metadata_workflow(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column):
    process_csv(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column)