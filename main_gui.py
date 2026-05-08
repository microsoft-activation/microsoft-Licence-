import tkinter as tk 
from tkinter import ttk, messagebox, scrolledtext 
import subprocess 
import sys 
import os 
import platform 
def resource_path(relative_path): 
    try: 
        base_path = sys._MEIPASS 
    except Exception: 
        base_path = os.path.abspath(".") 
    return os.path.join(base_path, relative_path) 
WINDOWS_KEYS = {
    "Windows 11 Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
    "Windows 11 Pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX", 
    "Windows 11 Education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    "Windows 11 Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "Windows 10 Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
    "Windows 10 Pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "Windows 10 Education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2", 
    "Windows 10 Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "Windows 8.1 Home": "",
    "Windows 8.1 Pro": "",
    "Windows 8.1 Education": "",
    "Windows 8.1 Enterprise": "",
    "Windows 8 Home": "",
    "Windows 8 Pro": "",
    "Windows 8 Education": "", 
    "Windows 8 Enterprise": "",
    "Windows 7 Home": "",
    "Windows 7 Pro": "",
    "Windows 7 Ultimate": "",
    "Windows 7 Enterprise": ""
}
selected_version = None
def execute_activation():
    """Execute activation based on selected version"""
    global selected_version
    if not selected_version:
        messagebox.showerror("Error", "Please select a Windows version first!")
        return
    key = WINDOWS_KEYS.get(selected_version)
    if not key:
        console_text.insert(tk.END, f"\n{selected_version} - Key not available\n")
        messagebox.showwarning("Not Supported", f"{selected_version} is currently not supported!")
        return
    console_text.delete(1.0, tk.END)
    console_text.insert(tk.END, f"Activating {selected_version}...\n")
    console_text.insert(tk.END, f"Product Key: {key}\n")
    console_text.insert(tk.END, "="*50 + "\n")
    ps_script = f"""
    Write-Host "Starting {selected_version} Activation..." -ForegroundColor Green
    slmgr /ipk {key}
    slmgr /skms kms8.msguides.com
    slmgr /ato
    Write-Host "Activation completed!" -ForegroundColor Green
    """
    try:
        process = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        ) 
        for line in process.stdout:
            console_text.insert(tk.END, line)
            console_text.see(tk.END)
            app.update()
        process.wait()
        console_text.insert(tk.END, "\nActivation process completed!\n")
        console_text.insert(tk.END, "\nPlease restart your computer to apply changes.\n")
    except Exception as e:
        console_text.insert(tk.END, f"\nError: {str(e)}\n")
