# LIGHTNING'S CHECK – AI-Powered Attendance System

## Overview

LIGHTNING'S CHECK is an intelligent, AI-driven attendance management system that uses facial recognition and voice authentication to streamline the process of taking attendance in classrooms. It replaces manual roll calls with a fast, secure, and accurate automated system, featuring dedicated dashboards for both teachers and students.

## Key Features

* **Teacher Dashboard**: Create subjects, manage enrollments, and take attendance using AI face or voice analysis.
* **Student Dashboard**: Enroll in subjects, track attendance history, and log in securely via FaceID.
* **AI-Based Attendance**:
  * **Face Recognition**: Detect and identify students in a classroom photo automatically.
  * **Voice Authentication**: Identify students by processing voice samples.
* **Join Codes & QR**: Teachers can generate join codes and QR codes to let students self-enroll in classes.
* **Authentication**: Password-based login for teachers and FaceID-based login for students.
* **Database Integration**: Powered by Supabase for fast, reliable, and secure data storage.

## Technology Stack

* **Frontend**: Streamlit
* **Database**: Supabase
* **Face Recognition**: dlib, scikit-learn (SVM classifier), face_recognition_models
* **Voice Recognition**: Librosa, Resemblyzer
* **Utilities**: NumPy, Pandas, Pillow, bcrypt (password hashing), Segno (QR codes)

## System Architecture

```text
User (Teacher / Student)
        ↓
   Streamlit UI
        ↓
  Authentication (Password / FaceID)
        ↓
Teacher / Student Dashboard
        ↓
AI Attendance Processing (Dlib / SVM / Resemblyzer)
        ↓
     Supabase (Database)
```

## Project Structure

```text
ai-attendance-project-app/
│
├── app.py                     # Main Streamlit application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore rules
├── .env.example               # Example configuration file
│
├── src/
│   ├── components/            # Reusable UI components (dialogs, cards, headers)
│   ├── database/              # Database configuration and queries (Supabase)
│   ├── pipelines/             # AI pipelines (face and voice recognition)
│   ├── screens/               # Main application screens (home, teacher, student)
│   └── ui/                    # Base layout and styling definitions
```

## Installation

### Prerequisites

* Python 3.10 or higher.
* **Windows Users**: You MUST install Visual Studio C++ Build Tools before installing the dependencies, as `dlib` requires a C++ compiler to build from source. Download it from the [Visual Studio website](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and select "Desktop development with C++" during installation.

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-attendance-project-app-main
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   * **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   * **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Configuration

This project requires a Supabase database. You must provide your Supabase connection details via Streamlit secrets.

1. Create a directory named `.streamlit` in the root of your project:
   ```bash
   mkdir .streamlit
   ```

2. Create a file named `secrets.toml` inside `.streamlit` and add your configuration based on the provided `.env.example`:
   ```toml
   # .streamlit/secrets.toml
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_key"
   ```

**Important:** Never commit `.streamlit/secrets.toml` to version control. It is already added to `.gitignore`.

## Deployment

### GitHub Setup

1. **Initialize a git repository (if not already initialized):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   ```
2. **Create a new repository on GitHub** and push the code:
   ```bash
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```
*Ensure that `.env` and `.streamlit/secrets.toml` are NOT committed.*

### Streamlit Community Cloud Deployment

1. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New app"**.
3. Select the repository you just pushed, set the branch to `main`, and the main file path to `app.py`.
4. Click on **"Advanced settings"**.
5. Select **Python 3.10** as the Python version (recommended for the required dependencies).
6. In the **Secrets** field, paste your Supabase credentials in TOML format:
   ```toml
   SUPABASE_URL = "your_actual_supabase_url"
   SUPABASE_KEY = "your_actual_supabase_key"
   ```
7. Click **"Save"** and then **"Deploy!"**.
Note: Streamlit Community Cloud runs on Linux. The included `packages.txt` ensures that system-level dependencies for `dlib` and `librosa` are installed automatically during the deployment process.

## Running the Application

To start the application, run:

```bash
streamlit run app.py
```

## How It Works

### Teacher Workflow

1. **Login/Register**: Teachers create an account with a username and password.
2. **Dashboard**: Teachers can view their managed subjects.
3. **Manage Subjects**: Teachers can create new subjects and generate shareable join codes/QR codes for students.
4. **Take Attendance**: 
   * Select a subject.
   * Upload photos of the classroom.
   * Click "Run Face Analysis" to detect students and log attendance.
   * Alternatively, use "Use Voice Attendance" for audio-based verification.
5. **View Records**: Check attendance history and aggregated statistics.

### Student Workflow

1. **Login/Register**: Students log in using a live camera feed. First-time users register their face and optionally a voice sample.
2. **Dashboard**: View enrolled subjects and personal attendance stats.
3. **Join Class**: Use a join code (or scan a QR code) provided by the teacher to enroll in a new subject.
4. **Track Status**: Monitor total classes and attended classes for each subject.

## AI Methodology

* **Face Recognition**: 
  * Uses `dlib`'s HOG-based face detector and 128-dimensional face embeddings.
  * A Support Vector Machine (SVM) classifier with a linear kernel from `scikit-learn` is trained on-the-fly with the registered students' face embeddings to predict attendance.
  * A confidence threshold (Euclidean distance) is used to ensure robust matches.
* **Voice Recognition**:
  * Uses `Resemblyzer` and `Librosa` to extract speaker embeddings from audio samples.
  * Dot product similarity is used to match voice segments against enrolled student voice profiles.

## Database

The application uses Supabase (PostgreSQL) with the following core entities:
* `teachers`: Stores teacher credentials (passwords are hashed with bcrypt).
* `students`: Stores student profiles, including face and voice embeddings.
* `subjects`: Stores subject/course information.
* `subject_students`: Junction table linking students to subjects (enrollments).
* `attendance_logs`: Records timestamped attendance for students in specific subjects.

## Security

* **No Hardcoded Secrets**: All sensitive keys are managed via Streamlit secrets (`secrets.toml`).
* **Password Hashing**: Teacher passwords are securely hashed using `bcrypt` before storage.
* **Protected Routes**: UI components and database actions are restricted based on session state roles (`teacher` vs. `student`).

## Limitations

* **Face Recognition Scalability**: Training the SVM classifier on-the-fly works well for small to medium classrooms but may need optimization for massive datasets.
* **Liveness Detection**: The current implementation does not include anti-spoofing (liveness detection), meaning it could potentially be tricked by a photo of a student.

## Future Improvements

* Implement liveness detection to prevent photo-spoofing.
* Add comprehensive analytics and export functionalities (e.g., CSV/Excel).
* Enhance mobile responsiveness for the teacher and student dashboards.
* Support cloud storage for uploaded class photos and audio segments.

## License

This project is licensed under the MIT License.