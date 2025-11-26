# app.py
import os
import sqlite3
import secrets
import string
import base64
from io import BytesIO
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, abort
import qrcode

app = Flask(__name__)
DB_NAME = "shortener.db"
BASE_URL = "http://127.0.0.1:5000"  

BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:5000')

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(secrets.choice(chars) for _ in range(length))
        if not url_exists(code):
            return code

def url_exists(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def generate_qr_base64(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        original_url = request.form["url"].strip()
        
        if not original_url.startswith(("http://", "https://")):
            original_url = "https://" + original_url

        short_code = generate_short_code()
        short_url = f"{BASE_URL}/@{short_code}"
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO urls (original_url, short_code, created_at) VALUES (?, ?, ?)",
            (original_url, short_code, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

        qr_base64 = generate_qr_base64(short_url)

        result = {
            "short_url": short_url,
            "qr_code": qr_base64,
            "original_url": original_url
        }

    return render_template("index.html", result=result)

@app.route("/@<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return redirect(row[0])
    else:
        abort(404, description="Short URL not found")

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", error="URL pendek tidak ditemukan."), 404

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)