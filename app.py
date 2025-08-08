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

@app.route("/")
def hello_world():  
    tabelle = "my_table"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {tabelle};")
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return f"{result}"

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
        conn_init.commit()
        cur_init.close()
        conn_init.close()
    app.run(host='0.0.0.0', debug=True)





