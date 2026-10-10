"""
A.R.G.U.S. Threat Assessment Dashboard
Alien Reconnaissance & Global Unified Security

Main Flask application serving the CTF dashboard on Port 9000.
Handles: stage progression, flag submission, hints, file downloads, scoring.
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, send_from_directory, flash
)
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(32))

DATABASE = "/app/data/argus.db"
CHALLENGES_DIR = "/app/static/challenges"

# ─── Stage Definitions ───────────────────────────────────────────────
# Flags and stage data kept in-code (not DB) for security

STAGES = {
    1: {
        "id": 1,
        "codename": "THE LANDING ZONE",
        "domain": "OSINT / Reconnaissance",
        "domain_icon": "🛰️",
        "difficulty": "Easy",
        "difficulty_level": 1,
        "points": 100,
        "faction": "Zeta Greys",
        "faction_desc": "Scout division — first contact specialists",
        "flag": "ALIEN{37.2350_115.8111}",
        "description": """A civilian posted a cryptic text description of a crashed UFO sighting on a public forum. 
The post mentions a dried lake bed, restricted airspace, and a location in Nevada where 
"nothing officially exists." Your mission: identify the exact geographic coordinates of 
the landing site using open-source intelligence techniques.""",
        "briefing": """INTERCEPTED CIVILIAN POST (Forum: r/UnexplainedSightings)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: DesertWatcher42 | Posted: 3 hours ago

"I was out near the dry lake beds in southern Nevada last night. You know, 
the area near that base everyone talks about but nobody's supposed to know 
about? The one next to Groom Lake? 

I saw something come down HARD about 2 miles south of the main runway 
complex. Massive flash of blue-white light, then nothing. By morning, 
there were black SUVs everywhere and they'd already cordoned off the area.

The coordinates are roughly where the dried lake bed meets the mountain 
range to the south. You can see the hangars on satellite view if you 
look carefully. The crash site is on the lake bed itself.

If anyone can get exact coordinates of that base, post them in the 
standard DD.DDDD format. You know the one I'm talking about."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASK: Use Google Earth, Maps, or OSINT tools to identify the exact 
coordinates of this location. Submit as: ALIEN{latitude_longitude}
Example format: ALIEN{12.3456_78.9012}""",
        "hints": [
            {
                "text": "The text mentions a dried lake bed in Nevada near a famous restricted military test site. Search for 'Groom Lake' on Google Maps.",
                "cost": 5
            }
        ],
        "files": [],
        "requires_token": False,
    },
    2: {
        "id": 2,
        "codename": "INTERCEPTED TELEMETRY",
        "domain": "Networking / Packet Analysis",
        "domain_icon": "📡",
        "difficulty": "Easy",
        "difficulty_level": 1,
        "points": 150,
        "faction": "Proxima Sentinels",
        "faction_desc": "Communications relay operators",
        "flag": "ALIEN{n3tw0rk_ch4tt3r_d3c0d3d}",
        "description": """A.R.G.U.S. satellites intercepted a raw data stream between the landing zone and an 
orbiting relay station. The aliens are using standard Earth network protocols to blend 
in with normal internet traffic. Your mission: analyze the packet capture and find the 
hidden alien transmission buried in the noise.""",
        "briefing": """SATELLITE INTERCEPT LOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTERCEPT ID: ARGUS-SAT-7742
SOURCE: 172.25.0.50 (Unregistered ground transmitter)
DESTINATION: 172.25.0.100 (Orbital relay — geostationary)
DURATION: 4.7 seconds
PROTOCOL MIX: DNS, ARP, TCP, HTTP (standard Earth protocols used as cover)

ANALYST NOTE: The transmission is buried within standard network noise. 
Most of the traffic is routine DNS lookups and ARP requests — typical 
camouflage. However, there is suspicious TCP activity on a non-standard 
port that warrants investigation.

Download the intercepted packet capture below and analyze it using 
Wireshark or tshark. Filter out the noise and follow the data.

TASK: Find the alien transmission hidden in the PCAP file.

