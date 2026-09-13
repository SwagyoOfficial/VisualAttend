import streamlit as st
from src.database.db import get_teacher_subjects
from src.components.add_photos_dialog import add_photo_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.attendance_result_dialog import attendance_result_dialog
from src.database.config import supabase
from datetime import datetime
import numpy as np
import pandas as pd

def take_attendance() :
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data["id"]
    st.subheader("Take Attendance")

    if 'attendance_images' not in st.session_state :
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects :
        st.info("You haven't created any subjects. Please create one to begin!")
        return
    subject_options = {f"{s['name']} : {s['subject_code']}" : s["subject_id"] for s in subjects}


    selected_subject = st.selectbox("Select Subject", options=list(subject_options.keys()))

    st.markdown("<br>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        st.markdown('<div class="add-photo-container">', unsafe_allow_html=True)
        if st.button("Add photos to analyze", key="add_photos_btn", icon=":material/add_photo_alternate:", use_container_width=True):
            add_photo_dialog()
        st.markdown('</div>', unsafe_allow_html=True)

    selected_subject_id = subject_options[selected_subject]
    st.divider()

    images = st.session_state.attendance_images
    if images :
        st.write("#### Added Images")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(images):
            with gallery_cols[idx %4] :
                st.image(img, width="stretch", caption=f"Photo {idx+1}")

    c1, c2 = st.columns(2)
    with c1 :
        if st.button("Run face analyzer", width="stretch", disabled=len(images) == 0) :
            with st.spinner("Deep scannning classroom images...") :
                all_detected_id = {}
                for idx, img in enumerate(images) :
                    img_np = np.array(img.convert("RGB"))
                    detected, _, _ = predict_attendance(img_np)

                    if detected :
                        for sid in detected.keys() :
                            student_id = int(sid)

                            all_detected_id.setdefault(student_id, []).append(f"Photo {idx+1}")

                try:
                    enrolled_res = supabase.table("subject_students").select("*, students(*)").eq("subject_id", selected_subject_id).execute()
                    enrolled_students = enrolled_res.data if enrolled_res else []
                except Exception as e:
                    st.error(f"Error fetching enrolled students: {e}")
                    enrolled_students = []

                if not enrolled_students:
                    st.warning("No students enrolled in this course")
                else :
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students :
                        student = node["students"]
                        sources = all_detected_id.get(int(student["student_id"]), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name" : student["name"],
                            "ID" : student["student_id"],
                            "Source" : ", ".join(sources) if is_present else "-",
                            "Status" : "✅Present" if is_present else "❌Absent"
                        })

                        attendance_to_log.append({
                            "student_id" : student["student_id"],

                            "subject_id" : selected_subject_id,
                            "timestamp" : current_timestamp,
                            "is_present" : bool(is_present)
                        })
                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
    with c2 :
        if st.button("Clear all images", width="stretch", icon=":material/delete:", type="primary", disabled = len(images) == 0) :
            st.session_state.attendance_images = []
            st.rerun()
