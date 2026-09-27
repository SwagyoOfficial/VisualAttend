import streamlit as st

def footer():
    st.markdown(
        """
        <div class="va-footer">
            <p>Swagyo &nbsp;·&nbsp; AI-Powered Attendance System</p>
            <p style="margin-top:0.3rem;">
                Contact: <a href="mailto:contact@swagyo.com">contact@swagyo.com</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
