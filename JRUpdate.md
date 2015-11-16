# JR Update

## 11/15/2015

### model.py
I added `model.py` that can be used as the ORM for the database. I also added a SQLite3 database for now as a sample.

###### TODO: Implement the current database's schema as a class (or classes).

Once the schema is complete, this is how to migrate:
```bash
python model.py apichoosinator init
python model.py apichoosinator migrate
python model.py apichoosinator upgrade
```

In `app.py`, simply include `from model import db, ...`, where `...` are the names of all of the classes separated by commas. Use them in `app.py` per the following examples where the class name is Test (many more available via Google): 
```python
Test.query.all()
Test.query.filter_by(col = criteria).first()
test = Test(constructor, variables)
db.session.add(test)
db.session.commit()
```

### secret.py
Added to include all secret keys, specifically the database URI for `model.py`. `secret.py` WILL BE IGNORED from GitHub, add the following line to your local `secret.py` file:
```python
DBKEY="sqlite://apichoosinator.sqlite"
```

### SQLite3
To use SQLite (sample commands):
```bash
> sqlite3 apichoosinator.sqlite
sqlite> .tables
sqlite> .databases
sqlite> .schema tablename
sqlite> .quit
```

### .gitignore
Added .gitignore file for the following folders/files:
- venv/
- migrations/
- apichoosinator.sqlite
- secret.py

To install dependencies under virtualenv:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

To establish migrations, follow steps under model.py.

To set up database, execute all commands EXCEPT `sqlite> .schema tablename` from the SQLite3 section.

To set up secret file, create `secret.py` per the secret.py section.