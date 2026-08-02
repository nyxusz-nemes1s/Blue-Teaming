#Modules
import customtkinter as ctk
import os
import re
import string
import secrets
from tkinter import messagebox
from PIL import Image

#Settings/display type shi 
application = ctk.CTk()
application.title("nyxusz-nemes1s password strength analysis")
application.geometry("800x600") #CHANGE THIS TO ANY RES U WANT
ctk.set_appearance_mode("system") 
ctk.set_default_color_theme("green") 

#loads all the alya images but w failure handling
def load_mood_image(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        img = Image.open(path)
    except FileNotFoundError:
        messagebox.showerror(
            "Missing image",
            f"Couldn't find {filename} in this folder.\n\n"
            "See the README for what images this app needs."
        )
        application.destroy()
        raise SystemExit
    return ctk.CTkImage(light_image=img, dark_image=img, size=(400, 300))

#ALYA images to change according to the password strenght level
angry_photo = load_mood_image("angry.jpg")

#happy image when password is really strong
happy_photo = load_mood_image("happy.jpeg")

#moderate image when password is good but could be better
moderate = load_mood_image("moderate.jpeg")

#neutral image when starting
neutral = load_mood_image("neutral.jpeg")

#password file
stored_passwords = []
password_file = os.path.join(os.path.dirname(__file__), "passwords.txt")
try:
    with open(password_file, "r") as file:
        for line in file:
            stored_passwords.append(line.strip())
except FileNotFoundError:
    messagebox.showerror(
        "You are missing the passwords.txt",
        "Couldn't find passwords.txt in this folder.\n\n"
        "This app needs a breach-password wordlist to check against.\n"
        "See the README for where to download one and where to place it.\n"
        "Have a good day!"
    )
    application.destroy()
    raise SystemExit
passwords = set(stored_passwords)

#To check if passwords.txt is being imported
#print(len(passwords))

#variables! CHANGE THIS TO ANYTHING YA WANT
NIP = "Nothing inputted"
current_suggestion = ""
button_settings = {
    "side": "left",
    "pady": 15,
    "padx": 5
}
lowtiergod = """Whats a high-tier human to a Low tier GOD"""
length = 16 #this is the length of the passowrd being generated in suggest_password function! 


#**********************FUHtions***********************

#the function where it suggests passwords if the user passwords is not good enough 
def suggest_password():  # CHANGFE THIS LENGHT TO ANYTHING YA WANT CHUD
    #note that passwords over 16 is considered the norm for a good password
    #IF you want a good password suggestions could be over 20-30 characters!

    guaranteed = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()"),
        secrets.choice("!@#$%^&*()"),
    ]


    all_characters = (
        string.ascii_letters
        + (string.digits * 2)
        + ("!@#$%^&*()" * 2)
    )
    remaining = [secrets.choice(all_characters) for _ in range(length - len(guaranteed))]

    new_password = guaranteed + remaining
    secrets.SystemRandom().shuffle(new_password)
    return ''.join(new_password)

#this FUHtions handles passwords.txt && strenght, and other labels 
def check_password():
    global current_suggestion
    password = user_password.get()
    strength = 0
    breached = False

    #hanldles password.txt thing
    if len(password) == 0:
        vulnerable_password.configure(text="Enter a password to check it against known breaches")
    if password in passwords and len(password) != 0:
        vulnerable_password.configure(text="This password has been seen in the passwords.txt list. Please pick a different one.")
        breached = True
    elif password not in passwords and len(password) != 0:
        vulnerable_password.configure(text="Not found in the passwords.txt list")


    #handles strenght of lenght
    if len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1
    elif len(password) == 0:
        strength = 0
        
    #handles strenght of cahracters
    if len(re.findall(r"[A-Z]", password)) >= 3:
        strength += 1
    if len(re.findall(r"[a-z]", password)) >= 3:
        strength += 1
    if len(re.findall(r"[0-9]", password)) >= 3:
        strength += 1
    if len(re.findall(r"[!@#$%^&*(),.?\":{}|<>]", password)) >= 3:
        strength += 1

    progress_percentage(strength / 6)
    alya_state(strength, breached)

    #uses the result_label to tell the user if password good
    if strength == 0:
        result_label.configure(text="No password inputted. Alya would be disappointed", text_color="yellow")

    elif strength > 0 and strength <= 2:
        result_label.configure(text="Weak Password. Sad", text_color="red")
        current_suggestion = suggest_password()
        suggestion_label.configure(text=f"Suggestion: {current_suggestion}")
    elif strength <= 4:
        result_label.configure(text="Moderate Password. Still average", text_color="orange")
        current_suggestion = ""
        suggestion_label.configure(text="Try adding symbols or numbers to improve strength")
    elif strength <= 5:
        result_label.configure(text="Strong Password. Kinda good", text_color="green")
        current_suggestion = ""
        suggestion_label.configure(text="Good enough")
    else:
        result_label.configure(text="Excellent Password. NICE", text_color="blue")
        current_suggestion = ""
        suggestion_label.configure(text="Really good!")

    #shhhh ignore this dont look at it
    if password == "ltg":
        ltg()


