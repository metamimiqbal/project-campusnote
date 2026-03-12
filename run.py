from campusnote import app, db

if __name__ == '__main__':
    # Ensure all SQLAlchemy models are materialized into SQLite before serving requests.
    with app.app_context():
        db.create_all()
    app.run(debug=True)

'''
then I ran this into terminal:

from campusnote import app, db; from sqlalchemy import inspect; 
with app.app_context():
    db.create_all();
    print(sorted(inspect(db.engine).get_table_names()))
'''