from src.database.config import supabase
import bcrypt


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_pass(pwd):
    return bcrypt.hashpw(
        pwd.encode(),
        bcrypt.gensalt()
    ).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(
        pwd.encode(),
        hashed.encode()
    )


# ============================================================
# TEACHER FUNCTIONS
# ============================================================

def check_teacher_exists(username):
    # Returns True if username already exists
    response = (
        supabase
        .table("teachers")
        .select("username")
        .eq("username", username)
        .execute()
    )

    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    response = (
        supabase
        .table("teachers")
        .insert(data)
        .execute()
    )

    teachers = response.data

    # Make teacher_id available to the application
    for teacher in teachers:
        if "id" in teacher and "teacher_id" not in teacher:
            teacher["teacher_id"] = teacher["id"]

    return teachers


def teacher_login(username, password):
    response = (
        supabase
        .table("teachers")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if response.data:
        teacher = response.data[0]

        if check_pass(password, teacher["password"]):

            # Supabase uses "id"
            # Application expects "teacher_id"
            if "id" in teacher and "teacher_id" not in teacher:
                teacher["teacher_id"] = teacher["id"]

            return teacher

    return None


# ============================================================
# STUDENT FUNCTIONS
# ============================================================

def get_all_students():
    response = (
        supabase
        .table("students")
        .select("*")
        .execute()
    )

    students = response.data

    # Supabase uses "id"
    # Application expects "student_id"
    for student in students:
        if "id" in student and "student_id" not in student:
            student["student_id"] = student["id"]

    return students


def create_student(
    new_name,
    face_embedding=None,
    voice_embedding=None
):
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }

    response = (
        supabase
        .table("students")
        .insert(data)
        .execute()
    )

    students = response.data

    # Make student_id available to the application
    for student in students:
        if "id" in student and "student_id" not in student:
            student["student_id"] = student["id"]

    return students


# ============================================================
# SUBJECT FUNCTIONS
# ============================================================

def create_subject(
    subject_code,
    name,
    section,
    teacher_id
):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }

    response = (
        supabase
        .table("subjects")
        .insert(data)
        .execute()
    )

    subjects = response.data

    # Make subject_id available to the application
    for subject in subjects:
        if "id" in subject and "subject_id" not in subject:
            subject["subject_id"] = subject["id"]

    return subjects


def get_teacher_subjects(teacher_id):
    response = (
        supabase
        .table("subjects")
        .select(
            "*, subject_students(count), attendance_logs(timestamp)"
        )
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for subject in subjects:

        # ====================================================
        # IMPORTANT:
        # Supabase uses "id"
        # Application expects "subject_id"
        # ====================================================
        if "id" in subject and "subject_id" not in subject:
            subject["subject_id"] = subject["id"]

        # ====================================================
        # Count enrolled students
        # ====================================================
        subject["total_students"] = (
            subject
            .get("subject_students", [{}])[0]
            .get("count", 0)
            if subject.get("subject_students")
            else 0
        )

        # ====================================================
        # Count unique attendance sessions
        # ====================================================
        attendance = subject.get("attendance_logs", [])

        unique_sessions = len(
            set(
                log["timestamp"]
                for log in attendance
                if log.get("timestamp")
            )
        )

        subject["total_classes"] = unique_sessions

        # Remove nested data after calculating statistics
        subject.pop("subject_students", None)
        subject.pop("attendance_logs", None)

    return subjects


# ============================================================
# SUBJECT ENROLLMENT FUNCTIONS
# ============================================================

def enroll_student_to_subject(
    student_id,
    subject_id
):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }

    response = (
        supabase
        .table("subject_students")
        .insert(data)
        .execute()
    )

    return response.data


def unenroll_student_to_subject(
    student_id,
    subject_id
):
    response = (
        supabase
        .table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data


def get_student_subjects(student_id):
    response = (
        supabase
        .table("subject_students")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )

    subjects = response.data

    # Make subject_id available inside nested subjects
    for item in subjects:
        if item.get("subjects"):
            subject = item["subjects"]

            if "id" in subject and "subject_id" not in subject:
                subject["subject_id"] = subject["id"]

    return subjects


# ============================================================
# ATTENDANCE FUNCTIONS
# ============================================================

def get_student_attendance(student_id):
    response = (
        supabase
        .table("attendance_logs")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )

    attendance = response.data

    # Make subject_id available inside nested subjects
    for log in attendance:
        if log.get("subjects"):
            subject = log["subjects"]

            if "id" in subject and "subject_id" not in subject:
                subject["subject_id"] = subject["id"]

    return attendance


def create_attendance(logs):
    response = (
        supabase
        .table("attendance_logs")
        .insert(logs)
        .execute()
    )

    return response.data


def get_attendance_for_teacher(teacher_id):
    response = (
        supabase
        .table("attendance_logs")
        .select("*, subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )

    attendance = response.data

    # Make subject_id available inside nested subjects
    for log in attendance:
        if log.get("subjects"):
            subject = log["subjects"]

            if "id" in subject and "subject_id" not in subject:
                subject["subject_id"] = subject["id"]

    return attendance
