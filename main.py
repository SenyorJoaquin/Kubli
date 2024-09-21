from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb

# Initialize the main application window
root = Tk()
root.title("Steganography Application")
root.geometry("900x700+150+180")
root.resizable(False, False)
root.configure(bg="#AF261C")

# =========================================== MENU FUNCTIONS ==========================================

# Function to show the main window
def show_main():
    menu_frame.pack_forget()  # Hides the Menu Frame
    main_frame.pack(fill="both", expand=True)

# Function to exit
def exit_app():
    root.destroy()
# =========================================== MENU FUNCTIONS ===========================================


# =========================================== MAIN FUNCTIONS ===========================================
def remove_hide_data_button():
    hide_data_button.place_forget()  # This hides the Hide Data button

def show_hide_data_button():
    hide_data_button.place(x=375, y=550)

# Function to Show Image
def showImage():
    global filename
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select Image File",
        filetypes=(("PNG file", "*.png"),
                   ("JPG File", "*.jpg"),
                   ("All files", "*.*"))
    )

    if filename:
        try:
            img = Image.open(filename)
            img = img.resize((250, 250), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open image.\n{e}")

# Function to Hide Data in Image
def Hide():
    global secret
    message = text1.get(1.0, END).strip()
    if not filename:
        messagebox.showwarning("Warning", "Please select an image first.")
        return
    if not message:
        messagebox.showwarning("Warning", "Please enter a message to hide.")
        return
    try:
        secret = lsb.hide(filename, message)
        messagebox.showinfo("Success", "Message hidden successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hide message.\n{e}")


# Function to Show Data in Image
def Show():
    if not filename:
        messagebox.showwarning("Warning", "Please select an image first.")
        return
    try:
        clear_message = lsb.reveal(filename)
        if clear_message:
            text1.delete(1.0, END)
            text1.insert(END, clear_message)
        else:
            messagebox.showinfo("Info", "No hidden message found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to reveal message.\n{e}")

# Function to Save Data in Image
def save():
    if secret:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")],
                                                 title="Save Image As")
        if save_path:
            try:
                secret.save(save_path)
                messagebox.showinfo("Success", f"Image saved successfully at {save_path}")

                # Clear the text box after saving
                text1.delete(1.0, END)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image.\n{e}")
    else:
        messagebox.showwarning("Warning", "No image to save. Please hide a message first.")
# =========================================== MAIN FUNCTIONS ===========================================


# =========================================== BUTTON FUNCTIONS =========================================

# Hover effect functions to change button image
def on_enter(e, hover_image):
    e.widget.config(image=hover_image)

def on_leave(e, normal_image):
    e.widget.config(image=normal_image)
# =========================================== BUTTON FUNCTIONS =========================================


# =========================================== Main Menu Frame ==========================================
menu_frame = Frame(root, bg="#AF261C")
menu_frame.pack(fill="both", expand=True)

# Menu Logo
logo_menu = PhotoImage(file="menu elements/kubli2.png")
caption_menu = PhotoImage(file="menu elements/caption2.png")
info_menu = PhotoImage(file="menu elements/info1.png")
Label(menu_frame, image=logo_menu, bg="#AF261C").pack(pady=35)
Label(menu_frame, image=caption_menu, bg="#AF261C").place(x=330, y=180)
Label(menu_frame, image=info_menu, bg="#AF261C").pack(pady=35)

# Frame to hold buttons
button_frame = Frame(menu_frame, bg="#AF261C")
button_frame.pack(pady=50)

# Load images for "Start" button (normal and hover)
start_normal = PhotoImage(file="menu elements/start_button_1.png")
start_hover = PhotoImage(file="menu elements/start_button_on_hover.png")

# Load images for "Exit" button (normal and hover)
exit_normal = PhotoImage(file="menu elements/exit_button_1.png")
exit_hover = PhotoImage(file="menu elements/exit_button_on_hover.png")

# Frame for buttons
button_frame = Frame(root, bg="#AF261C")
button_frame.place(x=215, y=500)

# Start Button (image-based)
start_button = Button(button_frame, image=start_normal, borderwidth=0, bg="#AF261C",
                      activebackground="#AF261C", command=show_main)
start_button.pack(side=LEFT, padx=10)

# Bind hover events for Start button
start_button.bind("<Enter>", lambda e: on_enter(e, start_hover))
start_button.bind("<Leave>", lambda e: on_leave(e, start_normal))

# Exit Button (image-based)
exit_button = Button(button_frame, image=exit_normal, borderwidth=0, bg="#AF261C",
                     activebackground="#AF261C", command=exit_app)
exit_button.pack(side=LEFT, padx=10)

# Bind hover events for Exit button
exit_button.bind("<Enter>", lambda e: on_enter(e, exit_hover))
exit_button.bind("<Leave>", lambda e: on_leave(e, exit_normal))
# =========================================== Main Menu Frame ==========================================


