import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write(
        "Enter the subject code provided by your teacher to enroll"
    )

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101"
    )

    if st.button(
        "Enroll now",
        type="primary",
        width="stretch"
    ):

        if join_code:

            # Find the subject using the subject code.
            # The subjects table uses "id", not "subject_id".
            res = (
                supabase
                .table("subjects")
                .select("id, name, subject_code, section")
                .eq("subject_code", join_code)
                .execute()
            )

            if res.data:

                subject = res.data[0]

                student_id = st.session_state.student_data[
                    "student_id"
                ]

                subject_id = subject["id"]

                # Check whether the student is already enrolled.
                check = (
                    supabase
                    .table("subject_students")
                    .select("*")
                    .eq("subject_id", subject_id)
                    .eq("student_id", student_id)
                    .execute()
                )

                if check.data:

                    st.warning(
                        "You are already enrolled in this subject"
                    )

                else:

                    # Enroll the student using subjects.id
                    enroll_student_to_subject(
                        student_id,
                        subject_id
                    )

                    st.success(
                        "Successfully enrolled!"
                    )

                    time.sleep(1)

                    st.rerun()

            else:

                st.error(
                    "Subject code not found"
                )

        else:

            st.warning(
                "Please enter a subject code"
            )
