import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import joblib
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# --------------------- DB SETUP --------------------- #
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, email TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS predictions (username TEXT, inputs TEXT, svm_result TEXT, rf_result TEXT)''')
conn.commit()

# --------------------- LOAD DATA --------------------- #
data = pd.read_csv("graduation_dataset.csv")
target_column = "Target"  # <-- Replace with your real target column name

if target_column not in data.columns:
    st.error(f"Target column '{target_column}' not found! Please check your CSV.")
    st.stop()

features = data.drop(target_column, axis=1)
target = data[target_column]

input_fields = features.columns.tolist()

# --------------------- MANUAL CATEGORICAL MAPPINGS --------------------- #
categorical_mappings = {
    "Marital status": { "Single": 1, "Married": 2, "Widowed": 3, "Divorced": 4 },
    "Application mode": { "Online": 1, "In-person": 2, "Referral": 3 },
    "Daytime/evening attendance": { "Daytime": 1, "Evening": 2 },
    "Previous qualification": { "None": 0, "High School": 1, "Bachelor": 2, "Master": 3 },
    "Nacionality": { "Local": 1, "International": 2 },
    "Mother's qualification": { "None": 0, "Primary": 1, "Secondary": 2, "Higher": 3 },
    "Father's qualification": { "None": 0, "Primary": 1, "Secondary": 2, "Higher": 3 },
    "Mother's occupation": { "Unemployed": 0, "Employed": 1 },
    "Father's occupation": { "Unemployed": 0, "Employed": 1 },
    "Displaced": { "No": 0, "Yes": 1 },
    "Educational special needs": { "No": 0, "Yes": 1 },
    "Debtor": { "No": 0, "Yes": 1 },
    "Tuition fees up to date": { "No": 0, "Yes": 1 },
    "Gender": { "Male": 0, "Female": 1 },
    "Scholarship holder": { "No": 0, "Yes": 1 },
    "International": { "No": 0, "Yes": 1 }
}

categorical_fields = list(categorical_mappings.keys())
numeric_fields = [f for f in input_fields if f not in categorical_fields]

# --------------------- MANUAL ENCODING --------------------- #
for col, mapping in categorical_mappings.items():
    if col in features.columns:
        features[col] = features[col].map(mapping)

# Encode target if needed
target = target.map({"No": 0, "Yes": 1})  # adjust if your target is Yes/No or Complete/Not

# --------------------- TRAIN & SAVE MODELS --------------------- #
if not os.path.exists("svm_model.pkl") or not os.path.exists("rf_model.pkl"):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    svm = SVC(probability=True)
    rf = RandomForestClassifier()
    svm.fit(X_train, y_train)
    rf.fit(X_train, y_train)
    joblib.dump(svm, "svm_model.pkl")
    joblib.dump(rf, "rf_model.pkl")
else:
    svm = joblib.load("svm_model.pkl")
    rf = joblib.load("rf_model.pkl")

# --------------------- SESSION STATE --------------------- #
if "user" not in st.session_state:
    st.session_state.user = None

# --------------------- AUTH --------------------- #
def register_user(username, email, password):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        return False
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    return True

def login_user(username, password):
    if username == "admin" and password == "admin123":
        return "admin"
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if c.fetchone():
        return "student"
    return None

# --------------------- MENUS --------------------- #
def student_menu():
    return st.sidebar.selectbox("Menu", ["Home", "Predict", "View Predictions", "Change Password", "Logout"])

def admin_menu():
    return st.sidebar.selectbox("Menu", ["Home", "View Predictions", "Graphical Analysis", "Logout"])

# --------------------- MAIN APP --------------------- #
def main():
    # --------------------- CUSTOM STYLE --------------------- #
    st.markdown("""
        <style>
        body {
            background-color: red;
            font-family: 'Times New Roman', Times, serif;
        }
        .stApp {
            background-color: RGB (128, 128, 128);
            font-family: 'Times New Roman', Times, serif;
        }
        section[data-testid="stSidebar"] {
            background-color: RGB (255, 255, 255);

        </style>
    """, unsafe_allow_html=True)

    st.title("🎓 Graduation Completion Prediction App")

    if st.session_state.user is None:
        auth_choice = st.sidebar.radio("Select", ["Login", "Register"])

        if auth_choice == "Register":
            st.subheader("Student Registration")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Register"):
                if register_user(username, email, password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists!")

        else:
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                role = login_user(username, password)
                if role:
                    st.session_state.user = username if role == "student" else "admin"
                    st.session_state.role = role
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    elif st.session_state.role == "student":
        choice = student_menu()

        if choice == "Home":
            st.subheader("👤 Student Profile")
            c.execute("SELECT * FROM users WHERE username=?", (st.session_state.user,))
            user_data = c.fetchone()
            st.write(f"**Username:** {user_data[0]}")
            st.write(f"**Email:** {user_data[1]}")

        elif choice == "Predict":
            st.subheader("🎯 Graduation Completion Prediction")
            user_inputs = {}

            with st.form("predict_form"):
                for field in input_fields:
                    if field in categorical_fields:
                        options = list(categorical_mappings[field].keys())
                        selected_label = st.selectbox(field, options)
                        user_inputs[field] = categorical_mappings[field][selected_label]
                    else:
                        user_inputs[field] = st.number_input(field, step=1.0)
                submit = st.form_submit_button("Predict")

            if submit:
                input_df = pd.DataFrame([user_inputs])
                svm_pred = svm.predict(input_df)[0]
                rf_pred = rf.predict(input_df)[0]

                svm_result = "Yes" if svm_pred == 1 else "No"
                rf_result = "Yes" if rf_pred == 1 else "No"

                st.success(f"✅ SVM Prediction: {svm_result}")
                st.success(f"✅ Random Forest Prediction: {rf_result}")

                c.execute("INSERT INTO predictions VALUES (?, ?, ?, ?)",
                          (st.session_state.user, str(user_inputs), svm_result, rf_result))
                conn.commit()

                result_df = input_df.copy()
                result_df["SVM_Result"] = svm_result
                result_df["RF_Result"] = rf_result
                csv = result_df.to_csv(index=False).encode()
                st.download_button("📥 Download Prediction", csv, "prediction.csv", "text/csv")

        elif choice == "View Predictions":
            st.subheader("📊 Your Predictions")
            df = pd.read_sql_query("SELECT * FROM predictions WHERE username=?", conn, params=(st.session_state.user,))
            st.dataframe(df)

        elif choice == "Change Password":
            st.subheader("🔑 Change Password")
            old_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            if st.button("Change"):
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (st.session_state.user, old_pass))
                if c.fetchone():
                    c.execute("UPDATE users SET password=? WHERE username=?", (new_pass, st.session_state.user))
                    conn.commit()
                    st.success("Password changed!")
                else:
                    st.error("Current password incorrect.")

        elif choice == "Logout":
            st.session_state.user = None
            st.rerun()

    elif st.session_state.role == "admin":
        choice = admin_menu()

        if choice == "Home":
            st.subheader("📋 All Registered Users")
            df = pd.read_sql_query("SELECT username, email FROM users", conn)
            st.dataframe(df)

        elif choice == "View Predictions":
            st.subheader("📊 All Predictions")
            df = pd.read_sql_query("SELECT * FROM predictions", conn)
            st.dataframe(df)

        elif choice == "Graphical Analysis":
            st.subheader("📈 Graphical Analysis")
            df = pd.read_sql_query("SELECT * FROM predictions", conn)
            if df.empty:
                st.warning("No predictions yet.")
            else:
                svm_counts = df['svm_result'].value_counts()
                rf_counts = df['rf_result'].value_counts()

                fig, ax = plt.subplots(1, 2, figsize=(12, 5))
                ax[0].bar(svm_counts.index, svm_counts.values)
                ax[0].set_title("SVM: Complete vs Not")
                ax[1].bar(rf_counts.index, rf_counts.values)
                ax[1].set_title("RF: Complete vs Not")
                st.pyplot(fig)

                st.subheader("🔍 Feature Distributions")
                fig2 = sns.pairplot(data)
                st.pyplot(fig2)

        elif choice == "Logout":
            st.session_state.user = None
            st.rerun()

# --------------------- RUN APP --------------------- #
if __name__ == '__main__':
    main()
