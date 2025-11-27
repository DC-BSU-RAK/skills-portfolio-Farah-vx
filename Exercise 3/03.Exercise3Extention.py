import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Menu, Menubutton, RAISED

# define the student class to store student data and methods for calculations
class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code = int(str(code).strip())
        self.name = name.strip()
        self.c1 = int(c1)
        self.c2 = int(c2)
        self.c3 = int(c3)
        self.exam = int(exam)

    def coursework_total(self):
        return self.c1 + self.c2 + self.c3  # total coursework score

    def overall_total(self):
        return self.coursework_total() + self.exam  # total score including exam

    def percentage(self):
        # calculate overall percentage based on total of 160
        return round((self.overall_total() / 160) * 100, 2)

    def grade(self):
        # determine grade based on percentage
        p = self.percentage()
        if p >= 70: return "A"
        if p >= 60: return "B"
        if p >= 50: return "C"
        if p >= 40: return "D"
        return "F"

# define the filename for saving/loading student data
file_data = "Exercise 3/studentMarks.txt"

# function to load student data from a file
def load_students(filename):
    students = []
    try:
        with open(filename, "r") as f:
            first = f.readline().strip()
            if first.isdigit():
                count = int(first)
                for _ in range(count):
                    parts = f.readline().strip().split(",")
                    if len(parts) == 6:
                        students.append(Student(*parts))
            else:
                f.seek(0)
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 6:
                        students.append(Student(*parts))
    except FileNotFoundError:
         # create file if not found, starting with zero students
        with open(filename, "w") as f:
            f.write("0\n")
    return students

# function to save student data back to the file
def save_students(filename, students_list):
    with open(filename, "w") as f:
        f.write(f"{len(students_list)}\n")
        for s in students_list:
            f.write(f"{s.code},{s.name},{s.c1},{s.c2},{s.c3},{s.exam}\n")

students = load_students(file_data)

# main window
root = tk.Tk()
root.title("Student Manager System")
root.geometry("900x520")
BG_COLOR = "#b7c5b6"
root.configure(bg=BG_COLOR)

# add hover functionality
def add_hover(widget):
    widget.bind("<Enter>", lambda e: widget.config(bg="#d9d9d9"))
    widget.bind("<Leave>", lambda e: widget.config(bg="SystemButtonFace"))

# title
tk.Label(root, text="STUDENT  MANAGEMENT", font=("Bahnschrift SemiBold",28,"bold"),
         bg=BG_COLOR, fg="#333E31").pack(pady=10)

# search bar
top_frame = tk.Frame(root, bg=BG_COLOR)
top_frame.pack(pady=8)
center_frame = tk.Frame(top_frame, bg=BG_COLOR)
center_frame.pack()

tk.Label(center_frame, text="Search:", bg=BG_COLOR, font=("Arial",12)).grid(row=0,column=0)
search_entry = tk.Entry(center_frame, font=("Arial",10), width=25)
search_entry.grid(row=0,column=1, padx=5)

# search button
btn_search = tk.Button(center_frame, text="Search", command=lambda: search_record())
btn_view = tk.Button(center_frame, text="View All Records", command=lambda: show_all())

btn_search.grid(row=0,column=2,padx=5)
btn_view.grid(row=0,column=3,padx=5)

#hover effects for buttons
add_hover(btn_search)
add_hover(btn_view)

#dropdown menu to sort students by name
def asc():
    global students
    students.sort(key=lambda s: s.name.lower())
    show_all()

def dsc():
    global students
    students.sort(key=lambda s: s.name.lower(), reverse=True)
    show_all()

sort = Menubutton(center_frame, text='Sort Students By', bg="#FFFFFF", fg="#000000",
                  font=('Arial', 10), relief=RAISED)
sort_menu = Menu(sort, tearoff=0)
sort.config(menu=sort_menu)

sort_menu.add_command(label='Ascending', command=asc)
sort_menu.add_command(label='Descending', command=dsc)

sort.grid(row=0,column=4,padx=5)

# layout split for main content and buttons
outer_margin = tk.Frame(root, bg=BG_COLOR)
outer_margin.pack(fill="both", expand=True, padx=25)  #  margin here

container = tk.Frame(outer_margin, bg=BG_COLOR)
container.pack(fill="both", expand=True)

content_area = tk.Frame(container, bg=BG_COLOR)
content_area.pack(side="top", fill="both", expand=True)

# bottom button bar 
bottom_menu = tk.Frame(container, bg=BG_COLOR)
bottom_menu.pack(side="bottom", fill="x", pady=10)

