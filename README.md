# SmartQCM

> SmartQCM helps teachers turn course material into multiple-choice questions, manage exam sessions, and review results without extra manual work.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)

SmartQCM uses Google Gemini to generate questions from PDF and DOCX files, then stores them in a workflow built for exams, practice, and analytics.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Key Features Explained](#key-features-explained)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

---

## Features

### AI-Powered QCM Generation
- **Question Generation**: Generate QCM questions from uploaded documents with Google Gemini AI
- **Dual Generation Modes**:
  - **Professor Mode**: Creates challenging, analytical questions for official exams
  - **Student Mode**: Generates practice questions focused on key concepts and definitions
- **Customizable Parameters**: Adjust question count, difficulty level, and question type
- **PDF Export**: Generate professional PDF documents with your QCMs

### Document Management
- Upload and manage educational documents (PDF, DOCX)
- Automatic text extraction from documents
- Organize and search documents
- Support for multiple file formats

### Exam Management
- Create and manage exam sessions
- Set time limits and access controls
- Real-time exam monitoring
- Automatic grading and scoring
- View detailed exam results and analytics

### Multi-Role System
- **Professors**: Create QCMs, manage exams, and review student results
- **Students**: Take exams, practice with generated QCMs, and view results
- **Managers**: Oversee exams and results across the platform
- **Admins**: Manage the full system

### Analytics & Statistics
- Performance dashboards for all user roles
- Exam result analytics
- Student progress tracking
- Charts and graphs for quick review

### Security & Authentication
- JWT-based authentication
- Email activation system
- Password reset functionality
- Role-based access control
- Secure file uploads

---

## Tech Stack

### Frontend
- **React 19** - Modern UI library
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Migrate** - Database migrations with Alembic
- **Google Generative AI** - AI question generation
- **PyMuPDF** - PDF processing
- **python-docx** - DOCX processing
- **ReportLab** - PDF generation

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 16+** and npm
- **PostgreSQL 12+**
- **Google API Key** (for Gemini AI)
- **Docker and Docker Compose**

---

## Quick Start

```bash
git clone <repository-url>
cd smart-qcm

# Configure environment variables in backend/.env
# Build and start the stack
docker compose up -d --build

# Run database migrations
docker compose exec backend flask db upgrade
```

Open the application at:
- Frontend: http://localhost
- Backend API: http://localhost:5000

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-qcm
```

### 2. Backend Setup (local development)

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration (local development)

Create a PostgreSQL database and update the connection string in your `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/smartqcm_db
```

### 4. Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/smartqcm_db

# Security
SECRET_KEY=your-secret-key-here

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Google AI
GOOGLE_API_KEY=your-google-api-key-here

# Email configuration (for activation and password reset)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Frontend URL used in activation/reset links
FRONTEND_URL=http://localhost:80
```

### 5. Database Migrations (local development)

```bash
# Initialize database (first time only)
flask db init

# Run migrations
flask db upgrade
```

### 6. Frontend Setup (local development)

```bash
cd frontend

# Install dependencies
npm install
```

### 7. Frontend Environment

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:5000
```

---

## Running the Application

### Run with Docker

```bash
docker compose up -d --build
docker compose exec backend flask db upgrade
```

The services will run on:
- Frontend: `http://localhost`
- Backend API: `http://localhost:5000`

### Run locally without Docker

```bash
cd backend
python app.py

cd ../frontend
npm run dev
```

The backend will run on `http://localhost:5000` and the frontend on `http://localhost:5173`.

---

## Project Structure

```
smart-qcm/
├── docker-compose.yml         # Multi-service orchestration (db, backend, frontend)
├── backend/
│   ├── Dockerfile             # Backend multi-stage image (Python)
│   ├── .dockerignore          # Backend Docker build context exclusions
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── migrations/            # Database migrations
│   ├── uploads/               # Uploaded documents storage
│   └── src/
│       ├── auth/              # Authentication module
│       ├── documents/         # Document management
│       ├── exams/             # Exam session management
│       ├── qcm/               # QCM generation and management
│       ├── school/            # School/branch management
│       ├── stats/             # Statistics and analytics
│       └── users/             # User management
│
└── frontend/
    ├── Dockerfile             # Frontend multi-stage image (Node build + Nginx)
    ├── .dockerignore          # Frontend Docker build context exclusions
    ├── nginx.conf             # Nginx configuration for serving Vite build
    ├── src/
    │   ├── components/        # Reusable React components
    │   ├── contexts/          # React contexts (Auth, etc.)
    │   ├── pages/             # Page components
    │   ├── services/          # API service layer
    │   └── App.jsx            # Main application component
    ├── package.json           # Node.js dependencies
    └── vite.config.js         # Vite configuration
```

---

## Key Features Explained

### AI Question Generation

The system uses Google Gemini AI to generate questions in two distinct modes:

- **Professor Mode**: Lower temperature (0.3) for deterministic, precise questions. Focuses on deep understanding, analysis, and synthesis.
- **Student Mode**: Higher temperature (0.9) for varied practice questions. Focuses on memory, definitions, and basic concepts.

### Exam Flow

1. **Professor** uploads a document
2. **Professor** generates QCM questions from the document
3. **Professor** creates an exam session with the QCM
4. **Students** take the exam within the specified time window
5. **System** automatically grades and provides results
6. **Professors/Managers** can view detailed analytics

---

## API Documentation

The backend includes Swagger/OpenAPI documentation. Once the server is running, visit:

```
http://localhost:5000/apidocs
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Acknowledgments

- Google Gemini AI for question generation capabilities
- The open-source community for excellent tools and libraries

---

<div align="center">

**Made with ♥️**

[⬆ Back to Top](#smartqcm-)

</div>
