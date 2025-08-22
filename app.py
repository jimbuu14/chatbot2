from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "my-postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "EM:IwltdoM,jnoi")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)
    return conn


@app.route("/", methods=['GET', 'POST'])
def todo_list():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, aufgabe FROM todo_list;")
    task = cur.fetchall()

    if request.method == "POST":
        content = request.form.get("aufgabe", "")
        if content == "":
            pass
        else:
            cur.execute(f"INSERT INTO todo_list (aufgabe) VALUES ('{content}');")
            conn.commit()
    
        aufgaben_ids = [1, 2, 3, 4, 5]
        for aufgabe_id in aufgaben_ids:
            checkbox_value = request.form.get(f"state-{ aufgabe_id }", "")
            if checkbox_value == "":
                continue           
            else:                
                #app.logger.info(f"Inhalt von aufgabe_id: {aufgabe_id}")
                cur.execute(f"UPDATE todo_list SET erledigt = {checkbox_value} WHERE id = {aufgabe_id};")
                conn.commit()

    cur.execute("SELECT erledigt FROM todo_list;")
    finished = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('todo.html', task=task, finished=finished)


@app.route("/chatbot/<name>", methods=['GET', 'POST'])
def chatbot(name):

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        benutzer = name
        content = request.form.get("content", "")
        cur.execute(f"INSERT INTO my_table (benutzer, content) VALUES ('{benutzer}', '{content}');")
        conn.commit()
    
    cur.execute("SELECT id, benutzer, content, created_at FROM my_table ORDER BY created_at ASC;")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', messages=messages, name=name)

if __name__ == "__main__":
    conn_init = get_db_connection() 
    if conn_init:
        cur_init = conn_init.cursor()
        cur_init.execute("""
            CREATE TABLE IF NOT EXISTS my_table (
                id SERIAL PRIMARY KEY, 
                benutzer VARCHAR(100) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur_init.execute("""
            CREATE TABLE IF NOT EXISTS todo_list (
                id SERIAL PRIMARY KEY,
                aufgabe TEXT NOT NULL,
                erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                beendet_am TIMESTAMP,
                erledigt BOOLEAN not null default false
            );
        """)

        conn_init.commit()
        cur_init.close()
        conn_init.close()
    app.run(host='0.0.0.0', debug=True)