left_margin = tk.Frame(bottom_menu, bg=BG_COLOR, width=60)
left_margin.pack(side="left")

buttons_area = tk.Frame(bottom_menu, bg=BG_COLOR)
buttons_area.pack(side="left", expand=True)

right_margin = tk.Frame(bottom_menu, bg=BG_COLOR, width=60)
right_margin.pack(side="right")

# create the action buttons
btn_add = tk.Button(buttons_area, text="Add Student", font=("Arial",12), width=15,
                    command=lambda: open_panel("add"))
btn_update = tk.Button(buttons_area, text="Update Student", font=("Arial",12), width=15,
                       command=lambda: open_panel("update"))
btn_delete = tk.Button(buttons_area, text="Delete Student", font=("Arial",12), width=15,
                       command=lambda: open_panel("delete"))
btn_high = tk.Button(buttons_area, text="Highest", font=("Arial",12), width=12,
                     command=lambda: show_highest())
btn_low = tk.Button(buttons_area, text="Lowest", font=("Arial",12), width=12,
                    command=lambda: show_lowest())

# pack the buttons with some space in between
btn_add.grid(row=0, column=0, padx=8)
btn_update.grid(row=0, column=1, padx=8)
btn_delete.grid(row=0, column=2, padx=8)
btn_high.grid(row=0, column=3, padx=8)
btn_low.grid(row=0, column=4, padx=8)

# add hover effect to all buttons
for b in [btn_add, btn_update, btn_delete, btn_high, btn_low]:
    add_hover(b)

# table setup to display student data
tree_frame = tk.Frame(content_area, bg=BG_COLOR)
tree_frame.pack(side="left", fill="both", expand=True)

style = ttk.Style()
style.configure("Treeview", rowheight=25)  # increase row height

columns = ("code","name","cw","exam","percent","grade")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

# styling for selected row
style.map("Treeview", background=[("selected", "#4a6984")])

# stop windows default blue selection
SELECT_BG = "#c8d6c6"

style.map("Treeview",
          background=[("selected", SELECT_BG)],
          foreground=[("selected", "black")]
)

# configure odd/even row colors
tree.tag_configure("oddrow", background="#ffffff")
tree.tag_configure("evenrow", background="#e6e6e6")  # light grey

# set up columns and headers
for col,text,w in [
    ("code","Student ID",100),
    ("name","Name",200),
    ("cw","Total Coursework",120),
    ("exam","Exam Mark",100),
    ("percent","Total Percentage",100),
    ("grade","Grade",80)
]:
    tree.heading(col,text=text)
    tree.column(col,width=w,anchor="center")

tree.pack(side="left", fill="both", expand=True)
sb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb.set)
sb.pack(side="right", fill="y")

# form panel for add/update/delete
form_frame = tk.Frame(content_area, width=320, bg="#e6e6e6", bd=2, relief="ridge")
form_frame.pack(side="left", fill="y")
form_frame.pack_propagate(False)

form_title = tk.Label(form_frame, text="", bg="#e6e6e6", font=("Arial",14,"bold"))
form_title.pack(pady=8)

form_body = tk.Frame(form_frame, bg="#e6e6e6")
form_body.pack(fill="both", expand=True, padx=6)

form_footer = tk.Frame(form_frame, bg="#e6e6e6")
form_footer.pack(pady=6)

def clear_form():
    form_title.config(text="")
    for w in form_body.winfo_children(): w.destroy()
    for w in form_footer.winfo_children(): w.destroy()

# display all students in the table
def show_all():
    tree.delete(*tree.get_children())
    row_index = 0
    for s in students:
        tag = "evenrow" if row_index % 2 == 0 else "oddrow"
        tree.insert("", "end",
                    values=(s.code, s.name, s.coursework_total(), s.exam,
                            f"{s.percentage()}%", s.grade()),
                    tags=(tag,))
        row_index += 1

# function to show student with highest percentage
def show_highest():
    if not students: return
    s = max(students, key=lambda x: x.percentage())
    tree.delete(*tree.get_children())
    tree.insert("", "end", values=(s.code,s.name,s.coursework_total(),s.exam,f"{s.percentage()}%",s.grade()))

# function to show student with lowest percentage
def show_lowest():
    if not students: return
    s = min(students, key=lambda x: x.percentage())
    tree.delete(*tree.get_children())
    tree.insert("", "end", values=(s.code,s.name,s.coursework_total(),s.exam,f"{s.percentage()}%",s.grade()))

