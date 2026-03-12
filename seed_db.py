from campusnote import app, db
from campusnote.models import University, Department, Year, Semester, Subject


def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    params = dict(kwargs)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    db.session.add(instance)
    db.session.flush()
    return instance


def seed_hierarchy():
    # Example structured data: University -> Department -> Year -> Semester -> Subjects
    data = {
        "RUET": {
            "CSE": {
                "1st Year": {
                    "1st Semester": ["Mathematics I", "Physics I", "Programming Fundamentals"],
                    "2nd Semester": ["Mathematics II", "Physics II", "Discrete Mathematics"],
                },
                "2nd Year": {
                    "1st Semester": ["Data Structures", "Digital Logic Design", "Statistics"],
                    "2nd Semester": ["Algorithms", "Object Oriented Programming", "Database Systems"],
                },
                "3rd Year": {
                    "1st Semester": ["Operating Systems", "Computer Networks", "Numerical Methods"],
                    "2nd Semester": ["Software Engineering", "Compiler Design", "Microprocessors"],
                },
                "4th Year": {
                    "1st Semester": ["Machine Learning", "Distributed Systems", "Information Security"],
                    "2nd Semester": ["Project/Thesis", "Advanced Topics in CSE"],
                },
            },
            "EEE": {
                "1st Year": {
                    "1st Semester": ["Mathematics I", "Chemistry", "Basic Electrical Engineering"],
                    "2nd Semester": ["Mathematics II", "Physics", "Circuit Analysis I"],
                },
                "2nd Year": {
                    "1st Semester": ["Circuit Analysis II", "Electronic Devices", "Signals and Systems"],
                    "2nd Semester": ["Electromagnetic Fields", "Electrical Machines I", "Control Systems"],
                },
            },
        },
        "BUET": {
            "CSE": {
                "1st Year": {
                    "1st Semester": ["Structured Programming", "Calculus", "Linear Algebra"],
                    "2nd Semester": ["Data Structures", "Discrete Math", "Digital Logic"],
                },
                "2nd Year": {
                    "1st Semester": ["Algorithms", "Database", "Computer Architecture"],
                    "2nd Semester": ["Operating Systems", "Computer Networks", "Theory of Computation"],
                },
            },
            "ME": {
                "1st Year": {
                    "1st Semester": ["Engineering Mechanics", "Thermodynamics I", "Mathematics I"],
                    "2nd Semester": ["Fluid Mechanics", "Manufacturing Processes", "Mathematics II"],
                },
            },
        },
        "DU": {
            "CSE": {
                "1st Year": {
                    "1st Semester": ["Introduction to Computing", "Calculus", "Physics"],
                    "2nd Semester": ["Data Structures", "Discrete Mathematics", "Digital Systems"],
                },
                "2nd Year": {
                    "1st Semester": ["Algorithms", "Database Systems", "Object Oriented Programming"],
                    "2nd Semester": ["Operating Systems", "Computer Networks", "Software Engineering"],
                },
            },
        },
    }

    for uni_name, departments in data.items():
        uni = get_or_create(University, name=uni_name)

        for dept_name, years in departments.items():
            dept = get_or_create(Department, name=dept_name, university_id=uni.id)

            for year_label, semesters in years.items():
                year = get_or_create(Year, label=year_label, department_id=dept.id)

                for sem_label, subjects in semesters.items():
                    sem = get_or_create(Semester, label=sem_label, year_id=year.id)

                    for subject_name in subjects:
                        get_or_create(Subject, name=subject_name, semester_id=sem.id)

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_hierarchy()
        print("Seed completed successfully.")