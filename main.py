import psycopg2


with open("pas.txt", "r") as file:
    password = file.read().strip()

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password=password,
    database="EmployeeManager",
    port="5432",
)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        surname VARCHAR(255),
        email VARCHAR(255),
        team_id INTEGER,
        position_id INTEGER,
        do_evaluations BOOLEAN,
        start_date DATE,
        end_date DATE,
        status BOOLEAN,
        onboarded BOOLEAN,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
''')

conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_method_scores (
        id SERIAL PRIMARY KEY,
        employee_loop_id INTEGER,
        position_method_id INTEGER,
        score DECIMAL,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_loops (
        id SERIAL PRIMARY KEY,
        employee_id INTEGER,
        team_loop_id INTEGER,
        position_id INTEGER,
        final_score DECIMAL,
        status VARCHAR(255),
        completed_at DATE,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS position_methods (
        id SERIAL PRIMARY KEY,
        position_id INTEGER,
        method_id INTEGER,
        weight DECIMAL,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS position_loops (
        id SERIAL PRIMARY KEY,
        position_name VARCHAR(255),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS team_loops (
        id SERIAL PRIMARY KEY,
        team_loop_name VARCHAR(255),
        team_id INTEGER,
        position_id INTEGER,
        start_date DATE,
        end_date DATE,
        status VARCHAR(255),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        id SERIAL PRIMARY KEY,
        team_name VARCHAR(255),
        partner VARCHAR(255),
        location VARCHAR(255),
        specifications VARCHAR(255),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
 ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS methods (
        id SERIAL PRIMARY KEY,
        description VARCHAR(255),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
''')

conn.commit()
conn.close()