# ======================================= Main Application Frame =======================================
main_frame = Frame(root, bg="#AF261C")

banner_main = PhotoImage(file="main elements/banner2.png")
name_main = PhotoImage(file="main elements/name2.png")


# Load images for "Create Image" button (normal and hover)
create_normal = PhotoImage(file="main elements/create_image_button1.png")
#show_hover = PhotoImage(file="menu elements/show_button_on_hover.png")

# Load images for "Decode Image" button (normal and hover)
decode_normal = PhotoImage(file="main elements/decode_image_button1.png")
#exit_hover = PhotoImage(file="menu elements/exit_button_on_hover.png")

# Logo
try:
    logo_main = PhotoImage(file="logo1.png")
    Label(main_frame, image=name_main, bg="#AF261C").place(x=175, y=45)
    Label(main_frame, image=logo_main, bg="#AF261C").place(x=10, y=10)
    Button(main_frame, text="Create Image", image=create_normal,
           command= lambda: [show_hide_data_button()], bg="#AF261C", fg="#AF261C").place(x=67.5, y=100)
    Button(main_frame, text="Decode Image", image=decode_normal,
       command=lambda: [remove_hide_data_button()], bg="#AF261C", fg="#AF261C").place(x=287.5, y=100)
    Label(main_frame, image=banner_main, bg="#AF261C").place(x=520, y=80)


except Exception as e:
    Label(main_frame, text="Steganography App", bg="#AF261C", fg="white", font="Arial 20 bold").place(x=10, y=10)


# First Frame - Image Display
f = Frame(main_frame,bg="#D9D9D9", width=340, height=280)
f.place(x=70, y=210)

lbl = Label(f, bg="#D9D9D9")
lbl.place(x=40, y=10)

# Second Frame - Text Area
frame2 = Frame(main_frame, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=480, y=210)

text1 = Text(frame2, font="Roboto 14", bg="white", fg="black", relief=GROOVE)
text1.place(x=0, y=0, width=320, height=255)

scrollbar1 = Scrollbar(frame2, command=text1.yview)
scrollbar1.place(x=320, y=0, height=255)

text1.configure(yscrollcommand=scrollbar1.set)


# Load images for "Show Data" button (normal and hover)
show_normal = PhotoImage(file="main elements/show_button1.png")
show_hover = PhotoImage(file="main elements/show_data_button_hover.png")

# Load images for "Hide Data" button (normal and hover)
hide_normal = PhotoImage(file="main elements/hide_button1.png")
hide_hover = PhotoImage(file="main elements/hide_image_hover.png")

# Load images for "Open Image" button (normal and hover)
open_image = PhotoImage(file="main elements/open_img_button1.png")
open_hover = PhotoImage(file="main elements/open_image_hover.png")

# Load images for "Save Image" button (normal and hover)
save_image = PhotoImage(file="main elements/save_image_button1.png")
save_hover = PhotoImage(file="main elements/save_image_hover.png")



# Fourth Frame - Data Buttons - Reversed order so that Image Buttons appear first ;)
show_data_button = (Button(main_frame, image=show_normal, command=Show, bd=0, bg="#AF261C", fg="#AF261C"))
show_data_button.place(x=375, y=550)

hide_data_button = Button(main_frame, image=hide_normal, command=Hide, bd=0, bg="#AF261C", fg="#AF261C")
hide_data_button.place(x=375, y=550)


open_image_button = (Button(main_frame, image=open_image, command=showImage, bd=0, bg="#AF261C", fg="#AF261C"))
open_image_button.place(x=175, y=550)

save_image_button = (Button(main_frame, image=save_image, command=save, bd=0, bg="#AF261C", fg="#AF261C"))
save_image_button.place(x=580, y=550)


# Bind hover events for Open Image button
open_image_button.bind("<Enter>", lambda e: on_enter(e, open_hover))
open_image_button.bind("<Leave>", lambda e: on_leave(e, open_image))

# Bind hover events for Show Image button
show_data_button.bind("<Enter>", lambda e: on_enter(e, show_hover))
show_data_button.bind("<Leave>", lambda e: on_leave(e, show_normal))

# Bind hover events for Hide Data button
hide_data_button.bind("<Enter>", lambda e: on_enter(e, hide_hover))
hide_data_button.bind("<Leave>", lambda e: on_leave(e, hide_normal))

# Bind hover events for Save Image button
save_image_button.bind("<Enter>", lambda e: on_enter(e, save_hover))
save_image_button.bind("<Leave>", lambda e: on_leave(e, save_image))

# ======================================= Main Application Frame ========================================


# Initialize filename and secret variables
filename = ""
secret = None

# Start the main loop
root.mainloop()
