import os
import tkinter as tk
from tkinter import ttk
from fuzzywuzzy import process

def search_files(keyword, folder_path):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if keyword in file.lower():
                results.append(os.path.join(root, file))
    return results

def suggest_files(keyword, folder_path, max_results=20):
    suggested_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if keyword in file.lower():
                suggested_files.append(os.path.join(root, file))
                if len(suggested_files) == max_results:
                    break
        if len(suggested_files) == max_results:
            break
    return suggested_files

def filter_files(suggested_files, keyword, threshold=0.6):
    filtered_files = []
    for file in suggested_files:
        score = process.extractOne(keyword, file)[1] / 100
        if score >= threshold:
            filtered_files.append(file)
    return filtered_files

def update_suggestions(*args):
    keyword = entry.get().lower()
    folder_path = folder_path_entry.get()  # Use the user input folder path
    suggested_files = suggest_files(keyword, folder_path, max_results=20)
    filtered_files = filter_files(suggested_files, keyword)
    lb.delete(0, tk.END)
    for file in filtered_files:
        lb.insert(tk.END, file)

root = tk.Tk()
root.geometry("600x400")
root.title("File Search")

style = ttk.Style()
style.theme_use('classic')
style.configure('TLabel', font=('Calibri', 14))
style.configure('TButton', font=('Calibri', 14))

frame = tk.Frame(root)
frame.pack(pady=20)

folder_path_frame = tk.Frame(frame)  # Add a new frame for the folder path entry
folder_path_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

folder_path_entry = ttk.Entry(folder_path_frame, font=("Calibri", 14), width=60)
folder_path_entry.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
folder_path_entry.insert(0, r"C:\Users\'user'\OneDrive")  # Set the default folder path

entry = ttk.Entry(frame, font=("Calibri", 16), width=60)
entry.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
entry.bind('<KeyRelease>', update_suggestions)

list_frame = tk.Frame(root)
list_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

xscrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

lb = tk.Listbox(list_frame, width=80, height=20, font=("Calibri", 12), yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
lb.pack(pady=10, fill=tk.BOTH, expand=True)

yscrollbar.config(command=lb.yview)
xscrollbar.config(command=lb.xview)

lb.bind("<Double-Button-1>", lambda event: os.startfile(lb.get(lb.curselection())))

root.mainloop()
