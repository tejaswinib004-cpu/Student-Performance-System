import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ---------- DATABASE CONNECTION ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # change if different
        database="student_db"
    )

# ---------- ADD STUDENT ----------
def add_student(name, age, subject, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, subject, marks) VALUES (%s, %s, %s, %s)",
        (name, age, subject, marks)
    )
    conn.commit()
    conn.close()

# ---------- FETCH DATA ----------
def fetch_students():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

# ---------- UPDATE MARKS ----------
def update_marks(id, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET marks=%s WHERE id=%s", (marks, id))
    conn.commit()
    conn.close()

# ---------- DELETE STUDENT ----------
def delete_student(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()

# ---------- STREAMLIT UI ----------
st.title("🎓 Student Performance Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "View Students", "Update Marks", "Delete Student", "Analysis"]
)

# ---------- ADD ----------
if menu == "Add Student":
    st.subheader("Add Student")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0, max_value=100)

    if st.button("Add"):
        add_student(name, age, subject, marks)
        st.success("Student added successfully")

# ---------- VIEW ----------
elif menu == "View Students":
    st.subheader("All Students")
    df = fetch_students()
    df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    st.dataframe(df)

# ---------- UPDATE ----------
elif menu == "Update Marks":
    st.subheader("Update Marks")
    id = st.number_input("Student ID", min_value=1)
    marks = st.number_input("New Marks", min_value=0, max_value=100)
    if st.button("Update"):
        update_marks(id, marks)
        st.success("Marks updated")

# ---------- DELETE ----------
elif menu == "Delete Student":
    st.subheader("Delete Student")
    id = st.number_input("Student ID", min_value=1)
    if st.button("Delete"):
        delete_student(id)
        st.success("Student deleted")

# ---------- ANALYSIS ----------
elif menu == "Analysis":
    st.subheader("Performance Analysis")
    df = fetch_students()

    if not df.empty:
        avg_marks = df["marks"].mean()
        pass_percent = (df["marks"] >= 40).mean() * 100
        top_scorer = df.loc[df["marks"].idxmax()]

        st.write("📊 Average Marks:", round(avg_marks, 2))
        st.write("✅ Pass Percentage:", round(pass_percent, 2), "%")
        st.write("🏆 Top Scorer:", top_scorer["name"], "-", top_scorer["marks"])

        # Subject wise average
        subject_avg = df.groupby("subject")["marks"].mean()

        st.subheader("Subject vs Average Marks")
        fig, ax = plt.subplots()
        subject_avg.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        # Pass / Fail Pie
        status_count = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail").value_counts()

        fig2, ax2 = plt.subplots()
        ax2.pie(status_count, labels=status_count.index, autopct="%1.1f%%")
        st.pyplot(fig2)