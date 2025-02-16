# utils.py

import streamlit as st
from functools import lru_cache

@lru_cache(maxsize=32)
def cached_api_call(url):
    """
    Caches API call responses.
    """
    response = st.experimental_get_query_params()  # Replace with proper caching if needed.
    return response

def render_banner(image_url, caption=""):
    """
    Renders a banner image.
    """
    st.image(image_url, caption=caption, use_column_width=True)
