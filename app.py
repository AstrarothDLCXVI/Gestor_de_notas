from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = '1234'  # IMPORTANTE: Cambiar en producción

# Función para conectar a la base de datos
def get_db():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear las tablas si no existen
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta principal - redirige al login o dashboard
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash de la contraseña
        hashed_password = generate_password_hash(password)
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, hashed_password))
            conn.commit()
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El usuario o email ya existe.', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('login.html')

# Ruta de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard - muestra todas las notas del usuario
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    notes = conn.execute('''
        SELECT * FROM notes 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', notes=notes)

# Crear nueva nota
@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db()
        conn.execute('INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)',
                    (session['user_id'], title, content))
        conn.commit()
        conn.close()
        
        flash('Nota creada exitosamente.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('note_form.html', note=None)

# Editar nota
@app.route('/note/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    conn = get_db()
    
    # Verificar que la nota pertenece al usuario
    note = conn.execute('SELECT * FROM notes WHERE id = ? AND user_id = ?',
                       (id, session['user_id'])).fetchone()
    
    if not note:
        conn.close()
        flash('Nota no encontrada.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn.execute('''
            UPDATE notes 
            SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        ''', (title, content, id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Nota actualizada exitosamente.', 'success')
        return redirect(url_for('dashboard'))
    
    conn.close()
    return render_template('note_form.html', note=note)

# Eliminar nota
@app.route('/note/delete/<int:id>')
@login_required
def delete_note(id):
    conn = get_db()
    conn.execute('DELETE FROM notes WHERE id = ? AND user_id = ?',
                (id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Nota eliminada exitosamente.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()  # Crear tablas si no existen
    app.run(debug=True)