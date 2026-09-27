import streamlit as st
from supabase import create_client, Client

supabase: Client = create_client(
    st.secrets["https://wgyorgzfdhvvrbsrlklm.supabase.co"],
    st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndneW9yZ3pmZGh2dnJic3Jsa2xtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA1MTQyNjAsImV4cCI6MjEwNjA5MDI2MH0.sVtOeuJu4IwpgKJik0ortlu9sIZHN75PYB76PWw0xv4"]
)
