import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from datetime import datetime

BG        = "#F0F4F8"
SIDEBAR   = "#1A2E4A"
ACCENT    = "#2E86AB"
ACCENT2   = "#27AE60"
DANGER    = "#E74C3C"
WHITE     = "#FFFFFF"
TEXT_DARK = "#1A1A2E"
TEXT_MUTED= "#6B7C93"
CARD      = "#FFFFFF"
BORDER    = "#D1DCE8"
FONT_HEAD = ("Helvetica", 22, "bold")
FONT_SUB  = ("Helvetica", 13, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_SMALL= ("Helvetica", 10)
FONT_BTN  = ("Helvetica", 11, "bold")


def get_db():
    conn = sqlite3.connect("dental_clinic.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullName VARCHAR(255),
        address LONGTEXT,
        gender VARCHAR(225),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        contactNumber BIGINT(11),
        regDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updationDate VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS dentists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dentistName VARCHAR(255),
        availableDaysTime VARCHAR(500),
        contactno BIGINT(11),
        dentistEmail VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        regDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updationDate VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255),
        fullName VARCHAR(255),
        address LONGTEXT,
        gender VARCHAR(225),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        contactNumber INT(13),
        regDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updationDate VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS dentalprocedure (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        procedureName VARCHAR(255),
        fee REAL,
        description TEXT,
        addedBy INT
    );
    CREATE TABLE IF NOT EXISTS appointment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patientId INT,
        dentistId INT,
        procedureId INT,
        appointmentDate VARCHAR(255),
        appointmentTime VARCHAR(255),
        status VARCHAR(50) DEFAULT 'Pending',
        notes TEXT,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS userslog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid INT(11),
        username VARCHAR(255),
        userip BINARY(16),
        loginTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        logout VARCHAR(255),
        status INT(11)
    );
    CREATE TABLE IF NOT EXISTS dentistslog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid INT(11),
        username VARCHAR(255),
        userip BINARY(16),
        loginTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        logout VARCHAR(255),
        status INT(11)
    );
    """)
    c.execute("SELECT * FROM staff WHERE email='admin@dental.com'")
    if not c.fetchone():
        c.execute("""INSERT INTO staff (username,fullName,address,gender,email,password,contactNumber)
                     VALUES ('admin','Admin Staff','Clinic HQ','N/A','admin@dental.com',?,'03000000000')""",
                  (hash_pw("admin123"),))
    conn.commit()
    conn.close()


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def make_btn(parent, text, cmd, color=ACCENT, fg=WHITE, width=18):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=color, fg=fg, font=FONT_BTN, relief="flat",
                  cursor="hand2", padx=10, pady=7, width=width,
                  activebackground=color, activeforeground=fg, bd=0)
    b.bind("<Enter>", lambda e: b.config(bg=_darken(color)))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b


def _darken(hex_color):
    r = max(0, int(hex_color[1:3], 16) - 20)
    g = max(0, int(hex_color[3:5], 16) - 20)
    b = max(0, int(hex_color[5:7], 16) - 20)
    return f"#{r:02x}{g:02x}{b:02x}"


def labeled_entry(parent, label, row, show=None):
    tk.Label(parent, text=label, font=FONT_BODY, bg=CARD,
             fg=TEXT_DARK, anchor="w").grid(row=row, column=0, sticky="w", pady=(8, 0))
    e = tk.Entry(parent, font=FONT_BODY, relief="flat", bd=0,
                 bg=BG, fg=TEXT_DARK, insertbackground=TEXT_DARK,
                 show=show or "")
    e.grid(row=row + 1, column=0, sticky="ew", ipady=7, pady=(2, 0))
    return e


def card_frame(parent, title="", padx=30, pady=30):
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True, padx=30, pady=30)
    if title:
        tk.Label(outer, text=title, font=FONT_HEAD, bg=BG, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    c = tk.Frame(outer, bg=CARD, relief="flat", bd=0,
                 highlightthickness=1, highlightbackground=BORDER)
    c.pack(fill="both", expand=True)
    inner = tk.Frame(c, bg=CARD)
    inner.pack(fill="both", expand=True, padx=padx, pady=pady)
    return inner, outer


def section_title(parent, text):
    tk.Label(parent, text=text, font=FONT_SUB, bg=CARD, fg=ACCENT).pack(anchor="w", pady=(0, 10))


class ScrollFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, bg=kwargs.get("bg", BG), highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=kwargs.get("bg", BG))
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)


class DentalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dental Clinic Management System")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.current_user = None
        self.user_role = None
        init_db()
        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        self.title("Dental Clinic — Login")

        root_frame = tk.Frame(self, bg=SIDEBAR)
        root_frame.pack(fill="both", expand=True)

        left = tk.Frame(root_frame, bg=SIDEBAR, width=380)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="Dental Clinic", font=("Helvetica", 28, "bold"), bg=SIDEBAR, fg=WHITE).pack(pady=(80, 10))
        tk.Label(left, text="Management System", font=("Helvetica", 14), bg=SIDEBAR, fg="#7FA7C9").pack()
        tk.Label(left, text="UET Lahore — 2026", font=FONT_SMALL, bg=SIDEBAR, fg="#4A6FA5").pack(pady=(30, 0))

        right = tk.Frame(root_frame, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        box = tk.Frame(right, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.place(relx=0.5, rely=0.5, anchor="center", width=400)

        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=40, pady=40, fill="both")

        tk.Label(inner, text="Welcome Back", font=FONT_HEAD, bg=CARD, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(inner, text="Sign in to continue", font=FONT_BODY, bg=CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(4, 20))

        tk.Label(inner, text="Role", font=FONT_BODY, bg=CARD, fg=TEXT_DARK).pack(anchor="w")
        self.login_role = ttk.Combobox(inner, values=["Patient", "Dentist", "Staff"],
                                       state="readonly", font=FONT_BODY)
        self.login_role.set("Patient")
        self.login_role.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(inner, text="Email", font=FONT_BODY, bg=CARD, fg=TEXT_DARK).pack(anchor="w")
        self.login_email = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                                    relief="flat", insertbackground=TEXT_DARK)
        self.login_email.pack(fill="x", ipady=7, pady=(2, 10))

        tk.Label(inner, text="Password", font=FONT_BODY, bg=CARD, fg=TEXT_DARK).pack(anchor="w")
        self.login_pw = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                                 relief="flat", show="•", insertbackground=TEXT_DARK)
        self.login_pw.pack(fill="x", ipady=7, pady=(2, 20))

        make_btn(inner, "Sign In", self.do_login, width=30).pack(fill="x")

        sep = tk.Frame(inner, bg=BORDER, height=1)
        sep.pack(fill="x", pady=20)

        tk.Label(inner, text="New patient?", font=FONT_BODY, bg=CARD, fg=TEXT_MUTED).pack(anchor="w")
        make_btn(inner, "Create Account", self.show_register, color=WHITE, fg=ACCENT, width=30).pack(fill="x", pady=(8, 0))

    def do_login(self):
        role = self.login_role.get().lower()
        email = self.login_email.get().strip()
        pw = self.login_pw.get()
        if not email or not pw:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        conn = get_db()
        c = conn.cursor()
        if role == "patient":
            c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hash_pw(pw)))
        elif role == "dentist":
            c.execute("SELECT * FROM dentists WHERE dentistEmail=? AND password=?", (email, hash_pw(pw)))
        else:
            c.execute("SELECT * FROM staff WHERE email=? AND password=?", (email, hash_pw(pw)))
        row = c.fetchone()
        conn.close()
        if row:
            self.current_user = dict(row)
            self.user_role = role
            self._open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def show_register(self):
        self.clear()
        self.title("Dental Clinic — Register")
        sf = ScrollFrame(self, bg=BG)
        sf.pack(fill="both", expand=True)
        parent = sf.inner

        tk.Label(parent, text="Create Patient Account", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(pady=(30, 0), padx=40, anchor="w")
        tk.Label(parent, text="Fill in your details below",
                 font=FONT_BODY, bg=BG, fg=TEXT_MUTED).pack(padx=40, anchor="w", pady=(4, 20))

        box = tk.Frame(parent, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=40, pady=(0, 30), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=30, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        fields = {}

        def row_entry(label, r, c, show=None):
            tk.Label(inner, text=label, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c, sticky="w", pady=(8, 0), padx=(0, 10))
            e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                         relief="flat", show=show or "", insertbackground=TEXT_DARK)
            e.grid(row=r + 1, column=c, sticky="ew", ipady=7, pady=(2, 0), padx=(0, 10))
            return e

        fields["fullName"] = row_entry("Full Name", 0, 0)
        fields["email"] = row_entry("Email", 0, 1)
        fields["gender"] = row_entry("Gender (M/F/Other)", 2, 0)
        fields["contact"] = row_entry("Contact Number", 2, 1)
        fields["password"] = row_entry("Password", 4, 0, show="•")
        fields["confirm"] = row_entry("Confirm Password", 4, 1, show="•")

        tk.Label(inner, text="Address", font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(14, 0))
        fields["address"] = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                                     relief="flat", insertbackground=TEXT_DARK)
        fields["address"].grid(row=7, column=0, columnspan=2, sticky="ew", ipady=7, pady=(2, 0))

        def do_reg():
            data = {k: v.get().strip() for k, v in fields.items()}
            if not all(data.values()):
                messagebox.showerror("Error", "All fields are required.")
                return
            if data["password"] != data["confirm"]:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            conn = get_db()
            c2 = conn.cursor()
            try:
                c2.execute("""INSERT INTO users (fullName,address,gender,email,password,contactNumber)
                              VALUES (?,?,?,?,?,?)""",
                           (data["fullName"], data["address"], data["gender"],
                            data["email"], hash_pw(data["password"]), data["contact"]))
                conn.commit()
                messagebox.showinfo("Success", "Account created! Please log in.")
                self.show_login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already registered.")
            finally:
                conn.close()

        btn_row = tk.Frame(inner, bg=CARD)
        btn_row.grid(row=8, column=0, columnspan=2, pady=20, sticky="w")
        make_btn(btn_row, "Register", do_reg, width=16).pack(side="left", padx=(0, 10))
        make_btn(btn_row, "Back to Login", self.show_login, color=WHITE, fg=ACCENT, width=16).pack(side="left")

    def _open_dashboard(self):
        if self.user_role == "patient":
            PatientDashboard(self)
        elif self.user_role == "dentist":
            DentistDashboard(self)
        else:
            StaffDashboard(self)

    def logout(self):
        self.current_user = None
        self.user_role = None
        self.show_login()


class BaseDashboard:
    NAV_ITEMS = []

    def __init__(self, app):
        self.app = app
        app.clear()
        app.title(f"Dental Clinic — {self.TITLE}")
        self._build_shell()
        self.show_home()

    def _build_shell(self):
        self.root = tk.Frame(self.app, bg=BG)
        self.root.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Dental Clinic", font=("Helvetica", 13, "bold"),
                 bg=SIDEBAR, fg=WHITE).pack()
        tk.Label(self.sidebar, text=self.ROLE_LABEL, font=FONT_SMALL,
                 bg=SIDEBAR, fg="#7FA7C9").pack(pady=(2, 20))

        tk.Frame(self.sidebar, bg="#2D4A6E", height=1).pack(fill="x", padx=20, pady=(0, 10))

        self.nav_buttons = {}
        for label, method in self.NAV_ITEMS:
            btn = tk.Button(self.sidebar, text=label, font=FONT_BODY,
                            bg=SIDEBAR, fg="#A8C4E0", relief="flat", cursor="hand2",
                            anchor="w", padx=20, pady=10, bd=0,
                            activebackground="#2D4A6E", activeforeground=WHITE,
                            command=lambda m=method: self._nav(m))
            btn.pack(fill="x")
            self.nav_buttons[method] = btn

        tk.Frame(self.sidebar, bg=SIDEBAR).pack(fill="y", expand=True)
        tk.Frame(self.sidebar, bg="#2D4A6E", height=1).pack(fill="x", padx=20, pady=10)

        user = self.app.current_user
        name = user.get("fullName") or user.get("dentistName") or user.get("username", "")
        tk.Label(self.sidebar, text=name, font=FONT_SMALL,
                 bg=SIDEBAR, fg=WHITE, wraplength=180).pack(padx=10)
        make_btn(self.sidebar, "Logout", self.app.logout, color="#E74C3C", width=14).pack(pady=15)

        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

    def _nav(self, method):
        for k, b in self.nav_buttons.items():
            b.config(bg=SIDEBAR if k != method else "#2D4A6E",
                     fg="#A8C4E0" if k != method else WHITE)
        getattr(self, method)()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def show_home(self):
        self._nav(self.NAV_ITEMS[0][1])

    def stat_card(self, parent, title, value, color=ACCENT):
        f = tk.Frame(parent, bg=CARD, highlightthickness=1,
                     highlightbackground=BORDER, padx=20, pady=20)
        f.pack(side="left", expand=True, fill="both", padx=8)
        tk.Label(f, text=str(value), font=("Helvetica", 28, "bold"),
                 bg=CARD, fg=color).pack(anchor="w")
        tk.Label(f, text=title, font=FONT_BODY, bg=CARD, fg=TEXT_MUTED).pack(anchor="w")

    def build_table(self, parent, columns, rows):
        tree_frame = tk.Frame(parent, bg=CARD)
        tree_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=CARD, fieldbackground=CARD,
                        foreground=TEXT_DARK, font=FONT_BODY, rowheight=32)
        style.configure("Treeview.Heading", background=ACCENT, foreground=WHITE,
                        font=("Helvetica", 11, "bold"))
        style.map("Treeview", background=[("selected", "#DBEAFE")])

        tv = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, width=max(90, 700 // len(columns)), anchor="w")

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tv.pack(fill="both", expand=True)

        for r in rows:
            tv.insert("", "end", values=r)
        return tv


class PatientDashboard(BaseDashboard):
    TITLE = "Patient Portal"
    ROLE_LABEL = "Patient"
    NAV_ITEMS = [
        ("Home", "patient_home"),
        ("Book Appointment", "patient_book"),
        ("My Appointments", "patient_appointments"),
        ("My Profile", "patient_profile"),
    ]

    def show_home(self):
        self._nav("patient_home")

    def patient_home(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text=f"Hello, {user.get('fullName', 'Patient')}",
                 font=FONT_HEAD, bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))
        tk.Label(p, text="Here's an overview of your dental care.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MUTED).pack(anchor="w", padx=30, pady=(0, 20))

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM appointment WHERE patientId=?", (user["id"],))
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM appointment WHERE patientId=? AND status='Pending'", (user["id"],))
        pending = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM dentists")
        dcount = c.fetchone()[0]
        conn.close()

        stat_row = tk.Frame(p, bg=BG)
        stat_row.pack(fill="x", padx=22, pady=(0, 20))
        self.stat_card(stat_row, "Total Appointments", total, ACCENT)
        self.stat_card(stat_row, "Pending", pending, "#E67E22")
        self.stat_card(stat_row, "Available Dentists", dcount, ACCENT2)

        tk.Label(p, text="Recent Appointments", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(0, 10))

        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT a.id, d.dentistName, dp.procedureName,
                            a.appointmentDate, a.appointmentTime, a.status
                     FROM appointment a
                     LEFT JOIN dentists d ON a.dentistId=d.id
                     LEFT JOIN dentalprocedure dp ON a.procedureId=dp.id
                     WHERE a.patientId=? ORDER BY a.id DESC LIMIT 5""", (user["id"],))
        rows = c.fetchall()
        conn.close()

        table_frame = tk.Frame(p, bg=BG, padx=30)
        table_frame.pack(fill="x", pady=(0, 30))
        cols = ("ID", "Dentist", "Procedure", "Date", "Time", "Status")
        data = [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "—", "No appointments yet")]
        self.build_table(table_frame, cols, data)

    def patient_book(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        tk.Label(p, text="Book Appointment", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))
        tk.Label(p, text="Select a dentist, procedure, and preferred time.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MUTED).pack(anchor="w", padx=30, pady=(0, 20))

        box = tk.Frame(p, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=30, pady=(0, 30), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=30, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, dentistName, availableDaysTime FROM dentists")
        dentists = c.fetchall()
        c.execute("SELECT id, procedureName, fee FROM dentalprocedure")
        procs = c.fetchall()
        conn.close()

        dmap = {f"{r['dentistName']} ({r['availableDaysTime']})": r['id'] for r in dentists}
        pmap = {f"{r['procedureName']} — Rs.{r['fee']}": r['id'] for r in procs}

        def lbl(txt, r, c2):
            tk.Label(inner, text=txt, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c2, sticky="w", pady=(10, 0), padx=(0, 10))

        lbl("Select Dentist", 0, 0)
        dvar = tk.StringVar()
        dcb = ttk.Combobox(inner, textvariable=dvar,
                           values=list(dmap.keys()) or ["No dentists added yet"],
                           state="readonly", font=FONT_BODY)
        dcb.grid(row=1, column=0, sticky="ew", ipady=4, padx=(0, 10), pady=(2, 0))

        lbl("Select Procedure", 0, 1)
        pvar = tk.StringVar()
        pcb = ttk.Combobox(inner, textvariable=pvar,
                           values=list(pmap.keys()) or ["No procedures added yet"],
                           state="readonly", font=FONT_BODY)
        pcb.grid(row=1, column=1, sticky="ew", ipady=4, pady=(2, 0))

        lbl("Preferred Date (YYYY-MM-DD)", 2, 0)
        date_e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                          relief="flat", insertbackground=TEXT_DARK)
        date_e.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_e.grid(row=3, column=0, sticky="ew", ipady=7, padx=(0, 10), pady=(2, 0))

        lbl("Preferred Time (HH:MM)", 2, 1)
        time_e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                          relief="flat", insertbackground=TEXT_DARK)
        time_e.insert(0, "10:00")
        time_e.grid(row=3, column=1, sticky="ew", ipady=7, pady=(2, 0))

        lbl("Notes (optional)", 4, 0)
        notes_e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                           relief="flat", insertbackground=TEXT_DARK)
        notes_e.grid(row=5, column=0, columnspan=2, sticky="ew", ipady=7, pady=(2, 0))

        def book():
            if not dvar.get() or not pvar.get():
                messagebox.showerror("Error", "Please select dentist and procedure.")
                return
            if dvar.get() not in dmap or pvar.get() not in pmap:
                messagebox.showerror("Error", "Invalid selection.")
                return
            conn = get_db()
            c2 = conn.cursor()
            user = self.app.current_user
            c2.execute("""INSERT INTO appointment (patientId,dentistId,procedureId,
                                                   appointmentDate,appointmentTime,notes)
                          VALUES (?,?,?,?,?,?)""",
                       (user["id"], dmap[dvar.get()], pmap[pvar.get()],
                        date_e.get(), time_e.get(), notes_e.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Appointment booked! Status: Pending")
            self.patient_appointments()

        tk.Frame(inner, bg=CARD, height=10).grid(row=6, columnspan=2)
        make_btn(inner, "Book Appointment", book, width=22).grid(row=7, column=0, sticky="w", pady=10)

    def patient_appointments(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        tk.Label(p, text="My Appointments", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        conn = get_db()
        c = conn.cursor()
        user = self.app.current_user
        c.execute("""SELECT a.id, d.dentistName, dp.procedureName,
                            a.appointmentDate, a.appointmentTime, a.status, a.notes
                     FROM appointment a
                     LEFT JOIN dentists d ON a.dentistId=d.id
                     LEFT JOIN dentalprocedure dp ON a.procedureId=dp.id
                     WHERE a.patientId=? ORDER BY a.id DESC""", (user["id"],))
        rows = c.fetchall()
        conn.close()

        table_frame = tk.Frame(p, bg=BG, padx=30)
        table_frame.pack(fill="both", expand=True, pady=(10, 0))

        cols = ("ID", "Dentist", "Procedure", "Date", "Time", "Status", "Notes")
        tv = self.build_table(table_frame, cols,
                              [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "—", "—", "None yet")])

        def cancel():
            sel = tv.selection()
            if not sel:
                messagebox.showerror("Error", "Select an appointment to cancel.")
                return
            appt_id = tv.item(sel[0])["values"][0]
            if appt_id == "—":
                return
            if messagebox.askyesno("Confirm", "Cancel this appointment?"):
                conn = get_db()
                c2 = conn.cursor()
                c2.execute("UPDATE appointment SET status='Cancelled' WHERE id=?", (int(appt_id),))
                conn.commit()
                conn.close()
                self.patient_appointments()

        make_btn(p, "Cancel Selected", cancel, color=DANGER, width=20).pack(anchor="w", padx=30, pady=15)

    def patient_profile(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text="My Profile", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        box = tk.Frame(p, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=30, pady=(10, 30), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=30, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        def lbl_e(label, val, r, c2):
            tk.Label(inner, text=label, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c2, sticky="w", pady=(10, 0), padx=(0, 10))
            e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                         relief="flat", insertbackground=TEXT_DARK)
            e.insert(0, str(val or ""))
            e.grid(row=r + 1, column=c2, sticky="ew", ipady=7, padx=(0, 10), pady=(2, 0))
            return e

        fn = lbl_e("Full Name", user.get("fullName", ""), 0, 0)
        em = lbl_e("Email", user.get("email", ""), 0, 1)
        gn = lbl_e("Gender", user.get("gender", ""), 2, 0)
        cn = lbl_e("Contact Number", user.get("contactNumber", ""), 2, 1)

        tk.Label(inner, text="Address", font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        addr = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                        relief="flat", insertbackground=TEXT_DARK)
        addr.insert(0, str(user.get("address", "")))
        addr.grid(row=5, column=0, columnspan=2, sticky="ew", ipady=7, pady=(2, 0))

        tk.Label(inner, text="New Password (leave blank to keep)",
                 font=FONT_BODY, bg=CARD, fg=TEXT_MUTED).grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(10, 0))
        pw_e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                        relief="flat", show="•", insertbackground=TEXT_DARK)
        pw_e.grid(row=7, column=0, columnspan=2, sticky="ew", ipady=7, pady=(2, 0))

        def save():
            conn = get_db()
            c = conn.cursor()
            pw_val = hash_pw(pw_e.get()) if pw_e.get() else user["password"]
            c.execute("""UPDATE users SET fullName=?,email=?,gender=?,contactNumber=?,
                                         address=?,password=?,updationDate=?
                         WHERE id=?""",
                      (fn.get(), em.get(), gn.get(), cn.get(), addr.get(),
                       pw_val, datetime.now().strftime("%Y-%m-%d %H:%M"), user["id"]))
            conn.commit()
            c.execute("SELECT * FROM users WHERE id=?", (user["id"],))
            self.app.current_user = dict(c.fetchone())
            conn.close()
            messagebox.showinfo("Saved", "Profile updated.")

        tk.Frame(inner, bg=CARD, height=10).grid(row=8, columnspan=2)
        make_btn(inner, "Save Changes", save, width=18).grid(row=9, column=0, sticky="w", pady=10)


class DentistDashboard(BaseDashboard):
    TITLE = "Dentist Portal"
    ROLE_LABEL = "Dentist"
    NAV_ITEMS = [
        ("Home", "dentist_home"),
        ("Appointments", "dentist_appts"),
        ("Procedures", "dentist_procs"),
        ("My Profile", "dentist_profile"),
    ]

    def show_home(self):
        self._nav("dentist_home")

    def dentist_home(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text=f"Dr. {user.get('dentistName', '')}",
                 font=FONT_HEAD, bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))
        tk.Label(p, text="Manage your appointments and procedures.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MUTED).pack(anchor="w", padx=30, pady=(0, 20))

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM appointment WHERE dentistId=?", (user["id"],))
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM appointment WHERE dentistId=? AND status='Pending'", (user["id"],))
        pending = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM dentalprocedure WHERE addedBy=?", (user["id"],))
        procs = c.fetchone()[0]
        conn.close()

        stat_row = tk.Frame(p, bg=BG)
        stat_row.pack(fill="x", padx=22, pady=(0, 20))
        self.stat_card(stat_row, "Total Appointments", total, ACCENT)
        self.stat_card(stat_row, "Pending", pending, "#E67E22")
        self.stat_card(stat_row, "My Procedures", procs, ACCENT2)

        tk.Label(p, text="Upcoming Appointments", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(0, 10))

        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT a.id, u.fullName, dp.procedureName,
                            a.appointmentDate, a.appointmentTime, a.status
                     FROM appointment a
                     LEFT JOIN users u ON a.patientId=u.id
                     LEFT JOIN dentalprocedure dp ON a.procedureId=dp.id
                     WHERE a.dentistId=? ORDER BY a.id DESC LIMIT 8""", (user["id"],))
        rows = c.fetchall()
        conn.close()

        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="x", pady=(0, 30))
        self.build_table(tf, ("ID", "Patient", "Procedure", "Date", "Time", "Status"),
                         [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "—", "None")])

    def dentist_appts(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text="All Appointments", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT a.id, u.fullName, dp.procedureName,
                            a.appointmentDate, a.appointmentTime, a.status, a.notes
                     FROM appointment a
                     LEFT JOIN users u ON a.patientId=u.id
                     LEFT JOIN dentalprocedure dp ON a.procedureId=dp.id
                     WHERE a.dentistId=? ORDER BY a.id DESC""", (user["id"],))
        rows = c.fetchall()
        conn.close()

        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="both", expand=True, pady=(10, 0))
        cols = ("ID", "Patient", "Procedure", "Date", "Time", "Status", "Notes")
        tv = self.build_table(tf, cols,
                              [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "—", "—", "None")])

        def update_status(status):
            sel = tv.selection()
            if not sel:
                messagebox.showerror("Error", "Select an appointment.")
                return
            appt_id = tv.item(sel[0])["values"][0]
            if appt_id == "—":
                return
            conn = get_db()
            c2 = conn.cursor()
            c2.execute("UPDATE appointment SET status=? WHERE id=?", (status, int(appt_id)))
            conn.commit()
            conn.close()
            self.dentist_appts()

        btn_row = tk.Frame(p, bg=BG, padx=30)
        btn_row.pack(anchor="w", pady=15)
        make_btn(btn_row, "Approve", lambda: update_status("Approved"), ACCENT2, width=14).pack(side="left", padx=(0, 8))
        make_btn(btn_row, "Reject", lambda: update_status("Rejected"), DANGER, width=14).pack(side="left")

    def dentist_procs(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text="Dental Procedures", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        box = tk.Frame(p, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=30, pady=(10, 20), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=25, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        inner.columnconfigure(2, weight=1)

        section_title(inner, "Add New Procedure")

        def fld(label, r, c2):
            tk.Label(inner, text=label, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c2, sticky="w", pady=(8, 0), padx=(0, 10))
            e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                         relief="flat", insertbackground=TEXT_DARK)
            e.grid(row=r + 1, column=c2, sticky="ew", ipady=7, padx=(0, 10), pady=(2, 0))
            return e

        name_e = fld("Procedure Name", 1, 0)
        fee_e = fld("Fee (Rs.)", 1, 1)
        desc_e = fld("Description", 1, 2)

        def add_proc():
            if not name_e.get() or not fee_e.get():
                messagebox.showerror("Error", "Name and fee are required.")
                return
            try:
                fee = float(fee_e.get())
            except:
                messagebox.showerror("Error", "Fee must be a number.")
                return
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO dentalprocedure (procedureName,fee,description,addedBy) VALUES (?,?,?,?)",
                      (name_e.get(), fee, desc_e.get(), user["id"]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Added", "Procedure added.")
            self.dentist_procs()

        make_btn(inner, "Add Procedure", add_proc, width=18).grid(row=3, column=0, sticky="w", pady=12)

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, procedureName, fee, description FROM dentalprocedure WHERE addedBy=?",
                  (user["id"],))
        rows = c.fetchall()
        conn.close()

        tk.Label(p, text="My Procedures", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(0, 10))
        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="x", pady=(0, 30))
        self.build_table(tf, ("ID", "Name", "Fee (Rs.)", "Description"),
                         [tuple(r) for r in rows] if rows else [("—", "—", "—", "None yet")])

    def dentist_profile(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text="My Profile", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        box = tk.Frame(p, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=30, pady=(10, 30), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=30, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        def fld(label, val, r, c2):
            tk.Label(inner, text=label, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c2, sticky="w", pady=(10, 0), padx=(0, 10))
            e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                         relief="flat", insertbackground=TEXT_DARK)
            e.insert(0, str(val or ""))
            e.grid(row=r + 1, column=c2, sticky="ew", ipady=7, padx=(0, 10), pady=(2, 0))
            return e

        nm = fld("Full Name", user.get("dentistName", ""), 0, 0)
        em = fld("Email", user.get("dentistEmail", ""), 0, 1)
        cn = fld("Contact", user.get("contactno", ""), 2, 0)
        av = fld("Available Days & Time", user.get("availableDaysTime", ""), 2, 1)
        pw_e = fld("New Password (blank to keep)", "", 4, 0)

        def save():
            conn = get_db()
            c = conn.cursor()
            pw_val = hash_pw(pw_e.get()) if pw_e.get() else user["password"]
            c.execute("""UPDATE dentists SET dentistName=?,dentistEmail=?,contactno=?,
                                             availableDaysTime=?,password=?,updationDate=?
                         WHERE id=?""",
                      (nm.get(), em.get(), cn.get(), av.get(), pw_val,
                       datetime.now().strftime("%Y-%m-%d %H:%M"), user["id"]))
            conn.commit()
            c.execute("SELECT * FROM dentists WHERE id=?", (user["id"],))
            self.app.current_user = dict(c.fetchone())
            conn.close()
            messagebox.showinfo("Saved", "Profile updated.")

        tk.Frame(inner, bg=CARD, height=10).grid(row=6, columnspan=2)
        make_btn(inner, "Save Changes", save, width=18).grid(row=7, column=0, sticky="w", pady=10)


class StaffDashboard(BaseDashboard):
    TITLE = "Staff Admin"
    ROLE_LABEL = "Dental Staff"
    NAV_ITEMS = [
        ("Dashboard", "staff_home"),
        ("Patients", "staff_patients"),
        ("Dentists", "staff_dentists"),
        ("Appointments", "staff_appts"),
        ("Procedures", "staff_procs"),
        ("User Logs", "staff_logs"),
        ("My Profile", "staff_profile"),
    ]

    def show_home(self):
        self._nav("staff_home")

    def staff_home(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text=f"Staff Panel — {user.get('fullName', '')}",
                 font=FONT_HEAD, bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))
        tk.Label(p, text="Full administrative access to the Dental Clinic system.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MUTED).pack(anchor="w", padx=30, pady=(0, 20))

        conn = get_db()
        c = conn.cursor()
        counts = {}
        for tbl, key in [("users", "Patients"), ("dentists", "Dentists"),
                         ("appointment", "Appointments"), ("dentalprocedure", "Procedures")]:
            c.execute(f"SELECT COUNT(*) FROM {tbl}")
            counts[key] = c.fetchone()[0]
        conn.close()

        stat_row = tk.Frame(p, bg=BG)
        stat_row.pack(fill="x", padx=22, pady=(0, 20))
        colors = [ACCENT, ACCENT2, "#E67E22", "#9B59B6"]
        for (k, v), col in zip(counts.items(), colors):
            self.stat_card(stat_row, k, v, col)

    def staff_patients(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        tk.Label(p, text="Manage Patients", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        box = tk.Frame(p, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=30, pady=(10, 20), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=25, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        inner.columnconfigure(2, weight=1)

        section_title(inner, "Add New Patient")

        def fld(label, r, c2, show=None):
            tk.Label(inner, text=label, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c2, sticky="w", pady=(8, 0), padx=(0, 10))
            e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK, relief="flat",
                         show=show or "", insertbackground=TEXT_DARK)
            e.grid(row=r + 1, column=c2, sticky="ew", ipady=7, padx=(0, 10), pady=(2, 0))
            return e

        fn = fld("Full Name", 1, 0)
        em = fld("Email", 1, 1)
        gn = fld("Gender", 1, 2)
        cn = fld("Contact", 3, 0)
        pw = fld("Password", 3, 1, show="•")

        tk.Label(inner, text="Address", font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
            row=5, column=0, columnspan=3, sticky="w", pady=(10, 0))
        addr_e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                          relief="flat", insertbackground=TEXT_DARK)
        addr_e.grid(row=6, column=0, columnspan=3, sticky="ew", ipady=7, pady=(2, 0))

        def add_patient():
            if not fn.get() or not em.get() or not pw.get():
                messagebox.showerror("Error", "Name, email, and password required.")
                return
            conn = get_db()
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO users (fullName,address,gender,email,password,contactNumber)
                             VALUES (?,?,?,?,?,?)""",
                          (fn.get(), addr_e.get(), gn.get(), em.get(), hash_pw(pw.get()), cn.get()))
                conn.commit()
                messagebox.showinfo("Added", "Patient added.")
                self.staff_patients()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already exists.")
            finally:
                conn.close()

        make_btn(inner, "Add Patient", add_patient, width=18).grid(row=7, column=0, sticky="w", pady=12)

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id,fullName,email,gender,contactNumber,regDate FROM users ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        tk.Label(p, text="All Patients", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(0, 8))
        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="x", pady=(0, 30))
        cols = ("ID", "Full Name", "Email", "Gender", "Contact", "Registered")
        tv = self.build_table(tf, cols,
                              [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "—", "None")])

        def delete_patient():
            sel = tv.selection()
            if not sel:
                messagebox.showerror("Error", "Select a patient.")
                return
            pid = tv.item(sel[0])["values"][0]
            if pid == "—":
                return
            if messagebox.askyesno("Confirm", "Delete this patient?"):
                conn = get_db()
                c2 = conn.cursor()
                c2.execute("DELETE FROM users WHERE id=?", (int(pid),))
                conn.commit()
                conn.close()
                self.staff_patients()

        make_btn(p, "Delete Patient", delete_patient, DANGER, width=18).pack(anchor="w", padx=30, pady=(0, 20))

    def staff_dentists(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        tk.Label(p, text="Manage Dentists", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        box = tk.Frame(p, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=30, pady=(10, 20), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=25, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        inner.columnconfigure(2, weight=1)

        section_title(inner, "Add New Dentist")

        def fld(label, r, c2, show=None):
            tk.Label(inner, text=label, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c2, sticky="w", pady=(8, 0), padx=(0, 10))
            e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK, relief="flat",
                         show=show or "", insertbackground=TEXT_DARK)
            e.grid(row=r + 1, column=c2, sticky="ew", ipady=7, padx=(0, 10), pady=(2, 0))
            return e

        nm = fld("Full Name", 1, 0)
        em = fld("Email", 1, 1)
        cn = fld("Contact", 1, 2)
        av = fld("Available Days & Time", 3, 0)
        pw = fld("Password", 3, 1, show="•")

        def add_dentist():
            if not nm.get() or not em.get() or not pw.get():
                messagebox.showerror("Error", "Name, email, and password required.")
                return
            conn = get_db()
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO dentists (dentistName,availableDaysTime,contactno,
                                                   dentistEmail,password)
                             VALUES (?,?,?,?,?)""",
                          (nm.get(), av.get(), cn.get(), em.get(), hash_pw(pw.get())))
                conn.commit()
                messagebox.showinfo("Added", "Dentist added.")
                self.staff_dentists()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already exists.")
            finally:
                conn.close()

        make_btn(inner, "Add Dentist", add_dentist, width=18).grid(row=4, column=0, sticky="w", pady=12)

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id,dentistName,dentistEmail,contactno,availableDaysTime,regDate FROM dentists ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        tk.Label(p, text="All Dentists", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(0, 8))
        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="x", pady=(0, 30))
        cols = ("ID", "Name", "Email", "Contact", "Available", "Registered")
        tv = self.build_table(tf, cols,
                              [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "—", "None")])

        def delete_dentist():
            sel = tv.selection()
            if not sel:
                messagebox.showerror("Error", "Select a dentist.")
                return
            did = tv.item(sel[0])["values"][0]
            if did == "—":
                return
            if messagebox.askyesno("Confirm", "Delete this dentist?"):
                conn = get_db()
                c2 = conn.cursor()
                c2.execute("DELETE FROM dentists WHERE id=?", (int(did),))
                conn.commit()
                conn.close()
                self.staff_dentists()

        make_btn(p, "Delete Dentist", delete_dentist, DANGER, width=18).pack(anchor="w", padx=30, pady=(0, 20))

    def staff_appts(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        tk.Label(p, text="All Appointments", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT a.id, u.fullName, d.dentistName, dp.procedureName,
                            a.appointmentDate, a.appointmentTime, a.status
                     FROM appointment a
                     LEFT JOIN users u ON a.patientId=u.id
                     LEFT JOIN dentists d ON a.dentistId=d.id
                     LEFT JOIN dentalprocedure dp ON a.procedureId=dp.id
                     ORDER BY a.id DESC""")
        rows = c.fetchall()
        conn.close()

        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="both", expand=True, pady=(10, 0))
        cols = ("ID", "Patient", "Dentist", "Procedure", "Date", "Time", "Status")
        tv = self.build_table(tf, cols,
                              [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "—", "—", "None")])

        def set_status(status):
            sel = tv.selection()
            if not sel:
                messagebox.showerror("Error", "Select an appointment.")
                return
            appt_id = tv.item(sel[0])["values"][0]
            if appt_id == "—":
                return
            conn = get_db()
            c2 = conn.cursor()
            c2.execute("UPDATE appointment SET status=? WHERE id=?", (status, int(appt_id)))
            conn.commit()
            conn.close()
            self.staff_appts()

        def delete_appt():
            sel = tv.selection()
            if not sel:
                messagebox.showerror("Error", "Select an appointment.")
                return
            appt_id = tv.item(sel[0])["values"][0]
            if appt_id == "—":
                return
            if messagebox.askyesno("Confirm", "Delete appointment?"):
                conn = get_db()
                c2 = conn.cursor()
                c2.execute("DELETE FROM appointment WHERE id=?", (int(appt_id),))
                conn.commit()
                conn.close()
                self.staff_appts()

        btn_row = tk.Frame(p, bg=BG, padx=30)
        btn_row.pack(anchor="w", pady=15)
        make_btn(btn_row, "Approve", lambda: set_status("Approved"), ACCENT2, width=14).pack(side="left", padx=(0, 8))
        make_btn(btn_row, "Reject", lambda: set_status("Rejected"), DANGER, width=14).pack(side="left", padx=(0, 8))
        make_btn(btn_row, "Delete", delete_appt, "#6B7C93", width=14).pack(side="left")

    def staff_procs(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        tk.Label(p, text="All Procedures", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT dp.id, dp.procedureName, dp.fee, dp.description, d.dentistName
                     FROM dentalprocedure dp
                     LEFT JOIN dentists d ON dp.addedBy=d.id
                     ORDER BY dp.id DESC""")
        rows = c.fetchall()
        conn.close()

        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="x", pady=(10, 30))
        cols = ("ID", "Procedure", "Fee (Rs.)", "Description", "Dentist")
        self.build_table(tf, cols,
                         [tuple(r) for r in rows] if rows else [("—", "—", "—", "—", "None")])

    def staff_logs(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        tk.Label(p, text="User Login Logs", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        conn = get_db()
        c = conn.cursor()

        tk.Label(p, text="Patient Logins", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(10, 6))
        c.execute("SELECT id,uid,username,loginTime,status FROM userslog ORDER BY id DESC")
        rows = c.fetchall()
        tf = tk.Frame(p, bg=BG, padx=30)
        tf.pack(fill="x", pady=(0, 20))
        self.build_table(tf, ("ID", "UID", "Username", "Login Time", "Status"),
                         [tuple(r) for r in rows] if rows else [("—", "—", "No logs yet", "—", "—")])

        tk.Label(p, text="Dentist Logins", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(10, 6))
        c.execute("SELECT id,uid,username,loginTime,status FROM dentistslog ORDER BY id DESC")
        rows2 = c.fetchall()
        conn.close()
        tf2 = tk.Frame(p, bg=BG, padx=30)
        tf2.pack(fill="x", pady=(0, 30))
        self.build_table(tf2, ("ID", "UID", "Username", "Login Time", "Status"),
                         [tuple(r) for r in rows2] if rows2 else [("—", "—", "No logs yet", "—", "—")])

    def staff_profile(self):
        self.clear_content()
        sf = ScrollFrame(self.content, bg=BG)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        user = self.app.current_user
        tk.Label(p, text="My Profile", font=FONT_HEAD,
                 bg=BG, fg=TEXT_DARK).pack(anchor="w", padx=30, pady=(30, 4))

        box = tk.Frame(p, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        box.pack(padx=30, pady=(10, 30), fill="x")
        inner = tk.Frame(box, bg=CARD)
        inner.pack(padx=30, pady=30, fill="x")
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        def fld(label, val, r, c2):
            tk.Label(inner, text=label, font=FONT_BODY, bg=CARD, fg=TEXT_DARK).grid(
                row=r, column=c2, sticky="w", pady=(10, 0), padx=(0, 10))
            e = tk.Entry(inner, font=FONT_BODY, bg=BG, fg=TEXT_DARK,
                         relief="flat", insertbackground=TEXT_DARK)
            e.insert(0, str(val or ""))
            e.grid(row=r + 1, column=c2, sticky="ew", ipady=7, padx=(0, 10), pady=(2, 0))
            return e

        nm = fld("Full Name", user.get("fullName", ""), 0, 0)
        em = fld("Email", user.get("email", ""), 0, 1)
        un = fld("Username", user.get("username", ""), 2, 0)
        cn = fld("Contact", user.get("contactNumber", ""), 2, 1)
        pw = fld("New Password", "", 4, 0)

        def save():
            conn = get_db()
            c = conn.cursor()
            pw_val = hash_pw(pw.get()) if pw.get() else user["password"]
            c.execute("""UPDATE staff SET fullName=?,email=?,username=?,contactNumber=?,
                                          password=?,updationDate=? WHERE id=?""",
                      (nm.get(), em.get(), un.get(), cn.get(), pw_val,
                       datetime.now().strftime("%Y-%m-%d %H:%M"), user["id"]))
            conn.commit()
            c.execute("SELECT * FROM staff WHERE id=?", (user["id"],))
            self.app.current_user = dict(c.fetchone())
            conn.close()
            messagebox.showinfo("Saved", "Profile updated.")

        tk.Frame(inner, bg=CARD, height=10).grid(row=6, columnspan=2)
        make_btn(inner, "Save Changes", save, width=18).grid(row=7, column=0, sticky="w", pady=10)


if __name__ == "__main__":
    app = DentalApp()
    app.mainloop()