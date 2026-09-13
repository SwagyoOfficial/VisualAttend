import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_to_subject
import time

@st.dialog("Join Class")
def auto_enroll_dialog(join_code):
    student_data = st.session_state.student_data
    st.markdown(
        f"You have been invited to join a class.  \n"
        f"Class code: **`{join_code}`**  \n\n"
        "Would you like to enroll?"
    )
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enroll Now", type="primary", width="stretch"):
            if join_code:
                try:
                    res = supabase.table("subjects").select("subject_id, name, subject_code").eq("subject_code", join_code).execute()
                    if res and res.data:
                        subject = res.data[0]
                        student_id = student_data["student_id"]

                        check = supabase.table("subject_students").select("*").eq('subject_id', subject["subject_id"]).eq("student_id", student_id).execute()

                        if check and check.data:
                            st.info("You are already enrolled in this class.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            enroll_to_subject(student_id, subject['subject_id'])
                            st.toast("Successfully enrolled in class.")
                            time.sleep(1)
                            st.query_params.clear()
                            st.rerun()
                    else:
                        st.warning("Invalid join code.")
                except Exception as e:
                    st.error(f"Unable to enroll right now: {e}")
    with col2:
        if st.button("No Thanks", width="stretch"):
            st.query_params.clear()
            st.rerun()