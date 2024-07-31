import subprocess
import tkinter as tk
from tkinter import scrolledtext

def get_saved_wifi_passwords():
    try:
        profiles_data = subprocess.check_output('netsh wlan show profiles', shell=True).decode('utf-8').split('\n')
        profiles = [line.split(":")[1].strip() for line in profiles_data if "All User Profile" in line]
        
        wifi_passwords = []

        for profile in profiles:
            profile_info = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True).decode('utf-8').split('\n')
            password_line = [line.split(":")[1].strip() for line in profile_info if "Key Content" in line]
            if password_line:
                password = password_line[0]
            else:
                password = "No Password Set"
            wifi_passwords.append((profile, password))

        return wifi_passwords
    except subprocess.CalledProcessError as e:
        return [("Error", "Could not retrieve profiles. Make sure to run the program with administrative privileges.")]

def display_wifi_passwords():
    wifi_passwords = get_saved_wifi_passwords()
    output_text.delete(1.0, tk.END)
    for wifi in wifi_passwords:
        output_text.insert(tk.END, f"SSID: {wifi[0]}, Password: {wifi[1]}\n")

# Create the main application window
app = tk.Tk()
app.title("Wi-Fi Password Retriever")
app.geometry("500x300")

# Create a button to retrieve Wi-Fi passwords
retrieve_button = tk.Button(app, text="Retrieve Wi-Fi Passwords", command=display_wifi_passwords)
retrieve_button.pack(pady=10)

# Create a scrolled text widget to display the passwords
output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=15)
output_text.pack(padx=10, pady=10)

# Start the GUI event loop
app.mainloop()
