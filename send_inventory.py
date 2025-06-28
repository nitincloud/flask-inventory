# send_inventory.py (Agent Script)
import platform
import socket
import uuid
import psutil
import requests
import json

SERVER_URL = "http://192.168.0.30:5000/add"  # Your Flask server IP

def get_device_info():
    return {
        "name": f"Laptop|{platform.system()}|1|{get_asset_tag()}|{get_serial_number()}|{platform.node()}|{get_user()}|{get_location()}|{get_year()}|{get_ip()}"
    }

def get_serial_number():
    return str(uuid.getnode())

def get_user():
    return psutil.users()[0].name if psutil.users() else "unknown"

def get_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except:
        return "0.0.0.0"

def get_asset_tag():
    return "US/CE/LP/001"

def get_location():
    return "Mumbai"

def get_year():
    return "2025"

def main():
    try:
        payload = get_device_info()
        print(f"Sending: {json.dumps(payload, indent=2)}")
        res = requests.post(SERVER_URL, json=payload)
        if res.status_code == 200:
            print("✅ Data sent successfully.")
        else:
            print(f"❌ Failed with status code: {res.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
