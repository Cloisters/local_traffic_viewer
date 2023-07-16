import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import os
import requests

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return None

def ping_ip(ip):
    response = os.system(f"ping -n 1 -w 1 {ip}")
    return ip if response == 0 else None

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return ""

def scan_home_network(local_ip, progress_var):
    ip_addresses = []
    hostnames = []
    response_codes = []
    prefix = ".".join(local_ip.split(".")[:-1])
    total_addresses = 254

    def update_progress():
        scanned_addresses = len(ip_addresses)
        progress = int(scanned_addresses / total_addresses * 100)
        progress_var.set(progress)

    with ThreadPoolExecutor() as executor:
        future_to_ip = {executor.submit(ping_ip, f"{prefix}.{i}"): f"{prefix}.{i}" for i in range(1, 255)}
        for future in as_completed(future_to_ip):
            ip = future.result()
            if ip:
                ip_addresses.append(ip)
                hostnames.append(get_hostname(ip))
                response_code = get_response_code(ip)
                response_codes.append(response_code)
                update_progress()

    progress_var.set(100)
    return ip_addresses, hostnames, response_codes

def get_response_code(ip):
    try:
        response = requests.get(f"http://{ip}", timeout=3)
        return response.status_code
    except requests.RequestException:
        return "N/A"

def update_ip_list():
    local_ip = get_local_ip()
    if local_ip:
        try:
            progress_var.set(0)
            ip_addresses, hostnames, response_codes = scan_home_network(local_ip, progress_var)
            tree.delete(*tree.get_children())
            for ip, hostname, response_code in zip(ip_addresses, hostnames, response_codes):
                online = ping_ip(ip)
                color = "green" if online else "red"
                tree.insert("", tk.END, values=(ip, hostname, response_code), tags=(color,))
        except Exception as e:
            tree.delete(*tree.get_children())
            tree.insert("", tk.END, values=("Error occurred", str(e)), tags=("red",))
    else:
        tree.delete(*tree.get_children())
        tree.insert("", tk.END, values=("Failed to retrieve local IP address.", ""), tags=("red",))

# GUI Setup
root = tk.Tk()
root.title("Home Network IP Scanner")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", fieldbackground="white")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Active IP Addresses in Your Home Network:")
label.pack()

tree = ttk.Treeview(frame, columns=("IP Address", "System Owner", "Response Code"), show="headings")
tree.heading("IP Address", text="IP Address")
tree.heading("System Owner", text="System Owner")
tree.heading("Response Code", text="Response Code")

tree.column("IP Address", width=120)
tree.column("System Owner", width=120)
tree.column("Response Code", width=100)

tree.tag_configure("green", background="green")
tree.tag_configure("red", background="red")

tree.pack()

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, mode='determinate', variable=progress_var)
progress_bar.pack(pady=5)

update_button = tk.Button(root, text="Scan Network", command=update_ip_list)
update_button.pack(pady=10)

root.mainloop()
