import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# student class
class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code = int(code.strip())
        self.name = name.strip()
        self.c1 = int(c1)
        self.c2 = int(c2)
        self.c3 = int(c3)
        self.exam = int(exam)

    def coursework_total(self):
        return self.c1 + self.c2 + self.c3

    def overall_total(self):
        return self.coursework_total() + self.exam

    def percentage(self):
        return round((self.overall_total() / 160) * 100, 2)

    def grade(self):
        p = self.percentage()
        if p >= 70: return "A"
        elif p >= 60: return "B"
        elif p >= 50: return "C"
        elif p >= 40: return "D"
        return "F"

# load students
def load_students(filename):
    students = []
    with open(filename, "r") as f:
        count = int(f.readline().strip())
        for _ in range(count):
            data = [p.strip() for p in f.readline().strip().split(",")]
            students.append(Student(*data))
    return students

students = load_students("Exercise 3/studentMarks.txt")

# GUI setup 
root = tk.Tk()
root.title("Student Manager System")
root.geometry("900x520")

# central background color 
BG_COLOR = "#b7c5b6"
root.configure(bg=BG_COLOR)

title_label = tk.Label(root,
                       text="Student Manager System",
                       font=("Arial", 20, "bold"),
                       bg=BG_COLOR,
                       fg="#333E31")
title_label.pack(pady=10)

# basic callbacks so the buttons created below have valid function references
def search_record():
    # filter students by student number or name 
    query = search_entry.get().strip().lower()
    tree.delete(*tree.get_children())
    if not query:
        return
    for s in students:
        if query.isdigit() and int(query) == s.code:
            tree.insert("", "end", values=(s.code, s.name, s.coursework_total(), s.exam, f"{s.percentage()}%", s.grade()))
        elif query in s.name.lower():
            tree.insert("", "end", values=(s.code, s.name, s.coursework_total(), s.exam, f"{s.percentage()}%", s.grade()))

def view_all():
    # show all student 
    show_all()

top_frame = tk.Frame(root, bg=BG_COLOR)
top_frame.pack(pady=15)

# placing everything inside an inner frame so it stays centered
center_frame = tk.Frame(top_frame, bg=BG_COLOR)
center_frame.pack()

search_label = tk.Label(center_frame, text="Search:", font=("Arial", 12), bg=BG_COLOR, fg="#2b2b2b")
search_label.grid(row=0, column=0, padx=5)

search_entry = tk.Entry(center_frame, font=("Arial", 12), width=25)
search_entry.grid(row=0, column=1, padx=5)

search_button = tk.Button(center_frame, text="Search", font=("Arial", 11), command=search_record)
search_button.grid(row=0, column=2, padx=5)

view_button = tk.Button(center_frame, text="View All Records", font=("Arial", 11), command=view_all)
view_button.grid(row=0, column=3, padx=10)

# table frame
table_frame = tk.Frame(root, bg="#b7c5b6")
table_frame.pack(fill="both", expand=True, padx=20)

# treeview styling
style = ttk.Style()

style.configure("Treeview",
                background="#f7f7ef",
                foreground="black",
                rowheight=30,
                fieldbackground="#f7f7ef")

style.configure("Treeview.Heading",
                background="#9da999",
                foreground="black",
                font=("Arial", 11, "bold"))

# stop windows default blue selection
SELECT_BG = "#c8d6c6"

style.map("Treeview",
          background=[("selected", SELECT_BG)],
          foreground=[("selected", "black")]
)

# Treeview
columns = ("code", "name", "coursework", "exam", "percent", "grade")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

tree.heading("code", text="Student No")
tree.heading("name", text="Name")
tree.heading("coursework", text="Coursework (/60)")
tree.heading("exam", text="Exam (/100)")
tree.heading("percent", text="Overall %")
tree.heading("grade", text="Grade")

tree.column("code", width=100, anchor="center")
tree.column("name", width=220)
tree.column("coursework", width=140, anchor="center")
tree.column("exam", width=120, anchor="center")
tree.column("percent", width=110, anchor="center")
tree.column("grade", width=80, anchor="center")

tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# functions
def show_all():
    tree.delete(*tree.get_children())
    for s in students:
        tree.insert("", "end", values=(
            s.code, s.name, s.coursework_total(), s.exam,
            f"{s.percentage()}%", s.grade()
        ))


def show_highest():
    best = max(students, key=lambda s: s.percentage())
    tree.delete(*tree.get_children())
    tree.insert("", "end", values=(
        best.code, best.name, best.coursework_total(), best.exam,
        f"{best.percentage()}%", best.grade()
    ))


def show_lowest():
    worst = min(students, key=lambda s: s.percentage())
    tree.delete(*tree.get_children())
    tree.insert("", "end", values=(
        worst.code, worst.name, worst.coursework_total(), worst.exam,
        f"{worst.percentage()}%", worst.grade()
    ))


def show_lowest():
    worst = min(students, key=lambda s: s.percentage())
    tree.delete(*tree.get_children())
    tree.insert("", "end", values=(
        worst.code, worst.name, worst.coursework_total(), worst.exam,
        f"{worst.percentage()}%", worst.grade()
    ))


# bottom buttons 
bottom_frame = tk.Frame(root, bg=BG_COLOR)
bottom_frame.pack(pady=15)

high_button = tk.Button(bottom_frame, text="Highest Score", font=("Arial", 11), command=show_highest)
high_button.grid(row=0, column=0, padx=10)

low_button = tk.Button(bottom_frame, text="Lowest Score", font=("Arial", 11), command=show_lowest)
low_button.grid(row=0, column=1, padx=10)


# load all on startup
show_all()

root.mainloop()