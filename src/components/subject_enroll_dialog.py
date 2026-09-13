import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_to_subject
import time

@st.dialog("Enroll in Class")
def subject_enroll_dialog():
    student_data = st.session_state.student_data
    join_code = st.text_input("Subject Code", placeholder='Enter class code')
    if st.button("Enroll Now", type='primary', width="stretch"):
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
                        st.toast("Successfully enrolled!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning("Invalid subject code. Please double-check and try again.")
            except Exception as e:
                st.error(f"Unable to enroll right now: {e}")
        else:
            st.warning("Please enter the subject code.")