# search function to find student by id or name
def search_record():
    q = search_entry.get().strip().lower()
    tree.delete(*tree.get_children())
    for s in students:
        if q.isdigit() and int(q)==s.code:
            tree.insert("", "end", values=(s.code,s.name,s.coursework_total(),s.exam,f"{s.percentage()}%",s.grade()))
        elif q in s.name.lower():
            tree.insert("", "end", values=(s.code,s.name,s.coursework_total(),s.exam,f"{s.percentage()}%",s.grade()))

# function to open add/update/delete panels
def open_panel(kind):
    clear_form()

    if kind == "add":
        form_title.config(text="Add Student")
        labels = ["ID","Name","Course1","Course2","Course3","Exam"]
        entries = {}

        for lab in labels:
            row = tk.Frame(form_body, bg="#e6e6e6"); row.pack(fill="x", pady=4)
            tk.Label(row, text=lab+":", bg="#e6e6e6", width=10, anchor="w").pack(side="left")
            e = tk.Entry(row)
            e.pack(side="left", fill="x", expand=True)
            entries[lab] = e

        def do_add():
            try:
                code = int(entries["ID"].get())
                name = entries["Name"].get()
                c1 = int(entries["Course1"].get())
                c2 = int(entries["Course2"].get())
                c3 = int(entries["Course3"].get())
                exam = int(entries["Exam"].get())
            except:
                messagebox.showerror("Error","Invalid input")
                return

            students.append(Student(code,name,c1,c2,c3,exam))
            save_students(file_data,students)
            show_all()
            clear_form()
            messagebox.showinfo("OK","Student added")

        add_button = tk.Button(form_footer, text="Add", command=do_add)
        add_button.pack(side="left", padx=5)
        add_hover(add_button)

    if kind == "delete":
        form_title.config(text="Delete Student")

        row = tk.Frame(form_body, bg="#e6e6e6"); row.pack(fill="x", pady=6)
        tk.Label(row, text="ID or Name:", bg="#e6e6e6").pack(side="left")
        box = tk.Entry(row); box.pack(side="left", fill="x", expand=True)

        def do_delete():
            q = box.get().strip()
            found = None
            if q.isdigit():
                found = next((s for s in students if s.code==int(q)),None)
            else:
                found = next((s for s in students if s.name.lower()==q.lower()),None)
            if not found:
                messagebox.showerror("Err","Not found")
                return
            students.remove(found)
            save_students(file_data,students)
            show_all()
            clear_form()
            messagebox.showinfo("OK","Deleted")

        delete_button = tk.Button(form_footer, text="Delete", command=do_delete)
        delete_button.pack(side="left", padx=5)
        add_hover(delete_button)

    if kind == "update":
        form_title.config(text="Update Student")

        row = tk.Frame(form_body, bg="#e6e6e6"); row.pack(fill="x", pady=6)
        tk.Label(row, text="Student ID:", bg="#e6e6e6").pack(side="left")
        id_box = tk.Entry(row); id_box.pack(side="left", fill="x", expand=True)

        row2 = tk.Frame(form_body, bg="#e6e6e6"); row2.pack(fill="x", pady=6)
        tk.Label(row2, text="Field:", bg="#e6e6e6").pack(side="left")
        field_var = tk.StringVar(value="Course1")
        field = ttk.Combobox(row2, textvariable=field_var,
                             values=["Course1","Course2","Course3"], state="readonly")
        field.pack(side="left")

        row3 = tk.Frame(form_body, bg="#e6e6e6"); row3.pack(fill="x", pady=6)
        tk.Label(row3, text="New value:", bg="#e6e6e6").pack(side="left")
        new_box = tk.Entry(row3); new_box.pack(side="left", fill="x", expand=True)

        def do_update():
            sid = id_box.get().strip()
            if not sid.isdigit():
                messagebox.showerror("Error","ID must be number")
                return
            st = next((s for s in students if s.code==int(sid)),None)
            if not st:
                messagebox.showerror("Err","Not found")
                return
            try:
                v = int(new_box.get())
            except:
                messagebox.showerror("Err","Value must be num")
                return
            f = field_var.get()
            if f=="Course1": st.c1=v
            if f=="Course2": st.c2=v
            if f=="Course3": st.c3=v
            save_students(file_data,students)
            show_all()
            clear_form()
            messagebox.showinfo("OK","Updated")

        update_button = tk.Button(form_footer, text="Update", command=do_update)
        update_button.pack(side="left", padx=5)
        add_hover(update_button)

# load all on startup
show_all()
root.mainloop()




