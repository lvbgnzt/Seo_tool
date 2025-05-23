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

def process_csv(file, firecrawl_token, chatgpt_token, additional_info, url_column, generate_title=True, generate_description=True):
    df = pd.read_csv(file)
    app = FirecrawlApp(api_key=firecrawl_token)
    results = []
    for url in df[url_column]:
        print(f"Processing URL: {url}")
        result = app.scrape_url(url, formats=["markdown", "html"])
        print(result)
        prompt_parts = ["Erstelle"]
        if generate_title:
            prompt_parts.append("einen Meta-Titel")
        if generate_description:
            if generate_title:
                prompt_parts.append("und")
            prompt_parts.append("eine Meta-Beschreibung")
        prompt_parts.append("für die folgende Seite:\n\n" + result.markdown)
        prompt = " ".join(prompt_parts)

        client = OpenAI(api_key=chatgpt_token)
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        text = completion.choices[0].message.content

        result_dict = {
            "url": url,
            "markdown": result.markdown
        }
        if generate_title:
            title = text.split("Meta-Beschreibung:")[0].replace("Meta-Titel:", "").strip() if "Meta-Beschreibung:" in text else text.strip()
            result_dict["meta_title"] = title
        if generate_description and "Meta-Beschreibung:" in text:
            description = text.split("Meta-Beschreibung:")[1].strip()
            result_dict["meta_description"] = description
        results.append(result_dict)

    return pd.DataFrame(results)
    

def run_metadata_workflow(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column):
    process_csv(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column)