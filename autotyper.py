import tkinter as tk
import keyboard
import time
import threading

#%%
def start_typing():
    text = text_entry.get("1.0", tk.END).strip()
    delay = float(delay_entry.get())
    
    def type_text():
        time.sleep(3)  # Give the user time to focus on the target window
        for char in text:
            keyboard.write(char)
            time.sleep(delay)
    
    threading.Thread(target=type_text, daemon=True).start()

# Create the main window
root = tk.Tk()
root.title("Auto Typer")
root.geometry("400x300")

tk.Label(root, text="Enter Text to Auto-Type:").pack()
text_entry = tk.Text(root, height=10, width=40)
text_entry.pack()

tk.Label(root, text="Typing Speed (seconds per character):").pack()
delay_entry = tk.Entry(root)
delay_entry.pack()
delay_entry.insert(0, "0.1")

tk.Button(root, text="Start Typing", command=start_typing).pack()

root.mainloop()