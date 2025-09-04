## 🚀 Task Manager

---

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Xequrt/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Xequrt/python-project-52/actions)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=Xequrt_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Xequrt_python-project-52)

**Task Manager** is a professional web application designed for efficient task management. Built on Django, it includes:

* **Secure Account System** — protected user authentication and management
* **Task Status Tracking** — comprehensive monitoring of task progress
* **Label System** — organized categorization and tagging functionality
* **Modern Architecture** — robust and scalable backend infrastructure

The application is ready for integration into work processes and daily operations.

### Production Build

[![Running Application](https://shields.fly.dev/badge/Running%20Application-Online-blueviolet)](https://task-manager-hik7.onrender.com/)

### Requirements

**System Requirements:**
* **Python 3.11+** — main programming language
* **PostgreSQL 15+** — database management system
* **uv package manager** — modern package manager
* **Git** — for repository cloning

**Python Dependencies:**
* **Django 5.2+** — web framework
* **psycopg2-binary** — PostgreSQL adapter
* **python-dotenv** — environment variables handling
* **gunicorn** — WSGI server
* **whitenoise** — static files handling

---

### Installation & Launch

1. **Clone the repository:**
```bash
git clone https://github.com/Xequrt/python-project-52.git
cd python-project-52
```

2. **Install dependencies:**
```bash
uv install
```

3. **Create `.env` file in the root directory:**
```bash
SECRET_KEY=your_secret_key
DEBUG=True # Set to False for production
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```
Replace `username`, `password`, `dbname`, and `your_secret_key` with your own values.

4. **Prepare and launch the application:**
```bash
uv run makemigrations
uv run migrate
uv run start
```

The application will be available at: http://localhost:8000

---

### 📋 Additional Setup

**Database setup:**
* Create a PostgreSQL database
* Update `DATABASE_URL` in the `.env` file

**Static files:**
* Collect static files using `uv run collectstatic`

**Environment variables:**
* Make sure all required variables are set in `.env`

---

### 🙏 Appreciation

Thank you for choosing my project! Your support means a lot to me. Whether you're a developer, a team member, or just exploring new tools, I'm glad you're here.

If this project helps you in your work, please:
* Give it a ⭐ on GitHub
* Share your experience with others

Happy coding!