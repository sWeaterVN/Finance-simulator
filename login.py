import tkinter as tk 
from tkinter import messagebox 
import os

root = tk.Tk()
root.title("welcome!")
root.geometry("400x250")

label = tk.Label(root, text="Enter your account", font=("Arial", 12))
label.pack(pady=10)

def is_log_button():
    username = entry_us.get()
    password = entry_pas.get()
    try:
        with open("infomation.txt", "r") as file:
            accounts = file.readlines()
            for account in accounts:
                if " : " not in account:
                    continue
                stored_user, stored_pass = account.strip().split(" : ")
                if username == stored_user and password == stored_pass:
                    messagebox.showinfo("Login Successful", "You have logged in successfully!")
                    root.destroy()
                    os.system("python main.py")
                    return
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No accounts found. Please sign up first.")

def is_sign_button():
    def save_account():
        new_username = new_entry_us.get()
        new_password = new_entry_pas.get()
        if new_username and new_password:
            with open("infomation.txt", "a") as file:
                file.write(f"\n{new_username} : {new_password}\n")
            messagebox.showinfo("Success", "Account created successfully!")
            sign_up_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("300x200")

    tk.Label(sign_up_window, text="User name:").pack(pady=5)
    new_entry_us = tk.Entry(sign_up_window, width=30)
    new_entry_us.pack(pady=5)

    tk.Label(sign_up_window, text="Password:").pack(pady=5)
    new_entry_pas = tk.Entry(sign_up_window, width=30, show="*")
    new_entry_pas.pack(pady=5)

    tk.Button(sign_up_window, text="Sign Up", command=save_account).pack(pady=10)

# login
frame1 = tk.Frame(root)
frame1.pack(pady=10)

txt_us = tk.Label(frame1, text="User name:")
txt_us.pack(side="left", padx=5)
entry_us = tk.Entry(frame1, width=30)
entry_us.pack(side="right", padx=5)

frame2 = tk.Frame(root)
frame2.pack(pady=10)

txt_pas = tk.Label(frame2, text="Password:")
txt_pas.pack(side="left", padx=5)
entry_pas = tk.Entry(frame2, width=30, show="*")
entry_pas.pack(side="right", padx=5)

login_button = tk.Button(root, text="Login", command=is_log_button)
login_button.pack(pady=10)

# sign up
frame3 = tk.Frame(root)
frame3.pack(pady=20)

txt_no_account = tk.Label(frame3, text="No account? Create a new!")
txt_no_account.pack(side="left", padx=5)
sign_up_button = tk.Button(frame3, text="Sign Up", command=is_sign_button)
sign_up_button.pack(side="right", padx=5)

root.mainloop()