TIP: Not all ports are created equal. Standard services use well-known 
ports (80, 443, 53). What happens on port 4444?""",
        "hints": [
            {
                "text": "Not all packets are important. Filter for TCP traffic on non-standard ports (try port 4444), then right-click a packet and select 'Follow TCP Stream' in Wireshark.",
                "cost": 10
            }
        ],
        "files": ["telemetry.pcap"],
        "requires_token": False,
    },
    3: {
        "id": 3,
        "codename": "ROSETTA STONE",
        "domain": "Cryptography",
        "domain_icon": "🔐",
        "difficulty": "Moderate",
        "difficulty_level": 2,
        "points": 200,
        "faction": "Cipher Collective",
        "faction_desc": "Encryption & counter-intelligence unit",
        "flag": "ALIEN{b4se_g0_b00m}",
        "description": """The intercepted telemetry from Stage 02 contained an encoded directive — a message 
encrypted using what appears to be a combination of human encoding systems. The aliens 
have been studying Earth's cryptography and are using our own tools against us. 
Decode the message to reveal their next target.""",
        "briefing": """ENCRYPTED DIRECTIVE EXTRACTED FROM TELEMETRY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The following encoded string was extracted from the TCP stream 
intercepted in Stage 02. Cryptanalysis suggests it uses multiple 
layers of encoding:

ENCODED STRING:
┌──────────────────────────────────────────┐
│  TllWUkF7bzRmcl90MF9vMDB6fQ==           │
└──────────────────────────────────────────┘

ANALYSIS NOTES:
- The string appears to use a common binary-to-text encoding scheme
- After the first layer is removed, the result resembles a flag 
  format but the characters are shifted/substituted
- The shift pattern is consistent with a classical cipher known 
  since ancient Rome

TASK: Decode all layers to reveal the plaintext flag.

HINT: Humans count in Base 10. Computers often encode in Base... ?
After that first decoding, look at the structure. Something about it 
looks almost right, but shifted.""",
        "hints": [
            {
                "text": "Step 1: The string is Base64 encoded — decode it first. Step 2: The result looks like a flag but letters are shifted by 13 positions. This is called ROT13 (a Caesar cipher).",
                "cost": 10
            }
        ],
        "files": [],
        "requires_token": False,
    },
    4: {
        "id": 4,
        "codename": "THE SYNDICATE PORTAL",
        "domain": "Web Security",
        "domain_icon": "🕸️",
        "difficulty": "Moderate",
        "difficulty_level": 2,
        "points": 250,
        "faction": "Stellar Dawn Cult",
        "faction_desc": "Human sympathizers providing shelter",
        "flag": "ALIEN{sq1_1nj3ct10n_succ3ss}",
        "description": """Intelligence reports indicate a radical human group called 'Stellar Dawn' is actively 
providing shelter and resources to the alien factions. They operate a secret online 
portal for their members. A.R.G.U.S. has located the portal on Port 9001, but it's 
protected by a login system. Find a way to bypass the authentication.""",
        "briefing": """INTELLIGENCE REPORT — STELLAR DAWN ORGANIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORGANIZATION: Stellar Dawn (Human collaborator group)
LEADER: Unknown (codename: "Supreme Leader")
MEMBERS: Estimated 50-200 acolytes
PORTAL: http://localhost:9001

The Stellar Dawn portal uses a basic login authentication system 
connected to a backend database. Our preliminary scan suggests the 
web application was hastily developed with poor security practices.

OBJECTIVE: Gain access to the portal WITHOUT valid credentials. 
The portal's internal communications may contain critical intelligence 
about alien safehouse locations and an access token needed for 
subsequent operations.

APPROACH: Consider how the login form communicates with the database. 
If user inputs are not properly sanitized before being included in 
database queries, the authentication logic can be manipulated.

