#!/usr/bin/env python3
import cgi
import cgitb
import sqlite3
import json
import hashlib
import sys
import os

cgitb.enable()

def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password_hash))
        conn.commit()
        return {"message": "Реєстрація успішна!"}
    except sqlite3.IntegrityError:
        return {"message": "Електронна пошта вже існує!"}
    finally:
        conn.close()

# Створення бази даних, якщо її ще немає
create_database()

# Обробка даних з форми
form = cgi.FieldStorage()
if "REQUEST_METHOD" in os.environ and os.environ["REQUEST_METHOD"] == "POST":
    # Отримання JSON з вхідного потоку
    data = json.load(sys.stdin)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if username and email and password:
        response = register_user(username, email, password)
    else:
        response = {"message": "Заповніть всі поля!"}
    
    print("Content-Type: application/json\n")
    print(json.dumps(response))
