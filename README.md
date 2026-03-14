# CampusNote

CampusNote is a Flask web app for sharing and discovering academic notes across universities, departments, years, semesters, and subjects.

Users can register, log in, upload notes (PDF/images), browse notes through a hierarchical academic structure, and search notes with filters.

## Features

- User authentication
  - Register, login, logout
  - Password hashing with `Flask-Bcrypt`
- Account management
  - Update username/email
  - Upload and resize profile picture
- Note uploads
  - Upload note files (`.pdf`, `.jpg`, `.jpeg`, `.png`)
  - Store note metadata linked to subject hierarchy
- Hierarchical browsing
  - University -> Department -> Year -> Semester -> Subject -> Notes
- Search and filtering
  - Keyword search in title, description, and subject name
  - Optional filtering by university/department/year/semester/subject
- Seed script
  - Populate sample academic hierarchy data for RUET, BUET, and DU

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- SQLite
- Pillow

## Project Structure

```text
project-campusnote/
├── campusnote/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── static/
│   │   ├── main.css
│   │   ├── profile_pics/
│   │   └── uploads/
│   │       └── notes/
│   └── templates/
│       ├── layout.html
│       ├── home.html
│       ├── register.html
│       ├── login.html
│       ├── account.html
│       ├── browse.html
│       ├── search.html
│       └── upload_notes.html
├── run.py
├── seed_db.py
└── requirements.txt
```

## Getting Started

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd project-campusnote
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize and seed database

```bash
python seed_db.py
```

This creates tables and seeds hierarchy data.

### 5. Run the app

```bash
python run.py
```

Open your browser at:

- `http://127.0.0.1:5000`

## Database Notes

- The app uses SQLite with URI `sqlite:///site.db`.
- In Flask, this resolves to `instance/site.db`.

## Useful Commands

```bash
# run app
python run.py

# seed hierarchy data
python seed_db.py
```

## Current Status

Implemented in current codebase:

- Authentication and account update flows
- Note upload with file validation and storage
- Hierarchical browse route
- Search page with keyword and hierarchy filters
- AJAX endpoints for dependent dropdown loading

## Contributing

1. Create a feature branch
2. Make changes
3. Test locally
4. Open a pull request

## License

No license file is currently defined for this repository.