def auto_detect_windows():
    """Auto detect Windows version with detailed info"""
    global selected_version
    console_text.delete(1.0, tk.END)
    console_text.insert(tk.END, "Detecting Windows version...\n")
    try:
        result = subprocess.run(
            'systeminfo | findstr /B /C:"OS Name" /C:"OS Version"',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            console_text.insert(tk.END, result.stdout + "\n")  
            os_info = result.stdout.strip()
            if "Windows 11" in os_info:
                if "Home" in os_info:
                    selected_version = "Windows 11 Home"
                elif "Pro" in os_info:
                    selected_version = "Windows 11 Pro"
                elif "Education" in os_info:
                    selected_version = "Windows 11 Education"
                elif "Enterprise" in os_info:
                    selected_version = "Windows 11 Enterprise"
                else:
                    selected_version = "Windows 11 Pro"
            elif "Windows 10" in os_info:
                if "Home" in os_info:
                    selected_version = "Windows 10 Home"
                elif "Pro" in os_info:
                    selected_version = "Windows 10 Pro"
                elif "Education" in os_info:
                    selected_version = "Windows 10 Education"
                elif "Enterprise" in os_info:
                    selected_version = "Windows 10 Enterprise"
                else:
                    selected_version = "Windows 10 Pro"
            else:
                selected_version = "Unknown Version"
            version_label.config(text=f"Detected: {selected_version}", foreground="#00ff00")
            console_text.insert(tk.END, f"\nAuto-detected: {selected_version}\n")
            if selected_version in WINDOWS_KEYS and WINDOWS_KEYS[selected_version]:
                activate_btn.config(state=tk.NORMAL, bg="#28a745", text=f"Activate {selected_version}")
            else:
                activate_btn.config(state=tk.DISABLED, bg="#6c757d", text="Version Not Supported") 
        else:
            version_label.config(text="Detection failed", foreground="#ff0000")
            console_text.insert(tk.END, "\nFailed to detect Windows version\n")
    except Exception as e:
        version_label.config(text="Detection failed", foreground="#ff0000")
        console_text.insert(tk.END, f"\nError: {str(e)}\n")
def select_windows_version(version):
    """User manually selects Windows version"""
    global selected_version
    selected_version = version
    selection_label.config(text=f"Selected: {version}", foreground="#00ff00")
    if version in WINDOWS_KEYS and WINDOWS_KEYS[version]:
        activate_btn.config(state=tk.NORMAL, bg="#28a745", text=f"Activate {version}")
        console_text.insert(tk.END, f"\nSelected: {version}\n")
        console_text.insert(tk.END, f"Key: {WINDOWS_KEYS[version]}\n")
    else:
        activate_btn.config(state=tk.DISABLED, bg="#6c757d", text="Version Not Supported")
        console_text.insert(tk.END, f"\n{version} - Currently Not Working\n")
def run_original_script(script_name):
    """Run original PowerShell scripts from your file system"""
    console_text.delete(1.0, tk.END)
    console_text.insert(tk.END, f"Executing {script_name}...\n")
    script_path = os.path.join(os.getcwd(), script_name)
    if not os.path.exists(script_path):
        console_text.insert(tk.END, f"\nError: {script_name} not found in current directory!\n")
        return
    try:
        process = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        for line in process.stdout:
            console_text.insert(tk.END, line)
            console_text.see(tk.END)
            app.update()
        process.wait()
        console_text.insert(tk.END, "\nProcess completed!\n")
    except Exception as e:
        console_text.insert(tk.END, f"\nError: {str(e)}\n")
app = tk.Tk() 
app.title("CyberActivator Pro v3.0") 
app.geometry("1000x750")
app.configure(bg="#1e1e1e")
try: 
    app.iconbitmap(resource_path("icon.ico")) 
except: 
    pass 
header_frame = tk.Frame(app, bg="#1e1e1e")
header_frame.pack(pady=15)
header = tk.Label(header_frame, 
                  text="CyberActivator Pro", 
                  font=("Segoe UI", 24, "bold"),
                  bg="#1e1e1e",
                  fg="#ffffff")
header.pack()
sub_header = tk.Label(header_frame,
                     text="Smart Activation System",
                     font=("Segoe UI", 12),
                     bg="#1e1e1e",
                     fg="#cccccc")
sub_header.pack()
detect_frame = tk.Frame(app, bg="#2d2d2d", relief=tk.RAISED, bd=1)
detect_frame.pack(pady=10, padx=20, fill="x")
detect_btn = tk.Button(detect_frame,
                      text="Auto Detect Windows Version",
                      command=auto_detect_windows,
                      font=("Segoe UI", 11, "bold"),
                      bg="#0078d4",
                      fg="white",
                      activebackground="#005a9e",
                      activeforeground="white",
                      relief=tk.FLAT,
                      padx=20,
                      pady=8,
                      cursor="hand2")
detect_btn.pack(pady=5)
version_label = tk.Label(detect_frame,
                        text="Click button to detect",
                        font=("Segoe UI", 10),
                        bg="#2d2d2d",
                        fg="#cccccc")
version_label.pack(pady=5)
selection_display = tk.Frame(app, bg="#1e1e1e")
selection_display.pack(pady=5)
selection_label = tk.Label(selection_display,
                          text="No version selected",
                          font=("Segoe UI", 11, "bold"),
                          bg="#1e1e1e",
                          fg="#cccccc")
selection_label.pack()
button_frame = tk.Frame(app, bg="#1e1e1e")
button_frame.pack(pady=10)
activate_btn = tk.Button(button_frame,
                        text="Select Windows Version First",
                        command=execute_activation,
                        font=("Segoe UI", 13, "bold"),
                        bg="#6c757d",
                        fg="white",
                        activebackground="#28a745",
                        activeforeground="white",
                        relief=tk.RAISED,
                        bd=3,
                        width=30,
                        height=2,
                        state=tk.DISABLED,
                        cursor="hand2")
activate_btn.pack()
separator_frame = tk.Frame(app, bg="#1e1e1e")
separator_frame.pack(pady=5)
separator_label = tk.Label(separator_frame,
                          text="───── OR Use Original Scripts ─────",
                          font=("Segoe UI", 10),
                          bg="#1e1e1e",
                          fg="#888888")
separator_label.pack()
scripts_frame = tk.LabelFrame(app,
                             text=" Original PowerShell Scripts ",
                             font=("Segoe UI", 12, "bold"),
                             bg="#2d2d2d",
                             fg="#ffffff",
                             relief=tk.GROOVE,
                             bd=2)
scripts_frame.pack(pady=10, padx=20, fill="x")
scripts_btn_frame = tk.Frame(scripts_frame, bg="#2d2d2d")
scripts_btn_frame.pack(pady=10)
btn1 = tk.Button(scripts_btn_frame,
                text="Windows 8/10/11",
                command=lambda: run_original_script("win8_10_11.ps1"),
                font=("Segoe UI", 10, "bold"),
                bg="#107c10",
                fg="white",
                activebackground="#0c5c0c",
                activeforeground="white",
                relief=tk.RAISED,
                bd=2,
                width=18,
                height=1,
                cursor="hand2")
btn1.grid(row=0, column=0, padx=10, pady=5)
btn2 = tk.Button(scripts_btn_frame,
                text="🔧 Windows 7/Later",
                command=lambda: run_original_script("win7_later.ps1"),
                font=("Segoe UI", 10, "bold"),
                bg="#d83b01",
                fg="white",
                activebackground="#a52c01",
                activeforeground="white",
                relief=tk.RAISED,
                bd=2,
                width=18,
                height=1,
                cursor="hand2")
btn2.grid(row=0, column=1, padx=10, pady=5)
btn3 = tk.Button(scripts_btn_frame,
                text="Alternative Method",
                command=lambda: run_original_script("alt_method.ps1"),
                font=("Segoe UI", 10, "bold"),
                bg="#ffb900",
                fg="black",
                activebackground="#cc9400",
                activeforeground="black",
                relief=tk.RAISED,
                bd=2,
                width=18,
                height=1,
                cursor="hand2")
btn3.grid(row=0, column=2, padx=10, pady=5)
def toggle_version_selection():
    if version_selection_frame.winfo_ismapped():
        version_selection_frame.pack_forget()
        toggle_btn.config(text="Show Windows Version Selection")
    else:
        version_selection_frame.pack(pady=10, padx=20, fill="both", expand=True)
        toggle_btn.config(text="▲ Hide Windows Version Selection")
toggle_btn = tk.Button(app,
                      text="▼ Show Windows Version Selection",
                      command=toggle_version_selection,
                      font=("Segoe UI", 10),
                      bg="#495057",
                      fg="white",
                      relief=tk.FLAT,
                      cursor="hand2")
toggle_btn.pack(pady=5)
version_selection_frame = tk.LabelFrame(app,
                                       text=" Select Windows Version Manually ",
                                       font=("Segoe UI", 12, "bold"),
                                       bg="#2d2d2d",
                                       fg="#ffffff",
                                       relief=tk.GROOVE,
                                       bd=2)
versions_grid = tk.Frame(version_selection_frame, bg="#2d2d2d")
versions_grid.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(versions_grid, text="Windows 11:", font=("Segoe UI", 10, "bold"), 
         bg="#2d2d2d", fg="#00ff00").grid(row=0, column=0, sticky="w", pady=5)
win11_versions = ["Windows 11 Home", "Windows 11 Pro", "Windows 11 Education", "Windows 11 Enterprise"]
for i, version in enumerate(win11_versions):
    btn = tk.Button(versions_grid,
                   text=version,
                   command=lambda v=version: select_windows_version(v),
                   font=("Segoe UI", 9),
                   bg="#495057",
                   fg="white",
                   relief=tk.RAISED,
                   bd=1,
                   width=20,
                   cursor="hand2")
    btn.grid(row=1, column=i, padx=5, pady=2)
tk.Label(versions_grid, text="Windows 10:", font=("Segoe UI", 10, "bold"), 
         bg="#2d2d2d", fg="#00ff00").grid(row=2, column=0, sticky="w", pady=(10,5))
win10_versions = ["Windows 10 Home", "Windows 10 Pro", "Windows 10 Education", "Windows 10 Enterprise"]
for i, version in enumerate(win10_versions):
    btn = tk.Button(versions_grid,
                   text=version,
                   command=lambda v=version: select_windows_version(v),
                   font=("Segoe UI", 9),
                   bg="#495057",
                   fg="white",
                   relief=tk.RAISED,
                   bd=1,
                   width=20,
                   cursor="hand2")
    btn.grid(row=3, column=i, padx=5, pady=2)
tk.Label(versions_grid, text="Other Versions:", font=("Segoe UI", 10, "bold"), 
         bg="#2d2d2d", fg="#ff9900").grid(row=4, column=0, sticky="w", pady=(10,5))
other_versions = ["Windows 8.1 Pro", "Windows 8 Pro", "Windows 7 Pro", "Windows 7 Ultimate"]
for i, version in enumerate(other_versions):
    btn = tk.Button(versions_grid,
                   text=version,
                   command=lambda v=version: select_windows_version(v),
                   font=("Segoe UI", 9),
                   bg="#6c757d",
                   fg="white",
                   relief=tk.RAISED,
                   bd=1,
                   width=20,
                   cursor="hand2")
    btn.grid(row=5, column=i, padx=5, pady=2)
console_frame = tk.LabelFrame(app,
                             text=" Live Console ",
                             font=("Segoe UI", 12, "bold"),
                             bg="#1e1e1e",
                             fg="#ffffff",
                             relief=tk.GROOVE,
                             bd=2)
console_frame.pack(pady=10, padx=20, fill="both", expand=True)
console_text = scrolledtext.ScrolledText(console_frame,
                                        height=12,
                                        bg="#000000",
                                        fg="#00ff00",
                                        font=("Consolas", 10),
                                        insertbackground="#ffffff",
                                        relief=tk.SUNKEN,
                                        bd=3)
console_text.pack(padx=10, pady=10, fill="both", expand=True)
console_text.insert(tk.END, "╔══════════════════════════════════════════════════════╗\n")
console_text.insert(tk.END, "║           CyberActivator Pro v3.0                    ║\n")
console_text.insert(tk.END, "╚══════════════════════════════════════════════════════╝\n\n")
console_text.insert(tk.END, "   Instructions:\n")
console_text.insert(tk.END, "1. Click 'Auto Detect' or manually select Windows version\n")
console_text.insert(tk.END, "2. Click 'Activate' button to start activation\n")
console_text.insert(tk.END, "3. OR use original PowerShell scripts below\n\n")
console_text.insert(tk.END, "   Administrator privileges required!\n")
footer_frame = tk.Frame(app, bg="#1e1e1e")
footer_frame.pack(pady=10)
footer = tk.Label(footer_frame,
                 text="Use at your own risk | Run as Administrator required",
                 font=("Segoe UI", 10),
                 bg="#1e1e1e",
                 fg="#ff6b6b")
footer.pack()
copyright_label = tk.Label(footer_frame,
                          text="© 2025 CyberActivator Pro v3.0",
                          font=("Segoe UI", 9),
                          bg="#1e1e1e",
                          fg="#888888")
copyright_label.pack(pady=5)
app.mainloop()