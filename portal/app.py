"""
Syndicate Web Portal — "Stellar Dawn" Login System
Port 9001 — Intentionally vulnerable to SQL Injection (Stage 04).

VULNERABILITY: The login query uses string formatting instead of parameterized queries,
allowing authentication bypass via SQL injection.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = "/app/data/syndicate.db"
FLAG = "ALIEN{sq1_1nj3ct10n_succ3ss}"
ADMIN_TOKEN = "XENO-CLEARANCE-7742"  # Token needed to unlock Stage 05


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with the users table."""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'member'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS communications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check if admin user exists
    existing = cursor.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not existing:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "X3n0M0rph_Pr0t0c0l_99!", "supreme_leader")
        )
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("acolyte_1", "st4rs_4l1gn", "acolyte")
        )
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("acolyte_2", "c0sm1c_d4wn", "acolyte")
        )

        # Seed communications
        comms = [
            ("admin", "Brothers and sisters, our celestial guests have arrived. The Great Alignment is upon us."),
            ("acolyte_1", "Supreme Leader, the safe house in Sector 4 is prepared. Supplies for 30 days."),
            ("admin", "Excellent. The visitors require specific atmospheric conditions. Nitrogen generators are en route."),
            ("acolyte_2", "The authorities suspect nothing. Our cover as a 'spiritual retreat' holds firm."),
            ("admin", "Phase 2 begins at midnight. All acolytes must report to the underground chapel."),
            ("admin", f"CLASSIFIED — Administrative clearance token for secure vault access: {ADMIN_TOKEN}"),
            ("acolyte_1", "The drone wreckage has been secured. Memory core extracted before A.R.G.U.S. arrived."),
            ("admin", f"AUTHORIZATION FLAG FOR EXTERNAL VERIFICATION: {FLAG}"),
        ]
        for sender, msg in comms:
            cursor.execute(
                "INSERT INTO communications (sender, message) VALUES (?, ?)",
                (sender, msg)
            )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    """Redirect to login page."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login endpoint — INTENTIONALLY VULNERABLE TO SQL INJECTION.

    The query uses string formatting, allowing payloads like:
        username: ' OR '1'='1
        password: ' OR '1'='1
    """
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()

        # VULNERABLE QUERY — Uses string formatting instead of parameterized queries
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        try:
            user = conn.execute(query).fetchone()
            conn.close()

            if user:
                session["logged_in"] = True
                session["username"] = user["username"] if user["username"] else "Unknown"
                session["role"] = user["role"] if user["role"] else "member"
                return redirect(url_for("dashboard"))
            else:
                flash("ACCESS DENIED — Invalid credentials.", "error")
        except sqlite3.Error as e:
            conn.close()
            flash(f"SYSTEM ERROR — Database malfunction: {str(e)}", "error")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """Protected dashboard — shows communications and flag after successful login."""
    if not session.get("logged_in"):
        flash("UNAUTHORIZED — Authentication required.", "error")
        return redirect(url_for("login"))

    conn = get_db()
    comms = conn.execute("SELECT * FROM communications ORDER BY timestamp ASC").fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        username=session.get("username", "Unknown"),
        role=session.get("role", "member"),
        communications=comms,
        flag=FLAG,
        admin_token=ADMIN_TOKEN
    )


@app.route("/logout")
def logout():
    """Clear session."""
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=9001, debug=False)
