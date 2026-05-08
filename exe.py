import os
import subprocess
import shutil
def build_exe():
    """Build EXE with all necessary options"""
    APP_NAME = "CyberActivatorPro"
    MAIN_FILE = "main_gui.py"
    ICON_FILE = "icon.ico"
    print("Cleaning previous builds...")
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    for file in os.listdir("."):
        if file.endswith(".spec"):
            os.remove(file)
    cmd = [
        "pyinstaller",
        "--onefile",                    
        "--windowed",                 
        "--name", APP_NAME,            
        "--clean",                     
        "--noconfirm",                 
        "--log-level=INFO",            
    ]
    if os.path.exists(ICON_FILE):
        cmd.extend(["--icon", ICON_FILE])
    cmd.extend([
        "--hidden-import", "tkinter",
        "--hidden-import", "subprocess",
        "--hidden-import", "platform",
        "--hidden-import", "sys",
        "--hidden-import", "os"
    ])
    cmd.append(MAIN_FILE)    
    print("\n" + "="*60)
    print(f"Building {APP_NAME}.exe...")
    print("="*60)
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("BUILD SUCCESSFUL!")
            print("="*60)            
            exe_path = os.path.abspath(f"dist/{APP_NAME}.exe")            
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"\n EXE Location: {exe_path}")
                print(f"File Size: {size_mb:.2f} MB")
                shutil.copy(exe_path, f"./{APP_NAME}.exe")
                print(f"Also copied to: {os.getcwd()}/{APP_NAME}.exe")                
                print("\n You can now run: CyberActivatorPro.exe")
                print("Remember to Run as Administrator!")
            else:
                print("EXE file not found!")
        else:
            print("\nBUILD FAILED!")            
    except FileNotFoundError:
        print("\nPyInstaller not found!")
        print("Install it: pip install pyinstaller")
    except Exception as e:
        print(f"\nError: {str(e)}")
if __name__ == "__main__":
    build_exe()