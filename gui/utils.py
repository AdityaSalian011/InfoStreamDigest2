import json, os, re
import tkinter as tk
from tkinter import messagebox
from email_validator import validate_email, EmailNotValidError

def get_user_data(file_name):
    """A helper function to get already rgistered user(if there is any)."""
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            try:
                user_data = json.loads(f.read())
            except Exception:
                user_data = {}
    else:
        user_data = {}
    
    return user_data

def create_entry_windows(frame_user, field:str, user_data, row, col=0):
    """
    frame_user here is the tk.LabelFrame object
    field is the desired entry field 
        i.e. username, email, api_key etc
    """
    tk.Label(frame_user, text=field.title()+':', font=('Arial', 14), bg='#2c2c2c', fg='white').grid(row=row, column=col, sticky='w', pady=5)
    entry = tk.Entry(frame_user, font=('Arial', 14), bg='#1e1e1e', fg='#00ffcc', insertbackground='white')
    entry.config(font=('Arial', 14), bg='#212121', fg='#00FF00')
    entry.grid(row=row, column=col+1, padx=10, pady=5, sticky='ew')
    entry.insert(0, user_data.get(field, ''))

    frame_user.columnconfigure(col+1, weight=1)
    return entry

def create_button(master, field:str, col=0, row=0):
    style_btn = {"font": ("Arial", 14, "bold"), "bg": "#007acc", "fg": "white", "activebackground": "#005f99", "activeforeground": "white", "relief": "flat", "bd": 0, "width": 15}

    btn = tk.Button(master, text=field.title(), **style_btn)
    btn.grid(row=row, column=col, padx=20, pady=10)
    return btn

def show_error_message(message):
    messagebox.showerror('Error', message)

def show_success_message(message):
    messagebox.showinfo('Success', message)

def check_username_pattern(username):
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    matching = re.search(pattern, username)
    if matching:
        return True
    return False

def check_email_pattern(email):
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, e
    
def store_user_data(new_user_data, file_name):
    """
    Storing new user data in a JsonFile.
    """
    json_contents = json.dumps(new_user_data, indent=4)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json_contents)

def create_entry_label_widgets(frame_user, row, col, text='Select a news topic'):
    label = tk.Label(
        frame_user, 
        text=text.title()+':', 
        font=('Arial', 14), 
        bg='#2c2c2c', 
        fg='white'
        ).grid(row=row, column=col, sticky='w', pady=5)
    
    entry_widget = tk.Entry(
        frame_user, 
        font=('Arial', 14), 
        bg='#1e1e1e', 
        fg='#00ffcc', 
        insertbackground='white',
        width=50
        )
    ## hide entry widget initially
    return label, entry_widget

def on_radio_button(entry_widget, selected_topic):
    selected = selected_topic.get()
    if str(selected).lower() == 'other':
        entry_widget.grid()     ## if selected radio btn is other, entry widget is displayed
        entry_widget.focus()
    else:
        entry_widget.grid_remove()      ## if not, entry widget is hidden
    
def get_selected_topic(entry_widget, selected_topic):
    selected = selected_topic.get()
    if str(selected).lower() == 'other':
        e_widget = entry_widget.get().strip()
        if e_widget:
            """If selected radio btn is other, and if it is not empty"""
            return e_widget, None   ## selected news topic is what user wrote in entry widget
        return None, 'Entry widget empty, please consider filling it.'  ## else we show them an error
    return selected, None
    
def create_radio_buttons(master, entry_widget, selected_topic:tk.StringVar, row, col):
    topics = [
        'trending',
        'technological trends',
        'public market',
        'sports',
        'entertainment',
        'other'
    ]

    rb_style = {
        'font': ('Arial', 15),
        'anchor': 'w',
        'bg': '#2c2c2c',
        'fg': 'white',
        'selectcolor': '#1e1e1e'
    }

    for i, topic in enumerate(topics):
        rb = tk.Radiobutton(
            master, 
            text=topic, 
            value=topic, 
            variable=selected_topic, 
            command=lambda: on_radio_button(entry_widget, selected_topic),
            **rb_style          
            )
        rb.grid(row=row, column=col+i, padx=5, pady=2)