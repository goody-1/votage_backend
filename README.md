# Votage Church Admin API

A robust suite of RESTful APIs for a church admin dashboard, built using a **FastAPI** and **Django** hybrid architecture. This project enables comprehensive management of church operations, including members, pastors, attendance, events, and more.

## 🚀 Features

- **Member Management**: Track members, their contact details, and first-timers.
- **Pastor Directory**: Maintain a database of pastors and leadership.
- **Service & Attendance Tracking**: Log church services and monitor attendance trends.
- **Event Management**: Organize and schedule church events.
- **Growth Track & Connect Groups**: Manage spiritual growth programs and small group connections.
- **Departmental Organization**: Keep track of various church departments and their members.
- **Dashboard Statistics**: Get real-time summaries and analytics of church data.
- **JWT Authentication**: Secure endpoints with JSON Web Token based authentication.

## 🛠️ Tech Stack

- **Backend**: FastAPI (for high-performance API endpoints)
- **Framework**: Django (for ORM, Admin interface, and core logic)
- **Database**: PostgreSQL (Neon.tech recommended for production)
- **Authentication**: JWT (PyJWT)
- **Environment Management**: Python Dotenv

## 📂 Project Structure

```text
church/
├── api/                # FastAPI application
│   ├── main.py         # FastAPI entry point
│   └── routers/        # API route definitions
├── apps/               # Django applications (domain logic)
│   ├── members/
│   ├── pastors/
│   ├── services/
│   └── ...
├── church/             # Django project settings
│   ├── settings.py
│   └── urls.py
├── manage.py           # Django management script
├── requirements.txt    # Project dependencies
└── .env                # Environment variables
```

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd church
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@host:port/dbname?sslmode=require
   ```

5. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the application**:
   ```bash
   # Start with Uvicorn (FastAPI)
   uvicorn api.main:app --reload
   ```

## 📖 API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🛡️ License

This project is licensed under the MIT License.
