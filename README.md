# Pre-dependencies.
    Python 3.6+
    Postgress

# Create a Python virtual enviroment to install python packages.
    python3 -m venv <env-name>
    source <env-name>/bin/activate
    <!-- source web_app/bin/activate  --> To activate the virtual env

# Install python dependencies.
    pip3 install --no-cache-dir -r requirements.txt

# Install postgresql.
    <!-- install postgress(default install's latest version) -->
    sudo apt-get update && apt-get install postgresql postgresql-contrib

    <!-- login as super user -->
    sudo -u postgres psql

    <!-- Create user and password, ex: CREATE USER pitch WITH PASSWORD 'test@123' -->
    CREATE USER <user> WITH PASSWORD <'password'>;

    <!-- Create database ex: CREATEDB pitch_db -->
    CREATEDB <database-name>


    Note-down the username, password and database and add values in the config/__init__.py
    example:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://<username>:<password>@127.0.0.1:5432/<database>'

# RUN the project.
    STEP 1:
        alembic upgrade head
    STEP 2:
        uvicorn app:app --reload
        # Can Also mention Host and the Port.
            #uvicorn app.main:app --host 0.0.0.0 --port 80
