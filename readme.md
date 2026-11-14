# Django Online Course & Assessment Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Web_Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

A full-stack web application built with Django that allows users to browse courses, view lessons, and complete final assessments to earn their grades. This project was developed as the Final Capstone for the **IBM Django Application Development with SQL and Databases** course on Coursera.

## ✨ Key Features

* **Authentication & Security:** Secure user registration, login, and logout. The assessment module is protected by `@login_required` decorators to prevent unauthorized access.
* **Course Management:** Browse available courses, view detailed course descriptions, and explore nested lesson modules via an intuitive accordion UI.
* **Interactive Final Assessment:**
  * Dynamic multiple-choice exam generated from the SQLite database.
  * Modern, interactive UI for selecting answers (styled as clickable cards).
  * Automated grading system that calculates the final percentage.
  * Pass/Fail evaluation (requires a 70% or higher to pass).
* **Detailed Results Dashboard:** Provides immediate feedback upon exam submission, including a percentage progress bar and a question-by-question breakdown of correct and incorrect answers.
* **Stunning UI/UX:** Fully responsive design built with **Bootstrap 5**. Includes custom CSS glassmorphism effects, hover animations, and a seamless **Dark/Light Mode** toggle that persists via LocalStorage.
* **Admin Dashboard:** Fully configured Django Admin interface with inline model management (`TabularInline` and `StackedInline`) for easy creation of Questions and Choices directly from the Course page.

## 🛠️ Technology Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons
* **Database:** SQLite (Default Django DB)
* **Version Control:** Git & GitHub

## 🚀 Local Installation & Setup

Follow these steps to run the project locally on your machine.

**1. Clone the repository**
```bash
git clone https://github.com/sayantan-pachal/Django-Application-Development-with-SQL-and-Databases.git
cd Django-Application-Development-with-SQL-and-Databases
```

**2. Create and activate a virtual environment (Recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install django
```

**4. Run Database Migrations**
```bash
python manage.py makemigrations onlinecourse
python manage.py migrate
```

**5. Create a Superuser (Admin Account)**
```bash
python manage.py createsuperuser
```

**6. Run the Development Server**
```bash
python manage.py runserver
```

**7. Access the Application**
* Main Application: `http://127.0.0.1:8000/onlinecourse/`
* Admin Panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure highlights

```text
├── onlinecourse/
│   ├── models.py         # Defines Course, Lesson, Question, Choice, and Submission
│   ├── views.py          # Core logic including submit() and show_exam_result()
│   ├── urls.py           # Application routing
│   ├── admin.py          # Admin panel configuration with inline models
│   └── templates/        # Bootstrap 5 HTML templates (Dark/Light mode enabled)
└── manage.py
```

## 👨‍💻 Author

**Sayantan Pachal**
* GitHub: [@sayantan-pachal](https://github.com/sayantan-pachal)
* Built for the IBM Coursera Django Specialization.