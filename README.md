# Educational Document Management System

A full-stack web application for managing and organizing educational documents. This system allows users to upload course materials (PDFs, DOCX, TXT files), extract text content for AI processing, and manage their document library with metadata like module name, branch, and academic year.

## Features

### Backend (Flask)
- JWT-based authentication with secure password hashing
- Role-based user management (Student, Professor, Manager, Admin)
- Document upload with automatic text extraction
- RESTful API architecture with blueprint organization
- PostgreSQL database with migrations
- File type validation and secure file handling

### Frontend (React)
- Modern, responsive UI with Tailwind CSS
- User authentication (Login/Register)
- Document upload with drag-and-drop support
- Document library with search and filtering
- User profile management
- Protected routes and JWT token management

## Project Structure

```
.
├── backend/
│   ├── app.py                 # Main application entry point
│   ├── config.py              # Application configuration
│   ├── requirements.txt       # Python dependencies
│   ├── migrations/            # Database migrations
│   └── src/
│       ├── auth/              # Authentication module
│       ├── users/             # User management module
│       ├── documents/         # Document management module
│       └── extensions.py      # Flask extensions
│
└── frontend/
    ├── src/
    │   ├── components/        # React components
    │   ├── pages/             # Page components
    │   ├── contexts/          # React contexts
    │   ├── services/          # API services
    │   └── App.jsx            # Main App component
    ├── package.json
    └── vite.config.js
```

## Tech Stack

### Backend
- Flask 3.0
- PostgreSQL (with SQLAlchemy ORM)
- Flask-JWT-Extended for authentication
- Flask-Migrate for database migrations
- PyMuPDF, python-docx for document processing
- Flask-CORS for cross-origin requests

### Frontend
- React 19
- Vite for build tooling
- React Router v7 for routing
- Axios for API requests
- Tailwind CSS v4 for styling

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL database

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

5. Run database migrations:
```bash
flask db upgrade
```

6. Start the development server:
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Update the `.env` file if your backend runs on a different port:
```env
VITE_API_URL=http://localhost:5000
```

5. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `POST /auth/logout` - Logout (client-side token removal)

### Users
- `GET /users/profile` - Get current user profile (requires authentication)

### Documents
- `POST /documents/upload` - Upload a document with metadata (requires authentication)
- `GET /documents/` - List all user documents (requires authentication)

## User Roles

- **Student**: Default role for new registrations
- **Professor**: Educator role with document access
- **Manager**: Administrative role
- **Admin**: Full system access (requires manual database update)

## Security Features

- Passwords hashed with bcrypt
- JWT token-based authentication
- Protected API endpoints
- File type validation
- SQL injection prevention via ORM
- CORS configuration for API access

## Document Processing

The system extracts text from uploaded documents for potential AI processing:
- **PDF files**: Extracted using PyMuPDF (fast and accurate)
- **DOCX files**: Extracted using python-docx
- **TXT files**: Direct reading with encoding support

Extracted text is stored in the database for quick AI queries without reprocessing files.

## Production Deployment

### Backend
1. Use a production WSGI server (e.g., Gunicorn):
```bash
gunicorn app:app
```

2. Set `DEBUG=False` in production
3. Use strong `SECRET_KEY` value
4. Configure proper CORS origins in `config.py`
5. Use environment variables for all sensitive data

### Frontend
1. Build the production bundle:
```bash
npm run build
```

2. Serve the `dist` folder using a web server (nginx, Apache, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is for educational purposes.
