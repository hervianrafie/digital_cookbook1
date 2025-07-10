from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'rahasia-super-aman'

# Fungsi koneksi ke database PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host='db',
        dbname='db_resep',
        user='postgres',
        password='password',
        port=5432
    )

# ---------------------- ROUTE: HALAMAN UTAMA (BERANDA) ----------------------
@app.route('/index')
def index():
    if 'user_id' in session:
        return render_template('index.html', name=session['name'])
    else:
        return redirect(url_for('login'))

# ---------------------- ROUTE: REGISTER ----------------------
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
            """, (name, email, password))
            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for('login'))  # Setelah register, ke login
        except Exception as e:
            return f"Terjadi kesalahan: {e}"

    return render_template('register.html')

# ---------------------- ROUTE: LOGIN ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('index'))
        else:
            return "Login gagal! Email atau password salah."

    return render_template('login.html')

# ---------------------- ROUTE: LOGOUT ----------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Jalankan server di port 8080 agar cocok dengan Docker
mport os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)