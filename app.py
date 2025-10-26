from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'innvotex_secret_key_2024'

# Veritabanı başlatma
def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT,
                  message TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# --- Context Processor ---
@app.context_processor
def inject_now():
    return {'now': datetime.now().year}

# --- Rotalar ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iletisim', methods=['GET', 'POST'])
def iletisim():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        # Veritabanına kaydet
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, email, phone, message) VALUES (?, ?, ?, ?)",
                  (name, email, phone, message))
        conn.commit()
        conn.close()
        
        flash('Mesajınız başarıyla gönderildi! En kısa sürede dönüş yapacağız.', 'success')
        return redirect(url_for('iletisim'))
    
    return render_template('iletisim.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# --- YENİ SAYFALAR ---
@app.route('/uretim')
def uretim():
    return render_template('uretim.html')

@app.route('/is-ortaklarimiz')
def is_ortaklarimiz():
    return render_template('is_ortaklarimiz.html')

@app.route('/hakkimizda')
def hakkimizda():
    return render_template('hakkimizda.html')

# --- ADMIN PANELİ ---
@app.route('/admin')
def admin():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    contacts = c.fetchall()
    conn.close()
    
    return render_template('admin.html', contacts=contacts)

@app.route('/admin/delete/<int:contact_id>')
def delete_contact(contact_id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    
    flash('Mesaj başarıyla silindi!', 'success')
    return redirect(url_for('admin'))

# Uygulama başladığında DB'yi başlat
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)