import os
import sqlite3
import json
import time
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Data'
app.config['SCREENSHOT_FOLDER'] = os.path.join('Data', 'screenshots')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.secret_key = 'barksecretkey'

if not os.path.exists('Data'):
    os.makedirs('Data')
if not os.path.exists(app.config['SCREENSHOT_FOLDER']):
    os.makedirs(app.config['SCREENSHOT_FOLDER'])

# Load password
with open("password.json") as f:
    PASSWORD = json.load(f)["password"]

# DB Setup
def init_db():
    with sqlite3.connect("mods.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mod_name TEXT NOT NULL,
                author TEXT NOT NULL,
                version TEXT NOT NULL,
                description TEXT NOT NULL,
                dependencies TEXT,
                filename TEXT NOT NULL,
                screenshot TEXT
            )
        """)
init_db()

# Routes
@app.route('/')
def index():
    with sqlite3.connect("mods.db") as conn:
        mods = conn.execute("SELECT * FROM mods ORDER BY id DESC").fetchall()
    return render_template("index.html", mods=mods)

@app.route('/create')
def create():
    return render_template("upload.html")

@app.route('/upload', methods=['POST'])
def upload():
    mod_name = request.form['mod_name']
    author = request.form['author']
    version = request.form['version']
    description = request.form['description']
    dependencies = request.form['dependencies']
    mod_file = request.files['mod_file']
    screenshot = request.files['screenshot']

    if mod_file and mod_name and author and version and description:
        mod_filename = mod_file.filename
        mod_path = os.path.join(app.config['UPLOAD_FOLDER'], mod_filename)
        mod_file.save(mod_path)

        screenshot_filename = None
        if screenshot and screenshot.filename != "":
            screenshot_filename = screenshot.filename
            screenshot_path = os.path.join(app.config['SCREENSHOT_FOLDER'], screenshot_filename)
            screenshot.save(screenshot_path)

        with sqlite3.connect("mods.db") as conn:
            conn.execute("""
                INSERT INTO mods (mod_name, author, version, description, dependencies, filename, screenshot)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (mod_name, author, version, description, dependencies, mod_filename, screenshot_filename))

        flash("Mod uploaded successfully!")
    else:
        flash("Missing required fields!")

    return redirect(url_for('index'))

@app.route('/download/<int:mod_id>')
def download(mod_id):
    with sqlite3.connect("mods.db") as conn:
        mod = conn.execute("SELECT * FROM mods WHERE id = ?", (mod_id,)).fetchone()
    if not mod:
        flash("Mod not found!")
        return redirect(url_for('index'))
    return render_template("download.html", mod=mod)

@app.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete_mod/<int:mod_id>', methods=['POST'])
def delete_mod(mod_id):
    password = request.form['password']

    if password != PASSWORD:
        flash("Wrong password!")
        return redirect(url_for('index'))

    with sqlite3.connect("mods.db") as conn:
        mod = conn.execute("SELECT filename, screenshot FROM mods WHERE id = ?", (mod_id,)).fetchone()
        if mod:
            filename, screenshot = mod
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except FileNotFoundError:
                pass
            if screenshot:
                try:
                    os.remove(os.path.join(app.config['SCREENSHOT_FOLDER'], screenshot))
                except FileNotFoundError:
                    pass
        conn.execute("DELETE FROM mods WHERE id = ?", (mod_id,))
        conn.commit()

    flash("Mod deleted.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
