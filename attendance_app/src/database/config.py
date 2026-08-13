import streamlit as st
from supabase import create_client, Client
import sys

# Check if secrets exist
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("Supabase configuration is missing. Please configure .streamlit/secrets.toml.")
    st.stop()

# Check if placeholders are still present
if st.secrets["SUPABASE_URL"] == "your_supabase_url_here" or st.secrets["SUPABASE_KEY"] == "your_supabase_key_here":
    st.error("Supabase configuration is using placeholder values. Please update .streamlit/secrets.toml with your actual credentials.")
    st.stop()

try:
    supabase: Client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception as e:
    st.error(f"Failed to initialize Supabase client: {e}")
    st.stop()