import tkinter as tk
from PIL import Image, ImageTk
import pygame
import math
from tkinter import font as tkfont
import random

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("900x600")
        
        # Initialize music
        pygame.mixer.init()
        pygame.mixer.music.load("Exercise 1/bgmusic.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
        # Load background images
        self.bg_image_main = Image.open("Exercise 1/images/bg1.png")
        self.bg_image_main = self.bg_image_main.resize((1300, 740), Image.Resampling.LANCZOS)
        self.bg_photo_main = ImageTk.PhotoImage(self.bg_image_main)

        self.bg_image_instructions = Image.open("Exercise 1/images/bg2.png")
        self.bg_image_instructions = self.bg_image_instructions.resize((1300, 740), Image.Resampling.LANCZOS)
        self.bg_photo_instructions = ImageTk.PhotoImage(self.bg_image_instructions)

        self.bg_image_levels = Image.open("Exercise 1/images/bg3.png")
        self.bg_image_levels = self.bg_image_levels.resize((1300, 740), Image.Resampling.LANCZOS)
        self.bg_photo_levels = ImageTk.PhotoImage(self.bg_image_levels)
        
        # Main background label
        self.bg_label = tk.Label(self.root, image=self.bg_photo_main)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Animated heading
        self.heading = "Math Quiz"
        self.letter_labels = []
        self.start_x_position = 500
        self.start_y_position = 160
        self.heading_font = tkfont.Font(family="Black Goth", size=85)
        self.current_x = self.start_x_position

        for character in self.heading:
            character_label = tk.Label(self.root, text=character, font=("Black Goth", 85), fg="#D4F7F9", bg="#140A2D")
            character_label.place(x=self.current_x, y=self.start_y_position)
            self.letter_labels.append(character_label)
            self.current_x += self.heading_font.measure(character) + 2

        self.wave_angle = 0
        self.animate_wave()

        # Start button
        self.button1 = tk.Button(
            self.root,
            text="START",
            font=("LuxemourDemo", 26),
            fg="white",
            bg="#4E02DB",
            activebackground="#8B44F5",
            width=12,
            height=1,
            command=self.show_instructions
        )
        self.button1.place(relx=0.53, rely=0.7, anchor="center")
        self.button1.bind("<Enter>", self.on_enter)
        self.button1.bind("<Leave>", self.on_leave)

        # Instruction frame
        self.instruction_frame = tk.Frame(self.root)
        self.instruction_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.instruction_frame.lower()

        self.instruction_bg_label = tk.Label(self.instruction_frame, image=self.bg_photo_instructions)
        self.instruction_bg_label.place(x=1, y=0, relwidth=1, relheight=1)

        instructions = ("""
            Instructions:
            1. Choose Difficulty Level:
               - Easy: Single-digit numbers (1-9)
               - Moderate: Double-digit numbers (10-99)
               - Advanced: Four-digit numbers (1000-9999)
            2. Answer the questions:
               - You will get 10 problems.
               - Type your answer and press Submit.
            3. Scoring:
               - Correct on first try = 10 points
               - Correct on second try = 5 points
               - Wrong twice = show correct answer
            4. After completion:
               - View your total score and performance.
               - Play again or Exit.
        """)
        self.instructions_label = tk.Label(
            self.instruction_frame, text=instructions, font=("Emotion Engine", 19), fg="white", bg="#140A2D", justify="left"
        )
        self.instructions_label.place(x=80, y=80)
        
        self.continue_button = tk.Button(
            self.instruction_frame,
            text="Continue",
            font=("LuxemourDemo", 24),
            fg="white",
            bg="#4E02DB",
            command=self.show_level_selection
        )
        self.continue_button.place(relx=0.6, rely=0.9, anchor="center")
        self.continue_button.bind("<Enter>", lambda e: self.continue_button.config(bg="#8B44F5"))
        self.continue_button.bind("<Leave>", lambda e: self.continue_button.config(bg="#4E02DB"))

        self.level_frame = tk.Frame(self.root)
        self.level_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.level_frame.lower()

        self.level_bg_label = tk.Label(self.level_frame, image=self.bg_photo_levels)
        self.level_bg_label.place(x=1, y=0, relwidth=1, relheight=1)

        self.level_label = tk.Label(
            self.level_frame,
            text="Select Level",
            font=("Black Goth", 50),
            fg="white",
            bg="#140A2D"
        )
        self.level_label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.easy_button = tk.Button(
            self.level_frame,
            text="Easy",
            font=("LuxemourDemo", 26),
            fg="white",
            bg="#4E02DB",
            width=12,
            command=lambda: self.set_level("Easy")
        )
        self.medium_button = tk.Button(
            self.level_frame,
            text="Medium",
            font=("LuxemourDemo", 26),
            fg="white",
            bg="#4E02DB",
            width=12,
            command=lambda: self.set_level("Medium")
        )
        self.hard_button = tk.Button(
            self.level_frame,
            text="Hard",
            font=("LuxemourDemo", 28),
            fg="white",
            bg="#4E02DB",
            width=12,
            command=lambda: self.set_level("Hard")
        )

        self.easy_button.place(relx=0.3, rely=0.67, anchor="center")
        self.medium_button.place(relx=0.5, rely=0.67, anchor="center")
        self.hard_button.place(relx=0.7, rely=0.67, anchor="center")
    
    def show_instructions(self):
        self.bg_label.place_forget()
        self.button1.place_forget()
        for label in self.letter_labels:
            label.place_forget()
        self.instruction_frame.lift()

    def show_level_selection(self):
        self.instruction_frame.lower()
        self.level_frame.lift()

    def set_level(self, level):
        self.current_level = level
        self.setup_quiz_page()
        if level == "Easy":
            self.start_easy_quiz()
        elif level == "Medium":
            self.start_medium_quiz()
        elif level == "Hard":
            self.start_hard_quiz()

    def on_enter(self, event):
        self.button1.config(bg="#8B44F5", fg="#FFFFFF")
    def on_leave(self, event):
        self.button1.config(bg="#4E02DB", fg="#E0CFFF")
    def animate_wave(self):
        for index, character_label in enumerate(self.letter_labels):
            new_y = self.start_y_position + int(10 * math.sin((self.wave_angle + index) * 0.5))
            character_label.place(y=new_y)
        self.wave_angle += 1
        self.root.after(60, self.animate_wave)

# Quiz  frames

    def setup_quiz_page(self):
        self.quiz_frame = tk.Frame(self.root)
        self.quiz_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.quiz_frame.lower()

        self.bg_quiz_img = Image.open("Exercise 1/images/bg4.png")
        self.bg_quiz_img = self.bg_quiz_img.resize((1300, 740), Image.Resampling.LANCZOS)
        self.bg_photo_quiz = ImageTk.PhotoImage(self.bg_quiz_img)
        self.bg_quiz_label = tk.Label(self.quiz_frame, image=self.bg_photo_quiz)
        self.bg_quiz_label.place(x=1, y=0, relwidth=1, relheight=1)

        # positioning the questions
        self.quiz_question_label = tk.Label(self.quiz_frame, text="", font=("Emotion Engine", 40), fg="black", bg="#beddf3")
        self.quiz_question_label.place(relx=0.5, rely=0.4, anchor="center")  

        self.quiz_answer_entry = tk.Entry(self.quiz_frame, font=("Emotion Engine", 30), fg="black", bg="#beddf3", justify='center')
        self.quiz_answer_entry.place(relx=0.5, rely=0.5, anchor="center")  

        self.quiz_submit_btn = tk.Button(self.quiz_frame, text="Submit", font=("LuxemourDemo", 20), fg="black", bg="#4E02DB", command=self.check_quiz_answer)
        self.quiz_submit_btn.place(relx=0.5, rely=0.6, anchor="center")  

        self.quiz_feedback = tk.Label(self.quiz_frame, text="", font=("Emotion Engine", 20), fg="black", bg="#beddf3")
        self.quiz_feedback.place(relx=0.5, rely=0.7, anchor="center")  

        # Score 
        self.score_label = tk.Label(self.quiz_frame, text="Score: 0", font=("Black Goth", 20), fg="black", bg="#beddf3")
        self.score_label.place(relx=0.22, rely=0.3)

        # Initialize quiz variables
        self.quiz_score = 0
        self.quiz_questions_asked = 0
        self.quiz_total_questions = 10
        self.current_quiz_answer = None
        self.current_quiz_op = None
        self.attempts = 0

    def start_easy_quiz(self):
        self.level_frame.lower()
        self.quiz_frame.lift()
        self.reset_quiz()
        self.next_quiz_question()

    def start_medium_quiz(self):
        self.level_frame.lower()
        self.quiz_frame.lift()
        self.reset_quiz()
        self.next_quiz_question()

    def start_hard_quiz(self):
        self.level_frame.lower()
        self.quiz_frame.lift()
        self.reset_quiz()
        self.next_quiz_question()

    def reset_quiz(self):
        self.quiz_score = 0
        self.quiz_questions_asked = 0
        self.attempts = 0
        self.score_label.config(text=f"Score: {self.quiz_score}")

    def next_quiz_question(self):
        if self.quiz_questions_asked >= self.quiz_total_questions:
            self.show_quiz_results()
            return
        self.quiz_questions_asked += 1
        if self.current_level == "Easy":
            self.generate_easy_quiz_question()
        elif self.current_level == "Medium":
            self.generate_medium_quiz_question()
        elif self.current_level == "Hard":
            self.generate_hard_quiz_question()

    def generate_easy_quiz_question(self):
        def randomInt():
            return random.randint(1, 9)
        def decideOperation():
            return random.choice(["+", "-"])
        num1 = randomInt()
        num2 = randomInt()
        op = decideOperation()
        if op == "-" and num2 > num1:
            num1, num2 = num2, num1
        self.current_quiz_answer = eval(f"{num1} {op} {num2}")
        self.current_quiz_op = op
        self.quiz_question_label.config(text=f"{num1} {op} {num2} =")
        self.quiz_answer_entry.delete(0, tk.END)
        self.quiz_feedback.config(text="")
        self.attempts = 0

    def generate_medium_quiz_question(self):
        def randomInt():
            return random.randint(10, 99)
        def decideOperation():
            return random.choice(["+", "-"])
        num1 = randomInt()
        num2 = randomInt()
        op = decideOperation()
        if op == "-" and num2 > num1:
            num1, num2 = num2, num1
        self.current_quiz_answer = eval(f"{num1} {op} {num2}")
        self.current_quiz_op = op
        self.quiz_question_label.config(text=f"{num1} {op} {num2} =")
        self.quiz_answer_entry.delete(0, tk.END)
        self.quiz_feedback.config(text="")
        self.attempts = 0

    def generate_hard_quiz_question(self):
        def randomInt():
            return random.randint(1000, 9999)
        def decideOperation():
            return random.choice(["+", "-"])
        num1 = randomInt()
        num2 = randomInt()
        op = decideOperation()
        if op == "-" and num2 > num1:
            num1, num2 = num2, num1
        self.current_quiz_answer = eval(f"{num1} {op} {num2}")
        self.current_quiz_op = op
        self.quiz_question_label.config(text=f"{num1} {op} {num2} =")
        self.quiz_answer_entry.delete(0, tk.END)
        self.quiz_feedback.config(text="")
        self.attempts = 0

    def check_quiz_answer(self):
        user_ans = self.quiz_answer_entry.get()
        try:
            user_ans_int = int(user_ans)
        except:
            self.quiz_feedback.config(text="Enter a valid number.")
            return

        if user_ans_int == self.current_quiz_answer:
            # correct answer
            if self.attempts == 0:
                self.quiz_score += 10
            elif self.attempts == 1:
                self.quiz_score += 5
            self.score_label.config(text=f"Score: {self.quiz_score}")
            self.quiz_feedback.config(text=f"Correct! Total Score: {self.quiz_score}", fg="green")
            self.root.after(1000, self.next_quiz_question)
            self.attempts = 0
        else:
            # wrong answer
            self.attempts += 1
            attempts_left = 2 - self.attempts
            if self.attempts >= 2:
                # show correct answer and move on to next question
                self.quiz_feedback.config(text=f"Wrong! Correct answer was {self.current_quiz_answer}\nTotal Score: {self.quiz_score}")
                self.root.after(1500, self.next_quiz_question)
                self.attempts = 0
            else:
                #  displaying attempts left
                self.quiz_feedback.config(text=f"Incorrect! Attempts left: {attempts_left}")
                self.quiz_answer_entry.delete(0, tk.END)

# results page
    def show_quiz_results(self):
        
        result_bg_image = Image.open("Exercise 1/images/bg5.png") 
        result_bg_image = result_bg_image.resize((1300, 740), Image.Resampling.LANCZOS)
        result_bg_photo = ImageTk.PhotoImage(result_bg_image)
        
        # label with the background image
        self.result_bg_label = tk.Label(self.quiz_frame, image=result_bg_photo)
        self.result_bg_label.image = result_bg_photo  
        self.result_bg_label.place(x=1, y=0, relwidth=1, relheight=1)
        
        #  appropriate result and rank
        result_text = f"Your score: {self.quiz_score} / 100"
        rank = "A+  Outstanding" if self.quiz_score >= 90 else \
            "A  excellenE" if self.quiz_score >= 80 else \
            "B Above Average " if self.quiz_score >= 70 else \
            "C  Average" if self.quiz_score >= 60 else "Fail"

        result_label = tk.Label(self.quiz_frame, text=result_text + "\nRank: " + rank, font=("Black Goth", 40), fg="white", bg="#140A2D")
        result_label.place(relx=0.5, rely=0.4, anchor="center")

        restart_btn = tk.Button(self.quiz_frame, text="Play Again", font=("LuxemourDemo", 26), command=self.restart_game)
        restart_btn.place(relx=0.4, rely=0.7, anchor="center")
        exit_btn = tk.Button(self.quiz_frame, text="Exit", font=("LuxemourDemo", 26), command=self.root.quit)
        exit_btn.place(relx=0.6, rely=0.7, anchor="center")
    
        
    def restart_game(self):
        self.level_frame.lift()
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()    



if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()