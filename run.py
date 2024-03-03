import subprocess
import tkinter as tk
import atexit

def run_powershell_command(command):
    """ Run a PowerShell command from Python """
    subprocess.run(["powershell", "-Command", command], check=True)

def set_proxy(enable, address=None, port=None):
    """ Sets or unsets the system proxy settings using PowerShell """
    try:
        if enable and address and port:
            proxy_command = f"Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' -Name ProxyServer -Value '{address}:{port}'"
            enable_command = "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' -Name ProxyEnable -Value 1"
            run_powershell_command(proxy_command)
            run_powershell_command(enable_command)
            print("Proxy enabled.")
        else:
            disable_command = "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' -Name ProxyEnable -Value 0"
            run_powershell_command(disable_command)
            print("Proxy disabled.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def run_sslocal():
    """ Runs the sslocal.exe command """
    print("Running 'sslocal.exe -c config.json'. Press CTRL+C to terminate.")
    return subprocess.Popen(["sslocal.exe", "-c", "config.json"])

def disable_proxy_at_exit(sslocal_process):
    """ Disables the proxy and terminates the sslocal process """
    set_proxy(False)
    sslocal_process.terminate()
    print("sslocal.exe terminated.")

def create_gui(sslocal_process):
    """ Create a GUI window with a button to disable the VPN """
    root = tk.Tk()
    root.title("VPN Control")

    def on_close():
        disable_proxy_at_exit(sslocal_process)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    button = tk.Button(root, text="Disable VPN", command=on_close)
    button.pack(pady=20, padx=20)

    root.mainloop()

if __name__ == "__main__":
    set_proxy(True, "127.0.0.1", "1080")
    sslocal_process = run_sslocal()
    create_gui(sslocal_process)
