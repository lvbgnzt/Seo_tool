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
    for url in df[url_column]:
        print(f"Processing URL: {url}")
        result = app.scrape_url(url, formats=["markdown", "html"])
        print(result)
    

def run_metadata_workflow(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column):
    process_csv(uploaded_file, firecrawl_token, chatgpt_token, additional_info, url_column)