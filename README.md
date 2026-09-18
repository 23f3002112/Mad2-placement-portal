# Mad2-placement-portal

Placement Portal Application (PPA) V2.
A comprehensive platform for Institutes, Companies, and Students to manage campus recruitment efficiently. Built with Flask and VueJS.

## Initial Setup / Installation

If you are opening this project for the first time or on a new computer, you must install the dependencies first. `node_modules` and Python environments are excluded from the repository to save space.

### 1. Install Backend Dependencies (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies (Terminal 2)
```bash
cd frontend
npm install
```

## How to Run

Assuming all dependencies are already installed, open **two separate terminals** and run the following commands:

### 1. Start MailHog (Terminal 1)
MailHog is used to catch and view outgoing emails locally. Run the MailHog executable from your Downloads folder:
```bash
/c/Users/HP/Downloads/MailHog_windows_amd64.exe
```

### 2. Start the Backend Server (Terminal 2)
```bash
cd backend
python app.py
```

### 3. Start the Frontend Dev Server (Terminal 3)
```bash
cd frontend
npm run dev
```

Once both processes are running, open your browser and navigate to [http://localhost:5173/](http://localhost:5173/) to use the application.

---

## 📁 Project Structure

```text
Mad2-placement-portal/
├── backend/
│   ├── api/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── company.py
│   │   ├── notification.py
│   │   └── student.py
│   ├── app.py
│   ├── cache.py
│   ├── celery_app.py
│   ├── celery_worker.py
│   ├── mail.py
│   ├── models.py
│   ├── setup_db.py
│   ├── tasks.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js
        ├── App.vue
        ├── components/
        ├── router/
        │   └── index.js
        └── views/
            ├── Home.vue
            ├── Login.vue
            ├── Register.vue
            ├── admin/
            │   ├── Dashboard.vue
            │   ├── Companies.vue
            │   ├── Students.vue
            │   ├── Jobs.vue
            │   ├── Applications.vue
            │   └── GlobalSearch.vue
            ├── company/
            │   ├── Dashboard.vue
            │   ├── Profile.vue
            │   ├── Jobs.vue
            │   ├── Applications.vue
            │   ├── Messages.vue
            │   └── Exports.vue
            └── student/
                ├── Dashboard.vue
                ├── Profile.vue
                ├── Jobs.vue
                ├── Applications.vue
                ├── Messages.vue
                └── Exports.vue
```

---

## 🌐 API Endpoints (Overview)

### Auth
- `POST /api/login` - Login for all roles
- `POST /api/register` - Register for student/company

### Admin
- `GET /api/admin/dashboard` - System stats
- `GET /api/admin/companies` - Manage companies
- `GET /api/admin/students` - Manage students
- `GET /api/admin/jobs` - Manage all job postings
- `GET /api/admin/search` - Global search across the platform

### Company
- `GET/POST /api/company/jobs` - Manage job postings
- `GET/PATCH /api/company/applications` - Review & update candidate applications
- `GET /api/company/messages` - In-app messages
- `POST /api/company/export` - Export data to CSV via Celery

### Student
- `GET /api/student/jobs` - Browse and search available jobs
- `POST /api/student/apply/<job_id>` - Apply to a job
- `GET /api/student/applications` - Track application status
- `PATCH /api/student/applications/<app_id>/respond` - Accept/Reject an offer

---

## 🔄 User Workflow

```text
Company Registers → Admin Approves → Company Posts Job
                                            ↓
Student Registers → Browses Jobs → Submits Application
                                            ↓
Company Reviews → Shortlists → Schedules Interview → Offers
                                            ↓
                                    Student Accepts/Rejects
```

---

## ✅ Features Implemented

| Feature                              | Status |
|--------------------------------------|--------|
| Role-based auth (Admin/Company/Student)| ✅ |
| JWT Token Authentication             | ✅ |
| Admin pre-seeded in database         | ✅ |
| Company approval workflow            | ✅ |
| Job posting workflow                 | ✅ |
| Student applications and tracking    | ✅ |
| Offer acceptance workflow            | ✅ |
| Interactive messages / updates       | ✅ |
| Global Search feature                | ✅ |
| CSV export (async Celery job)        | ✅ |
| Email notifications (MailHog)        | ✅ |
| Background Task processing           | ✅ |
| Redis caching implementation         | ✅ |
| Responsive Bootstrap UI              | ✅ |

---

## 💻 Tech Stack

| Layer     | Technology                     |
|-----------|-------------------------------|
| Backend   | Flask (Python)                 |
| Auth      | Flask-JWT-Extended             |
| Database  | SQLite + SQLAlchemy            |
| Caching   | Redis + Flask-Caching          |
| Jobs      | Celery + Redis                 |
| Emails    | MailHog                        |
| Frontend  | Vue 3 + Vite                   |
| Routing   | Vue Router 4                   |
| Styling   | Bootstrap 5 + custom CSS       |
