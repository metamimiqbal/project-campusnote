PROMPT START

You are an expert project presentation script writer for a university software project viva/defense.

Your task:
Create a complete, realistic, detailed speaking script for a 3-person team presentation of the project described below.
Important context: this project was actually built by one person, but the presentation must distribute responsibilities across 3 roles in a believable and technically accurate way.

Output quality requirements:
1. Do not miss any project detail provided below.
2. Do not invent features that are not implemented.
3. Clearly separate who says what.
4. Keep technical explanations accurate but presentation-friendly.
5. Include transitions between speakers.
6. Include demo narration lines (what to click, what appears, what to say).
7. Include likely adviser questions and strong model answers.
8. Tone: confident, student-professional, clear English.
9. Script should feel natural to speak, not robotic.

Project identity:
- Project title: CampusNote
- Developer name: Tamim Iqbal
- GitHub username: metamimiqbal
- City/Country: Dhaka, Bangladesh
- Date reference: March 2026

Core project concept:
CampusNote is a Flask web app for sharing and discovering academic notes across a hierarchy:
University -> Department -> Year -> Semester -> Subject -> Notes

Main user goals:
- Register/login securely
- Upload notes (pdf/image)
- Browse notes through academic hierarchy
- Search notes with keyword + filters
- Manage account/profile image
- Open/download note files

Tech stack and dependencies:
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- email-validator
- Pillow
- SQLite database
- Bootstrap 5.3 + Bootstrap Icons
- Custom CSS theme system with multiple theme presets

App configuration and startup behavior:
- Flask app with SQLAlchemy, Bcrypt, LoginManager initialized in app package.
- Secret key read from environment variables.
- Database URI defaults to sqlite:///site.db (resolves to instance/site.db).
- run.py calls db.create_all() inside app context before app.run(debug=True).
- seed_db.py also calls db.create_all() then seeds hierarchy data.

Authentication details:
- Register flow:
  - Validates username/email uniqueness
  - Hashes password with Bcrypt
  - Saves user
  - Auto logs in newly created user
  - Uses flash success message
- Login flow:
  - Email + password + remember me
  - Verifies bcrypt hash
  - Supports next page redirect
- Logout route protected by login_required
- Login manager has custom login message and login view.

Account management details:
- Account page allows username/email update
- Username/email validators allow current user’s own values
- Profile picture upload accepted (jpg/png)
- Uploaded profile image is resized to 125x125 using Pillow
- User can view “My Uploads” list on account page

Database schema details:
- University:
  - id, unique name
  - one-to-many departments
- Department:
  - id, name, university_id
  - unique(name, university_id)
  - one-to-many years
- Year:
  - id, label, department_id
  - unique(label, department_id)
  - one-to-many semesters
- Semester:
  - id, label, year_id
  - unique(label, year_id)
  - one-to-many subjects
- Subject:
  - id, name, semester_id
  - unique(name, semester_id)
  - one-to-many notes
- User:
  - id, username unique, email unique, password hashed
  - profile_pic default, joined_at
  - one-to-many notes
- Note:
  - id, title, description, file_path, uploaded_at
  - user_id foreign key
  - subject_id foreign key
- Rating:
  - id, score
  - user_id foreign key
  - note_id foreign key
  - unique(user_id, note_id)

Important implementation status note:
- Rating model exists in schema but full rating routes/UI are not fully implemented in current routes/templates.
- Note detail route/page with rating actions is not currently implemented.
- Script must mention this as current scope limitation/future work, not as already completed feature.

Browse feature implementation:
- Route supports hierarchical drill-down using query params:
  - uni, dept, year, sem, sub
- Stepwise behavior:
  - no uni -> list universities
  - uni only -> list departments
  - uni+dept -> list years
  - uni+dept+year -> list semesters
  - uni+dept+year+sem -> list subjects
  - full selection including sub -> list notes for that subject