TARGET URL: http://localhost:9001/login""",
        "hints": [
            {
                "text": "The database trusts user input too much. Try entering ' OR '1'='1 in both the username and password fields. This manipulates the SQL query to always return true.",
                "cost": 10
            }
        ],
        "files": [],
        "requires_token": False,
    },
    5: {
        "id": 5,
        "codename": "THE CRASHED CORE",
        "domain": "Digital Forensics",
        "domain_icon": "🧬",
        "difficulty": "Hard",
        "difficulty_level": 3,
        "points": 300,
        "faction": "Navigator Drones",
        "faction_desc": "Autonomous reconnaissance & mapping units",
        "flag": "ALIEN{m3m0ry_d03s_n0t_l13}",
        "description": """A.R.G.U.S. successfully shot down an alien scout drone. While the hardware was 
destroyed on impact, our field team managed to extract a memory dump from the 
drone's navigation core before it fully corrupted. The aliens embedded a 
self-destruct code within a running process. Extract it from the memory dump.""",
        "briefing": """FIELD REPORT — DRONE RECOVERY OPERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INCIDENT: Drone shoot-down over Sector 4
STATUS: Hardware destroyed, memory core extracted
FILE: drone_core.raw (Memory dump of the navigation system)

ACCESS RESTRICTION: This file is classified. You must provide the 
administrative clearance token obtained from the Stellar Dawn portal 
(Stage 04) to download it.

ANALYSIS APPROACH:
1. Download the memory dump using your clearance token
2. Examine the file for process structures and memory regions
3. Look for suspicious processes (alien_proc, xcom_relay)
4. Extract strings from suspicious memory regions
5. Search for the self-destruct code pattern (ALIEN{...})

TOOLS: Use 'strings' and 'grep' to extract readable text from the 
binary dump. For advanced analysis, Volatility 3 can parse the 
process structures.

COMMAND EXAMPLE:
  strings drone_core.raw | grep -i "ALIEN{"
  
NOTE: The dump also contains red herrings and decoy strings. 
Look for the legitimate self-destruct code format.""",
        "hints": [
            {
                "text": "The flag is hidden within a process memory region. Use 'strings drone_core.raw | grep ALIEN{' to search for the flag pattern. Look for the one marked as SELF_DESTRUCT_CODE — that's the real flag.",
                "cost": 15
            }
        ],
        "files": ["drone_core.raw"],
        "requires_token": True,
        "required_token": "XENO-CLEARANCE-7742",
    },
    6: {
        "id": 6,
        "codename": "THE MOTHERSHIP'S PAYLOAD",
        "domain": "Reverse Engineering",
        "domain_icon": "⚙️",
        "difficulty": "Hard",
        "difficulty_level": 3,
        "points": 350,
        "faction": "Mothership Command",
        "faction_desc": "Central command — doomsday protocol architects",
        "flag": "ALIEN{r3v3rs1ng_s4v3d_34rth}",
        "description": """The final alien faction has planted a logic bomb on Earth's communication infrastructure. 
The binary 'doomsday.elf' is set to detonate and disrupt all global communications. 
It can only be disarmed with a specific 4-digit PIN, but the code is compiled and 
the source is unavailable. Reverse engineer the binary to find the correct PIN.""",
        "briefing": """CRITICAL ALERT — DOOMSDAY PROTOCOL DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THREAT LEVEL: ████████████████ MAXIMUM
PAYLOAD: doomsday.elf (64-bit Linux ELF binary)
STATUS: ARMED — Requires 4-digit PIN to disarm

The binary implements a verification function that:
1. Takes a 4-digit PIN as a command-line argument
2. Applies mathematical transformations to each digit
3. Compares the result against hardcoded expected values
4. Prints the flag ONLY if the correct PIN is provided

YOUR MISSION:
1. Download the binary: doomsday.elf
2. Load it into a disassembler (Ghidra, IDA, or GDB)
3. Locate the check_pin() function
4. Analyze the mathematical operations:
   - Each character is multiplied by a constant
   - The result is XORed with another constant
   - The final value is compared to expected bytes
5. Reverse the math to calculate the correct PIN
6. Run: ./doomsday.elf <PIN>
7. Submit the flag that is printed

TOOLS: GDB, Ghidra, IDA Free, objdump, or radare2

EXAMPLE COMMANDS:
  chmod +x doomsday.elf
  ./doomsday.elf 1234     # Test with wrong PIN
  
  # In GDB:
  gdb ./doomsday.elf
  (gdb) disas check_pin
  
  # In terminal:
  objdump -d doomsday.elf | grep -A 50 check_pin""",
        "hints": [
            {
                "text": "The check_pin function multiplies each input character by 3, then XORs the result with 0x5A (decimal 90). The expected values are stored in the binary. To reverse: for each expected byte E, the original character = (E XOR 0x5A) / 3.",
                "cost": 15
            }
        ],
        "files": ["doomsday.elf"],
        "requires_token": False,
    },
}


