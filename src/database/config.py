import streamlit as st
from supabase import create_client, Client

supabase: Client = create_client(
    st.secrets["https://wgyorgzfdhvvrbsrlklm.supabase.co"],
    st.secrets["SUPABASE_KEY"]
)
