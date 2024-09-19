import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys
import threading

# Define the version of the application
APP_VERSION = "1.0.0"

# Function to execute git commands including subtree
def execute_git_commands(repo_url, subtree_url, ref, tab_control, add_tab_index):
    # Check if any of the inputs are empty
    if not repo_url or not subtree_url or not ref:
        messagebox.showwarning("Input Error", "All fields must be filled in.")
        return
    
    def confirm_and_execute():
        try:
            git_executable = os.path.join(sys._MEIPASS, 'PortableGit', 'bin', 'git.exe')  # Access git.exe using relative path

            if not os.path.exists(git_executable):
                raise FileNotFoundError(f"Git executable not found at: {git_executable}")

            # Run git commands in batch
            commands = [
                [git_executable, 'config', '--global', 'core.autocrlf', 'false'],
                [git_executable, 'init'],
                [git_executable, 'remote', 'add', 'origin', repo_url],
                [git_executable, 'add', '--all'],
                [git_executable, 'commit', '-m', ':tada: Initial Commit'],
                [git_executable, 'subtree', 'add', '--prefix', 'subtree', subtree_url, ref]
            ]

            for cmd in commands:
                subprocess.run(cmd, check=True)

            # Display success message
            messagebox.showinfo("Success", "Subtree add operation completed successfully!")
            
            # Hide the "Add Subtree" tab
            tab_control.forget(add_tab_index)

            # Show and select the "Pull Subtree" tab after a successful subtree add
            pull_tab = ttk.Frame(tab_control)
            tab_control.add(pull_tab, text="Pull Subtree")
            setup_pull_tab(pull_tab, tab_control)
            tab_control.select(pull_tab)  # Select the "Pull Subtree" tab

        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Git command failed: {e}")

    # Pop-up confirmation window
    confirm_window = tk.Toplevel()
    confirm_window.title("Confirm Remote")
    confirm_window.geometry("800x200")

    warning_label = ttk.Label(confirm_window, text="Please confirm if the remote URL is correct:")
    warning_label.pack(pady=10)

    # Display the repo_url in a more conspicuous way
    url_label = ttk.Label(confirm_window, text=repo_url, font=("Arial", 12, "bold"), foreground="red", wraplength=750)
    url_label.pack(pady=10)

    confirm_button = ttk.Button(confirm_window, text="Confirm", command=lambda: [confirm_window.destroy(), run_in_thread(confirm_and_execute)])
    confirm_button.pack(side=tk.LEFT, padx=20, pady=10)

    cancel_button = ttk.Button(confirm_window, text="Cancel", command=confirm_window.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Function to perform git subtree pull in a separate thread to keep the GUI responsive
def execute_git_subtree_pull(subtree_url, ref):
    try:
        git_executable = os.path.join(sys._MEIPASS, 'PortableGit', 'bin', 'git.exe')

        if not os.path.exists(git_executable):
            raise FileNotFoundError(f"Git executable not found at: {git_executable}")

        # Pull the subtree
        subprocess.run([git_executable, 'subtree', 'pull', '--prefix', 'subtree', subtree_url, ref], check=True)
        messagebox.showinfo("Success", "Subtree pull operation completed successfully!")
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Git command failed: {e}")

# Run git commands in a separate thread to keep the GUI responsive
def run_in_thread(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.start()

# Function to set up the "Pull Subtree" tab
def setup_pull_tab(pull_tab, tab_control):
    subtree_repo_pull_label = ttk.Label(pull_tab, text="Enter Subtree Repository URL (HTTPS): ")
    subtree_repo_pull_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    subtree_repo_pull_entry = ttk.Entry(pull_tab, width=50)
    subtree_repo_pull_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    pull_tab.columnconfigure(1, weight=1)

    ref_pull_label = ttk.Label(pull_tab, text="Enter Commit SHA, Branch Name, or Tag: ")
    ref_pull_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ref_pull_entry = ttk.Entry(pull_tab, width=50)
    ref_pull_entry.grid(row=1, column=1, padx=10, pady=5, sticky="e")
    pull_tab.columnconfigure(1, weight=1)

    submit_button_pull = ttk.Button(pull_tab, text="Pull Subtree", 
                                    command=lambda: run_in_thread(execute_git_subtree_pull, subtree_repo_pull_entry.get(), ref_pull_entry.get()))
    submit_button_pull.grid(row=2, column=0, columnspan=2, pady=20)

# GUI setup
def create_gui(is_git_initialized):
    root = tk.Tk()
    root.title(f"Git Subtree Automation Tool v{APP_VERSION}")

    # Show the initial UI as soon as possible
    root.update()

    def load_additional_components():
        tab_control = ttk.Notebook(root)
        add_tab_index = None

        if not is_git_initialized:
            add_tab = ttk.Frame(tab_control)
            add_tab_index = tab_control.index("end")
            tab_control.add(add_tab, text="Add Subtree")

            remote_frame = ttk.LabelFrame(add_tab, text="Remote Add")
            remote_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

            main_repo_label = ttk.Label(remote_frame, text="Enter GitLab Repository URL (HTTPS): ")
            main_repo_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            main_repo_entry = ttk.Entry(remote_frame, width=50)
            main_repo_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
            remote_frame.columnconfigure(1, weight=1)

            subtree_frame = ttk.LabelFrame(add_tab, text="Subtree Add")
            subtree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

            subtree_repo_label = ttk.Label(subtree_frame, text="Enter Subtree Repository URL (HTTPS): ")
            subtree_repo_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            subtree_repo_entry = ttk.Entry(subtree_frame, width=50)
            subtree_repo_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
            subtree_frame.columnconfigure(1, weight=1)

            ref_label = ttk.Label(subtree_frame, text="Enter Commit SHA, Branch Name, or Tag: ")
            ref_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            ref_entry = ttk.Entry(subtree_frame, width=50)
            ref_entry.grid(row=1, column=1, padx=10, pady=5, sticky="e")
            subtree_frame.columnconfigure(1, weight=1)

            submit_button_add = ttk.Button(add_tab, text="Initialize Git and Add Subtree", 
                                           command=lambda: run_in_thread(execute_git_commands, main_repo_entry.get(), subtree_repo_entry.get(), ref_entry.get(), tab_control, add_tab_index))
            submit_button_add.grid(row=2, column=0, columnspan=2, pady=20)

        # Conditionally add the "Pull Subtree" tab only if .git exists
        if is_git_initialized:
            pull_tab = ttk.Frame(tab_control)
            tab_control.add(pull_tab, text="Pull Subtree")
            setup_pull_tab(pull_tab, tab_control)

        tab_control.pack(expand=1, fill="both")

        if not is_git_initialized:
            tab_control.select(0)

    # Load additional components in a separate thread to improve startup speed
    threading.Thread(target=load_additional_components).start()

    # Display the main window
    root.mainloop()

def check_git_initialized():
    return os.path.isdir(".git")

if __name__ == "__main__":    
    is_git_initialized = check_git_initialized()
    create_gui(is_git_initialized)

