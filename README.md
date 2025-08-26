🎓 Graduation Prediction System

This project predicts student graduation outcomes using Machine Learning models integrated into a web-based application. It allows users to input student-related data and get predictions about graduation success.

🚀 Live Demo

(https://malihafatima1-graduationprediction-app-anscty.streamlit.app/)


✨ Features

Student graduation prediction using trained Random Forest and SVM models.

User authentication with database integration.

Web interface with custom styling.

Pre-trained models and encoders for quick deployment.


🛠️ Tech Stack

Backend: Python (Flask/Django)

Machine Learning: Scikit-learn

Database: SQLite

Frontend: HTML, CSS

Deployment: Vercel

Version Control: Git & GitHub

📂 Project Structure
GRADUATIONPREDICTION/
│── app.py               # Main application
│── auth.py              # User authentication
│── config.py            # Configuration settings
│── database.py          # Database connections
│── model.py             # ML model functions
│── graduation_dataset.csv # Training dataset
│── rf_model.pkl         # Random Forest model
│── svm_model.pkl        # SVM model
│── encoders.pkl         # Data encoders
│── target_encoder.pkl   # Target encoder
│── users.db             # SQLite database
│── assets/style.css     # Styling

⚙️ Local Setup

    Clone the repository:

git clone https://github.com/Malihafatima1/GraduationPrediction.git
cd GraduationPrediction

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r requirements.txt

Run the application locally:

python app.py

Open in browser:

    http://127.0.0.1:5000/

📊 Dataset

The dataset (graduation_dataset.csv) contains student attributes used to train the machine learning models.
🤖 Models

    Random Forest Classifier

    Support Vector Machine (SVM)

    Encoders for preprocessing

✨ Future Enhancements

    Add more ML models for comparison.

    Deploy on cloud platforms like AWS or Heroku for scalability.

    Implement interactive data visualizations.

👩‍💻 Author

Maliha Fatima
📌 MCA Graduate | Web & ML Enthusiast