#This code is very important and useful do NOT delete ts
def ltg(): 
    result_label.configure(text=lowtiergod, text_color="yellow")

def reset_suggestion_label(): #this func is for another func below
    suggestion_label.configure(text="", text_color="lightblue")

#copies the suggestion made to the users clipboard then after 3 seconds resets the label with reset_suggestion_label
def copy_suggestion():
    if current_suggestion == "":
        suggestion_label.configure(text="Nothing to copy yet!", text_color="yellow")
        application.after(3000, reset_suggestion_label)
        return
    application.clipboard_clear()
    application.clipboard_append(current_suggestion)
    suggestion_label.configure(text="Copied Successfuly!", text_color="yellow")
    application.after(3000, reset_suggestion_label)

def clear_password(): #clears password box and other labels
    user_password.delete(0, "end")
    result_label.configure(text="Cleared. Waiting for input")
    vulnerable_password.configure(text="Cleared. Waiting for input")
    suggestion_label.configure(text="Cleared. Waiting for input")
    alya_state(0)

#alyas state depending on password strenght and if passowrd found in passwords.txt
def alya_state(strength, breached=False): 
    #0=no input, 1-2=angry, 3-4=moderate, 5-6=happy.
    if breached:
        image_label.configure(image=angry_photo)
    elif strength == 0:
        image_label.configure(image=neutral)
    elif strength <= 2:
        image_label.configure(image=angry_photo)
    elif strength <= 4:
        image_label.configure(image=moderate)
    else:   # strength 5 or 6
        image_label.configure(image=happy_photo)

def toggle_password(): #IS AUTOMATICALLY HIDDEN FROM THE START
    if user_password.cget('show') == "*":
        user_password.configure(show="")
        toggle_button.configure(text="Hide")
    else:
        user_password.configure(show="*")
        toggle_button.configure(text="Show")

def progress_percentage(value): #PERCentage
    progress_bar.set(value)

    perc=int(value*100)
    status_bar.configure(text=f"{perc}%")



#**********************UI elements******************************

#where the user puts their password in
user_password = ctk.CTkEntry(application, width=50, height=50, placeholder_text="Enter your password here bro", show="*", font=("Arial", 14, "bold"))
user_password.pack(pady=10, padx=15, fill="x")

#frame
buttons = ctk.CTkFrame(
    application,
    fg_color="transparent",
    border_width=2,
    corner_radius=12
    )
buttons.pack(pady=15, padx=5)

#the toggle button for hiding and showing the password (ITS AUTOAMTICALLY ON)
toggle_button = ctk.CTkButton(
    buttons,
    text="Show",
    command=toggle_password,
    fg_color="crimson",
    hover_color="#FF3355",   
    text_color="white")
toggle_button.pack(**button_settings)

#button for checking if the password is good
check_button = ctk.CTkButton(
    buttons,
    text="Check Strength",
    command=check_password,
    fg_color="crimson",
    hover_color="#FF3355",   
    text_color="white")
check_button.pack(**button_settings)

#the copy button duh
copy_button = ctk.CTkButton(
    buttons,
    text="Copy Suggestion",
    command=copy_suggestion,
    fg_color="crimson",
    hover_color="#FF3355",   
    text_color="white")
copy_button.pack(**button_settings)

#the button for clearing the user_password
clear_button = ctk.CTkButton(
    buttons,
    text="Clear",
    command=clear_password,
    fg_color="crimson",
    hover_color="#FF3355",   
    text_color="white")
clear_button.pack(**button_settings)

#progress bar
progress_bar = ctk.CTkProgressBar(
    master=application,
    width=750,
    height=28)
progress_bar.set(0)
progress_bar.pack(pady=4)

#status bar for the progress bar (bars)
status_bar = ctk.CTkLabel(application,
                          text="0%",
                          font=("Arial", 21, "bold"),
                          border_width=2,
                          corner_radius=5)
status_bar.pack(pady=1)

#tells the user if poassword good
result_label = ctk.CTkLabel(application,
                            text=NIP,
                            font=("Arial", 14, "bold"),
                            border_width=2,
                            corner_radius=5)
result_label.pack(pady=2)

#tells the user if password is found in passwords.txt
vulnerable_password = ctk.CTkLabel(application,
                                   text=NIP,
                                   text_color="yellow",
                                   font=("Arial", 14, "bold"),
                                   border_width=2,
                                   corner_radius=5)
vulnerable_password.pack(pady=2)

#tells user suggestions to password
suggestion_label = ctk.CTkLabel(application,
                                text=NIP,
                                text_color="lightblue",
                                font=("Arial", 14, "bold"),
                                border_width=2,
                                corner_radius=5)
suggestion_label.pack(pady=2)

#loads the alya image at the botom
image_label = ctk.CTkLabel(application, image=neutral, text="")
image_label.pack(side="bottom", pady=0)

application.mainloop()
#sudo apt install opsec && sudo apt remove feelings
#hehe im so auraful
