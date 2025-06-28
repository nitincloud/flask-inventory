import requests
import platform
import socket
import psutil
import subprocess

# Server where Flask is running
FLASK_URL = "http://192.168.0.30:5000/add"  # Replace with your real server IP

# Collect system info
device_name = socket.gethostname()
full_device_name = socket.getfqdn()

processor = platform.processor()
arch, _ = platform.architecture()
system_type = f"{platform.system()} {arch}"

# RAM
ram_bytes = psutil.virtual_memory().total
ram_gb = round(ram_bytes / (1024 ** 3), 1)

# Pen & touch support (Windows only)
try:
    output = subprocess.check_output("powershell Get-PnpDevice | findstr Touch", shell=True).decode()
    touch_support = "Touch Supported" if "Touch" in output else "No pen or touch input"
except:
    touch_support = "Unknown"

# Build readable string
item_name = (
    f"Device: {device_name} | Full: {full_device_name} | CPU: {processor} | "
    f"RAM: {ram_gb} GB | System: {system_type} | Touch: {touch_support}"
)

# Send to Flask
data = {
    "name": item_name,
    "quantity": 1
}

try:
    response = requests.post(FLASK_URL, json=data)
    if response.status_code == 200:
        print("✅ System info sent successfully!")
    else:
        print(f"❌ Failed to send data: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
