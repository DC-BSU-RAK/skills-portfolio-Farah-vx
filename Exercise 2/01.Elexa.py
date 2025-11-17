import tkinter as tk
from PIL import Image, ImageTk
import random
import threading
import win32com.client
import pygame

# setting up the main window
root = tk.Tk()
root.title("Joke Program")
root.geometry("900x600")

# initialize the mixer for playing sounds and music
pygame.mixer.init()

# load and start playing background music in a loop
pygame.mixer.music.load("Exercise 2/bg1.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # loop music indefinitely

# load the laugh sound effect once for reuse
laugh_sound_path = "Exercise 2/laughSound.mp3"
laugh_sound = pygame.mixer.Sound(laugh_sound_path)

# load background images for different screens with safe resizing
original_bg1 = Image.open("Exercise 2/images/bg1.png")
original_bg2 = Image.open("Exercise 2/images/bg2.png")
original_bg3 = Image.open("Exercise 2/images/bg3.png")

def resize_image_stretch(image, width, height):
    # resize images to fit the screen dimensions
    return image.resize((width, height), Image.LANCZOS)

# resize backgrounds
bg1 = resize_image_stretch(original_bg1, 1300, 650)
bg2 = resize_image_stretch(original_bg2, 1300, 650)
bg3 = resize_image_stretch(original_bg3, 1300, 650)

# convert images to tkinter-compatible format
start_bg = ImageTk.PhotoImage(bg1)
joke_bg = ImageTk.PhotoImage(bg2)
end_bg = ImageTk.PhotoImage(bg3)

# create frames for different screens
start_frame = tk.Frame(root, width=1300, height=650)
joke_frame = tk.Frame(root, width=1300, height=650)
end_frame = tk.Frame(root, width=1300, height=650)

# place all frames in the same location; we'll lift the active one
for f in (start_frame, joke_frame, end_frame):
    f.place(x=0, y=0)

# function to raise a specific frame to the front
def show_frame(frame):
    frame.tkraise()

# start screen setup
tk.Label(start_frame, image=start_bg).place(x=0, y=0)

start_button = tk.Button(
    start_frame,
    text="""Alexa 
Tell Me A Joke""",
    font=("Super Dessert", 37),
    bg='#fef7a2',
    fg='black',
    padx=0,
    pady=0,
    borderwidth=1,
    highlightthickness=0,
    height=2,
    width=12,
    command=lambda: [show_frame(joke_frame), update_joke_display()]  # move to joke screen and show first joke
)
start_button.place(relx=0.55, rely=0.43, anchor='center')

label= tk.Label(
    start_frame,
    text="WHOAA!",
    font=("Smilen", 28),
    bg="white",
    fg="black",
    
)
label.place(x=1090, y=405)

# setup for text-to-speech using windows speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")
# make the voice sound more lively and animated
speaker.Rate = 4
speaker.Volume = 100

def speak(text):
    # function to speak text asynchronously
    def run():
        try:
            # add pitch boost for a more cartoonish voice
            xml_text = f'<pitch middle="+10">{text}</pitch>'
            speaker.Speak(xml_text, 1)
        except:
            pass
    threading.Thread(target=run, daemon=True).start()

# list of jokes with their punchlines
jokes = [
    ("Why did the chicken cross the road?","To get to the other side."),
    ("What happens if you boil a clown?","You get a laughing stock."),
    ("Why did the car get a flat tire?","Because there was a fork in the road!"),
    ("How did the hipster burn his mouth?","He ate his pizza before it was cool."),
    ("What did the janitor say when he jumped out of the closet?","SUPPLIES!!!!"),
    ("Have you heard about the band 1023MB?","It's probably because they haven't got a gig yet…"),
    ("Why does the golfer wear two pants?","Because he's afraid he might get a 'Hole-in-one' "),
    ("Why should you wear glasses to maths class?","Because it helps with division."),
    ("Why does it take pirates so long to learn the alphabet?","Because they could spend years at C."),
    ("Why did the woman go on the date with the mushroom?","Because he was a fun-ghi."),
    ("Why do bananas never get lonely?","Because they hang out in bunches."),
    ("What did the buffalo say when his kid went to college?","Bison."),
    ("Why shouldn't you tell secrets in a cornfield?","Too many ears."),
    ("What do you call someone who doesn't like carbs?","Lack-Toast Intolerant."),
    ("Why did the can crusher quit his job?","Because it was soda pressing."),
    ("Why did the birthday boy wrap himself in paper?","He wanted to live in the present."),
    ("What does a house wear?","A dress."),
    ("Why couldn't the toilet paper cross the road?","Because it got stuck in a crack."),
    ("Why didn't the bike want to go anywhere?","Because it was two-tired!"),
    ("Want to hear a pizza joke?","Nahhh, it's too cheesy!"),
    ("Why are chemists great at solving problems?","Because they have all of the solutions!"),
    ("Why is it impossible to starve in the desert?","Because of all the sand which is there!"),
    ("What did the cheese say when it looked in the mirror?","Halloumi!"),
    ("Why did the developer go broke?","Because he used up all his cache."),
    ("Did you know that ants are the only animals that don't get sick?","It's true! It's because they have little antibodies."),
    ("Why did the donut go to the dentist?","To get a filling."),
    ("What do you call a bear with no teeth?","A gummy bear!"),
    ("What does a vegan zombie like to eat?","Graaains."),
    ("What do you call a dinosaur with only one eye?","A Do-you-think-he-saw-us!"),
    ("Why should you never fall in love with a tennis player?","Because to them... love means NOTHING!"),
    ("What did the full glass say to the empty glass?","You look drunk."),
    ("What's a potato's favorite form of transportation?","The gravy train"),
    ("What did one ocean say to the other?","Nothing, they just waved."),
    ("What did the right eye say to the left eye?","Honestly, between you and me something smells."),
    ("What do you call a dog that's been run over by a steamroller?","Spot!"),
    ("What's the difference between a hippo and a zippo?","One's pretty heavy and the other's a little lighter"),
    ("Why don't scientists trust Atoms?","They make up everything."),
]

# shuffle jokes for variety
random.shuffle(jokes)
joke_index = 0  # keep track of current joke

# function to update the joke display
def update_joke_display():
    """show new joke in top bubble & clear punchline, also read aloud."""
    global current_joke, current_punchline, joke_index
    print("Updating joke at index:", joke_index)  # debug info
    current_joke, current_punchline = jokes[joke_index]
    joke_label.config(text=current_joke)
    punchline_label.config(text="")  # clear punchline bubble
    # speak the joke aloud
    print("Speaking:", current_joke)  # debug info
    speak(current_joke)

# function to reveal and speak the punchline
def show_punchline():
    global current_punchline
    punchline_label.config(text=current_punchline)
    speak(current_punchline)
    # play laugh sound in a separate thread
    threading.Thread(target=lambda: laugh_sound.play(), daemon=True).start()

# function to select and show a new joke
def next_joke():
    global joke_index
    joke_index = random.randint(0, len(jokes) - 1)
    print("Next joke index:", joke_index)  # debug info
    update_joke_display()

# function to go to the end screen
def quit_to_end():
    show_frame(end_frame)

# setup joke screen UI
tk.Label(joke_frame, image=joke_bg).place(x=0, y=0)

# top bubble with joke text
joke_label = tk.Label(
    joke_frame,
    text=jokes[0][0],
    font=("Ruji's Handwriting Font", 22, "bold"),
    bg="#e3ffea",
    fg="black",
    wraplength=450,
    justify="center"
)
joke_label.place(x=340, y=100)

# lower bubble with punchline
punchline_label = tk.Label(
    joke_frame,
    text="",
    font=("Ruji's Handwriting Font", 22, "bold"),
    bg="#e3ffea",
    fg="black",
    wraplength=450,
    justify="center"
)
punchline_label.place(x=580, y=385)

# buttons for interaction
btn_punchline = tk.Button(joke_frame, text="Show Punchline",
                          font=("Smilen", 24, "bold"),
                          bg="black", fg="white",
                          command=show_punchline)
btn_next = tk.Button(joke_frame, text="Next Joke",
                     font=("Smilen", 24, "bold"),
                     bg="black", fg="white",
                     command=next_joke)
btn_quit = tk.Button(joke_frame, text="QUIT",
                     font=("Smilen", 34, "bold"),
                     bg="#a31b1b", fg="white",
                     command=quit_to_end)

# position the buttons
btn_punchline.place(x=400, y=250)
btn_next.place(x=680, y=250)
btn_quit.place(x=1100, y=90)

# setup end screen UI
tk.Label(end_frame, image=end_bg).place(x=0, y=0)

# final message label
tk.Label(end_frame,
         text="Hope You Enjoyed It!",
         font=("Super Dessert", 40),
         bg="#75d6d0",
         fg="black"
        ).place(x=350, y=220)

# add exit button to close the app
exit_button = tk.Button(
    end_frame,
    text="Exit",
    font=("Smilen", 39, "bold"),
    bg="red",
    fg="white",
    command=root.quit  # close the window
)
exit_button.place(x=700, y=350)

# start with the start screen
show_frame(start_frame)
# run the main event loop
root.mainloop()

