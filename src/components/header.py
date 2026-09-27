import streamlit as st
from src.ui.base_layout import style_base_layout


def header_home():
    st.markdown(
        """
        <div style="text-align:center; padding: 0.5rem 0 1rem;">
            <div style="width:48px; height:48px; background:var(--blue-50); border-radius:12px; display:inline-flex; align-items:center; justify-content:center; margin-bottom:0.5rem;">
                <span class="material-symbols-outlined" style="color:var(--blue-600); font-size:28px;">school</span>
            </div>
            <h1 style="margin:0; color:var(--blue-900); font-size:2.1rem; font-weight:800; letter-spacing:-0.02em;">
                Swagyo
            </h1>
            <p style="color:var(--gray-600); font-size:0.95rem; margin:0.3rem 0 0;">
                AI-powered attendance system for modern classrooms
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def navbar(hide_actions: bool = False):
    style_base_layout()

    st.markdown(
        """
        <div class="va-navbar">
            <div class="va-navbar-brand">
                <span class="material-symbols-outlined" style="color:var(--blue-600); font-size:24px;">school</span>
                <span>Swagyo</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _navbar_actions(hide_actions)


def _navbar_actions(hide_actions: bool = False):
    if hide_actions:
        return

    _, action_col = st.columns([5, 1])
    with action_col:
        if 'teacher_data' in st.session_state and st.session_state.get('user_role') == 'teacher':
            if st.button("Logout", key='logout', type='secondary', icon=":material/logout:"):
                del st.session_state.teacher_data
                st.session_state.user_role = None
                st.session_state.is_logged_in = False
                st.session_state['login_type'] = None
                st.rerun()

        elif 'student_data' in st.session_state and st.session_state.get('user_role') == 'student':
            if st.button("Logout", key='logout', type='secondary', icon=":material/logout:"):
                del st.session_state.student_data
                st.session_state.user_role = None
                st.session_state.is_logged_in = False
                st.session_state['login_type'] = None
                st.rerun()

        else:
            if st.button("Get started", key='get_started_btn', icon=":material/arrow_forward:"):
                st.session_state['login_type'] = 'choose'
                st.rerun()


def back():
    if st.button("Back", key='back_btn', icon=":material/arrow_back:"):
        st.session_state['login_type'] = None
        st.rerun()
