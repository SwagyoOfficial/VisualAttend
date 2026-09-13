from src.database.config import supabase
import streamlit as st
import bcrypt
import time

def safe_execute(query_builder, max_retries=2, delay=0.5):
    """
    Safely executes a Supabase query builder with retries and exception handling.
    """
    for attempt in range(max_retries):
        try:
            return query_builder.execute()
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"Database connection error: {e}")
                return None
            time.sleep(delay)
    return None

def check_pass(pwd, hash_pwd):
    return bcrypt.checkpw(pwd.encode(), hash_pwd.encode())

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def login_teacher(username, password):
    if not username or not password:
        return False, 'Some fields are not filled!'
    try:
        teacher = teacher_login(username, password)
        if teacher:
            st.session_state.teacher_data = {
                "id": teacher['teacher_id'],
                "username": teacher['username'],
                "name": teacher['name'],
            }
            st.session_state.user_role = 'teacher'
            st.session_state.is_logged_in = True
            return True, "Welcome back!"
        return False, "Incorrect username or password!"
    except Exception as e:
        return False, str(e)

def register_teacher(teacher_name, teacher_username, teacher_password):
    if not teacher_username or not teacher_password or not teacher_name:
        return False, 'Some fields are not filled!'

    if check_teacher_exists(teacher_username):
        return False, 'Username already taken!'
    try:
        result = create_teacher(teacher_name, teacher_username, teacher_password)
        if result:
            return True, 'Successfully created!'
        return False, 'Database connection error during registration.'
    except Exception as e:
        return False, str(e)

def check_teacher_exists(username):
    try:
        query = supabase.table("teachers").select("username").eq("username", username)
        response = safe_execute(query)
        return len(response.data) > 0 if response and response.data else False
    except Exception:
        return False

def create_teacher(name, username, password):
    data = {
        "username": username,
        "password": hash_password(password),
        "name": name
    }
    query = supabase.table("teachers").insert(data)
    response = safe_execute(query)
    return response.data if response else None

def teacher_login(username, password):
    try:
        query = supabase.table("teachers").select("*").eq("username", username)
        response = safe_execute(query)
        if response and response.data:
            teacher = response.data[0]
            if check_pass(password, teacher['password']):
                return teacher
        return None
    except Exception:
        return None

def get_all_students():
    try:
        query = supabase.table("students").select("*")
        response = safe_execute(query)
        if response and response.data is not None:
            return response.data
        return []
    except Exception:
        return []

def create_student(name, face_embedding=None):
    data = {'name': name, 'face_embedding': face_embedding}
    query = supabase.table('students').insert(data)
    response = safe_execute(query)
    return response.data if response else None

def create_subject(id, name, section, teacher_id):
    try:
        data = {
            'subject_code': id,
            'name': name,
            "section": section,
            'teacher_id': teacher_id
        }
        query = supabase.table('subjects').insert(data)
        response = safe_execute(query)
        return response.data if response else None
    except Exception as e:
        st.warning(f"Error creating subject: {e}")
        return None

def get_teacher_subjects(teacher_id):
    try:
        query = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id)
        response = safe_execute(query)
        if not response or not response.data:
            return []
        subjects = response.data
        for sub in subjects:
            sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
            attendance = sub.get('attendance_logs', [])
            unique_sessions = len(set(log['timestamp'] for log in attendance)) if attendance else 0
            sub['total_classes'] = unique_sessions

            sub.pop('subject_students', None)
            sub.pop('attendance_logs', None)

        return subjects
    except Exception as e:
        st.error(f"Error fetching teacher subjects: {e}")
        return []

def enroll_to_subject(std_id, sub_id):
    data = {"student_id": std_id, "subject_id": sub_id}
    query = supabase.table("subject_students").insert(data)
    response = safe_execute(query)
    return response

def unenroll_to_subject(std_id, sub_id):
    query = supabase.table("subject_students").delete().eq("student_id", std_id).eq("subject_id", sub_id)
    response = safe_execute(query)
    return response.data if response else None

def get_student_subjects(std_id):
    query = supabase.table("subject_students").select("*, subjects(*)").eq('student_id', std_id)
    response = safe_execute(query)
    return response.data if response else []

def get_student_attendance(student_id):
    query = supabase.table("attendance_logs").select("*, subjects(*)").eq('student_id', student_id)
    response = safe_execute(query)
    return response.data if response else []

def create_attendance(logs):
    query = supabase.table("attendance_logs").insert(logs)
    response = safe_execute(query)
    return response.data if response else None

def get_attendance_for_teacher(teacher_id):
    query = supabase.table("attendance_logs").select("*, subjects!inner(*)").eq("subjects.teacher_id", teacher_id)
    response = safe_execute(query)
    return response.data if response else []