# ─── Database ─────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codename TEXT NOT NULL UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            score INTEGER DEFAULT 0,
            current_stage INTEGER DEFAULT 1
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER NOT NULL,
            stage_id INTEGER NOT NULL,
            submitted_flag TEXT NOT NULL,
            is_correct INTEGER DEFAULT 0,
            submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS hints_used (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER NOT NULL,
            stage_id INTEGER NOT NULL,
            hint_index INTEGER NOT NULL,
            used_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents(id),
            UNIQUE(agent_id, stage_id, hint_index)
        )
    """)

    conn.commit()
    conn.close()


def get_agent(codename):
    conn = get_db()
    agent = conn.execute("SELECT * FROM agents WHERE codename = ?", (codename,)).fetchone()
    conn.close()
    return agent


def create_agent(codename):
    conn = get_db()
    try:
        conn.execute("INSERT INTO agents (codename) VALUES (?)", (codename,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Agent already exists
    conn.close()
    return get_agent(codename)


def get_completed_stages(agent_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT stage_id FROM submissions WHERE agent_id = ? AND is_correct = 1",
        (agent_id,)
    ).fetchall()
    conn.close()
    return {row["stage_id"] for row in rows}


def get_used_hints(agent_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT stage_id, hint_index FROM hints_used WHERE agent_id = ?",
        (agent_id,)
    ).fetchall()
    conn.close()
    hints = {}
    for row in rows:
        sid = row["stage_id"]
        if sid not in hints:
            hints[sid] = set()
        hints[sid].add(row["hint_index"])
    return hints


def get_total_hint_penalty(agent_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT stage_id, hint_index FROM hints_used WHERE agent_id = ?",
        (agent_id,)
    ).fetchall()
    conn.close()
    total = 0
    for row in rows:
        stage = STAGES.get(row["stage_id"])
        if stage and row["hint_index"] < len(stage["hints"]):
            total += stage["hints"][row["hint_index"]]["cost"]
    return total


# ─── Routes ───────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page — Agent codename entry."""
    if session.get("agent_codename"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    """Register/login an agent by codename."""
    codename = request.form.get("codename", "").strip().upper()
    if not codename or len(codename) < 2 or len(codename) > 30:
        flash("Invalid codename. Use 2-30 characters.", "error")
        return redirect(url_for("index"))

    agent = create_agent(codename)
    session["agent_codename"] = codename
    session["agent_id"] = agent["id"]
    return redirect(url_for("briefing"))


@app.route("/briefing")
def briefing():
    """Mission briefing page with full lore."""
    if not session.get("agent_codename"):
        return redirect(url_for("index"))
    return render_template("briefing.html", codename=session["agent_codename"])


@app.route("/dashboard")
def dashboard():
    """Main threat assessment dashboard."""
    if not session.get("agent_codename"):
        return redirect(url_for("index"))

    agent_id = session["agent_id"]
    agent = get_agent(session["agent_codename"])
    completed = get_completed_stages(agent_id)
    used_hints = get_used_hints(agent_id)
    hint_penalty = get_total_hint_penalty(agent_id)

    # Calculate score
    total_score = 0
    for sid in completed:
        if sid in STAGES:
            total_score += STAGES[sid]["points"]
    total_score -= hint_penalty

    # Determine which stages are accessible (sequential unlock)
    stage_status = {}
    for sid, stage in STAGES.items():
        if sid in completed:
            stage_status[sid] = "NEUTRALIZED"
        elif sid == 1 or (sid - 1) in completed:
            stage_status[sid] = "ACTIVE"
        else:
            stage_status[sid] = "LOCKED"

    # Total possible points
    max_points = sum(s["points"] for s in STAGES.values())

    return render_template(
        "dashboard.html",
        codename=session["agent_codename"],
        stages=STAGES,
        stage_status=stage_status,
        completed=completed,
        total_score=total_score,
        max_points=max_points,
        hint_penalty=hint_penalty,
        stages_completed=len(completed),
        total_stages=len(STAGES)
    )


@app.route("/stage/<int:stage_id>")
def stage_detail(stage_id):
    """Individual stage detail page."""
    if not session.get("agent_codename"):
        return redirect(url_for("index"))

    if stage_id not in STAGES:
        flash("Stage not found.", "error")
        return redirect(url_for("dashboard"))

    agent_id = session["agent_id"]
    completed = get_completed_stages(agent_id)

    # Check if stage is accessible
    if stage_id != 1 and (stage_id - 1) not in completed:
        flash("ACCESS DENIED — Complete the previous stage first.", "error")
        return redirect(url_for("dashboard"))

    stage = STAGES[stage_id]
    is_completed = stage_id in completed
    used_hints = get_used_hints(agent_id).get(stage_id, set())

    return render_template(
        "stage.html",
        stage=stage,
        is_completed=is_completed,
        used_hints=used_hints,
        codename=session["agent_codename"]
    )


@app.route("/submit/<int:stage_id>", methods=["POST"])
def submit_flag(stage_id):
    """Flag submission endpoint (AJAX)."""
    if not session.get("agent_codename"):
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    if stage_id not in STAGES:
        return jsonify({"success": False, "message": "Invalid stage."}), 404

    agent_id = session["agent_id"]
    completed = get_completed_stages(agent_id)

    # Check access
    if stage_id != 1 and (stage_id - 1) not in completed:
        return jsonify({"success": False, "message": "Stage locked."}), 403

    # Already completed
    if stage_id in completed:
        return jsonify({"success": False, "message": "Stage already neutralized."}), 400

    submitted_flag = request.json.get("flag", "").strip()
    stage = STAGES[stage_id]

    # Record submission
    conn = get_db()
    is_correct = 1 if submitted_flag == stage["flag"] else 0
    conn.execute(
        "INSERT INTO submissions (agent_id, stage_id, submitted_flag, is_correct) VALUES (?, ?, ?, ?)",
        (agent_id, stage_id, submitted_flag, is_correct)
    )

    if is_correct:
        # Update agent's current stage
        conn.execute(
            "UPDATE agents SET current_stage = ? WHERE id = ? AND current_stage <= ?",
            (stage_id + 1, agent_id, stage_id)
        )

    conn.commit()
    conn.close()

    if is_correct:
        return jsonify({
            "success": True,
            "message": f"FLAG ACCEPTED — {stage['faction']} faction neutralized!",
            "points": stage["points"]
        })
    else:
        return jsonify({
            "success": False,
            "message": "INCORRECT — Flag does not match. Try again, Agent."
        })


@app.route("/hint/<int:stage_id>/<int:hint_index>", methods=["POST"])
def request_hint(stage_id, hint_index):
    """Hint request endpoint (AJAX)."""
    if not session.get("agent_codename"):
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    if stage_id not in STAGES:
        return jsonify({"success": False, "message": "Invalid stage."}), 404

    stage = STAGES[stage_id]
    if hint_index < 0 or hint_index >= len(stage["hints"]):
        return jsonify({"success": False, "message": "Invalid hint."}), 404

    agent_id = session["agent_id"]
    hint = stage["hints"][hint_index]

    # Record hint usage
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO hints_used (agent_id, stage_id, hint_index) VALUES (?, ?, ?)",
            (agent_id, stage_id, hint_index)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already used

    conn.close()

    return jsonify({
        "success": True,
        "hint": hint["text"],
        "cost": hint["cost"]
    })


@app.route("/verify-token", methods=["POST"])
def verify_token():
    """Verify the admin token from Stage 04 to unlock Stage 05 downloads."""
    if not session.get("agent_codename"):
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    token = request.json.get("token", "").strip()
    if token == "XENO-CLEARANCE-7742":
        session["vault_access"] = True
        return jsonify({"success": True, "message": "CLEARANCE GRANTED — Vault access unlocked."})
    else:
        return jsonify({"success": False, "message": "INVALID TOKEN — Access denied."})


@app.route("/download/<filename>")
def download_file(filename):
    """Serve challenge files with access control."""
    if not session.get("agent_codename"):
        return redirect(url_for("index"))

    # Stage 05 file requires vault access
    if filename == "drone_core.raw" and not session.get("vault_access"):
        flash("ACCESS DENIED — You need the clearance token from Stage 04.", "error")
        return redirect(url_for("stage_detail", stage_id=5))

    safe_files = ["telemetry.pcap", "drone_core.raw", "doomsday.elf"]
    if filename not in safe_files:
        flash("File not found.", "error")
        return redirect(url_for("dashboard"))

    return send_from_directory(CHALLENGES_DIR, filename, as_attachment=True)


@app.route("/logout")
def logout():
    """Clear session and return to landing."""
    session.clear()
    return redirect(url_for("index"))


@app.route("/api/stats")
def api_stats():
    """API endpoint for dashboard statistics."""
    if not session.get("agent_codename"):
        return jsonify({"error": "Not authenticated"}), 401

    agent_id = session["agent_id"]
    completed = get_completed_stages(agent_id)
    hint_penalty = get_total_hint_penalty(agent_id)
    total_score = sum(STAGES[sid]["points"] for sid in completed) - hint_penalty

    return jsonify({
        "codename": session["agent_codename"],
        "stages_completed": len(completed),
        "total_stages": len(STAGES),
        "score": total_score,
        "max_score": sum(s["points"] for s in STAGES.values()),
        "hint_penalty": hint_penalty,
        "completed_stages": list(completed)
    })


# ─── Init & Run ──────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=9000, debug=False)