- Template includes breadcrumb navigation and step cards.
- At notes level, shows title, description, uploader, upload date, open file button.
- If no notes, shows empty-state prompt.

Search feature implementation:
- Search route joins Note with Subject -> Semester -> Year -> Department -> University.
- Keyword query matches:
  - note title
  - note description
  - subject name
- Optional filters:
  - university, department, year, semester, subject
- Results sorted by uploaded_at descending.
- Template includes:
  - search bar
  - collapsible filters panel
  - active filters indicator
  - result count text
  - note cards with subject/uploader/date and open file action.

Upload feature implementation:
- Upload page requires login.
- Upload form includes:
  - title
  - description (optional)
  - university_id, department_id, year_id, semester_id, subject_id
  - note_file (pdf/jpg/jpeg/png)
- Server-side logic:
  - dynamically scopes select choices based on submitted parent values
  - validates hierarchy consistency (department belongs to selected university, etc.)
  - validates file extension on server
  - saves file under static/uploads/notes with random secure filename
  - stores relative file path
  - creates note row with current_user and subject
- Flash success/failure messages.

Dynamic dropdown API endpoints:
- api/departments (requires login)
- api/years (requires login)
- api/semesters (requires login)
- api/subjects (requires login)
- Upload page JavaScript listens for parent select change and fetches child options.

Home page behavior:
- Guest view:
  - Hero section, CTA buttons (Join Free, Browse Notes)
  - Feature cards (organized notes, quick search, peer powered)
- Logged-in view:
  - Personalized greeting
  - quick search bar
  - quick links (browse, upload, account)
  - recent uploads (up to 8 newest notes)
  - empty state if no notes

Layout/UI design details:
- Bootstrap-based responsive layout
- Navbar with conditional links based on auth state
- Flash messages displayed globally
- Footer with project tagline
- Account dropdown with avatar
- Theme switcher in navbar:
  - Stores selected theme in localStorage and cookie
  - Available themes:
    - Indigo Classic
    - Cyberpunk Grid
    - Crimson Dusk
    - Emerald Night
    - Copper Sand
    - Sunrise Paper
- Custom CSS tokens for colors, borders, shadows, typography, cards, forms, note cards, breadcrumb styling.

Seed data details:
- seed_db.py populates structured hierarchy for:
  - RUET
  - BUET
  - DU
- Includes departments like CSE/EEE/ME
- Includes multiple years and semesters
- Includes many subject names per semester
- Uses get_or_create pattern and commits at end.

Project structure overview:
- app package contains:
  - init
  - models
  - forms
  - routes
  - static (main.css, profile_pics, uploads/notes)
  - templates (layout, home, register, login, account, browse, search, upload notes)
- root contains:
  - run.py
  - seed_db.py
  - requirements.txt
  - README and planning docs

Role distribution for script (fixed, must follow):
1. Role A (Tamim): Project Lead + Backend Integration
   - Overall architecture, Flask routing, auth flow, upload workflow, integration logic, final testing and delivery.
2. Role B (Friend 1): Frontend Engineer
   - Templates, Bootstrap layout, CSS system, theme switcher UX, responsive behavior, page-level UI flow.
3. Role C (Friend 2): Database and Data Layer Engineer
   - Schema design, constraints, relationships, SQLite + SQLAlchemy, seeding strategy, query/filter logic support.

Now generate:
1. A full 12-15 minute presentation script with speaker labels:
   - Role A:
   - Role B:
   - Role C:
2. A slide-by-slide structure (or section-by-section if no slides).
3. Demo walkthrough script with exact speaking lines and handoff cues.
4. A concise “limitations and future work” section that honestly reflects current implementation status.
5. 12 likely adviser questions with polished answers, assigned to the right role.
6. A final closing statement by Role A.

Formatting constraints for your output:
- Use clean headings
- Use natural spoken language
- Keep each speaking turn manageable in length
- Include explicit transitions like “Now I’ll hand over to…”
- No fabricated features beyond provided details

PROMPT END
