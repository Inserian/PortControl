import socket
import tkinter as tk
from tkinter import ttk, messagebox
import platform

class PortBlocker:
    def __init__(self, master):
        self.master = master
        self.master.title("Port Blocker Enhanced")
        self.master.geometry("700x500")

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Panic.TButton', font=('Arial', 10), background='red')
        self.style.configure('Release.TButton', font=('Arial', 10), background='green')

        # Header Label
        self.header_label = ttk.Label(master, text="Port Blocker Utility", font=('Arial', 14, 'bold'))
        self.header_label.pack(pady=10)

        # Ports Label and Entry
        self.ports_label = ttk.Label(master, text="Enter ports (separated by commas) or leave empty to check default range:",
                                     font=('Arial', 10))
        self.ports_label.pack(pady=5)
        self.ports_entry = ttk.Entry(master, width=60)
        self.ports_entry.pack(pady=5)

        # Buttons Frame for Check, Block, Unblock, and System Info
        self.buttons_frame = ttk.Frame(master)
        self.buttons_frame.pack(pady=10)
        self.check_button = ttk.Button(self.buttons_frame, text="Check Ports", command=lambda: self.check_ports(all_ports=False))
        self.check_button.pack(side=tk.LEFT, padx=5)
        self.check_all_button = ttk.Button(self.buttons_frame, text="Check All Ports", command=lambda: self.check_ports(all_ports=True))
        self.check_all_button.pack(side=tk.LEFT, padx=5)
        self.block_button = ttk.Button(self.buttons_frame, text="Block Port", command=self.block_port)
        self.block_button.pack(side=tk.LEFT, padx=5)
        self.unblock_button = ttk.Button(self.buttons_frame, text="Unblock Port", command=self.unblock_port)
        self.unblock_button.pack(side=tk.LEFT, padx=5)
        self.sys_info_button = ttk.Button(self.buttons_frame, text="System Info", command=self.display_system_info)
        self.sys_info_button.pack(side=tk.LEFT, padx=5)

        # Panic and Release Buttons
        self.panic_button = ttk.Button(master, text="Panic Block", style='Panic.TButton', command=self.panic_block)
        self.panic_button.pack(side=tk.LEFT, padx=10, pady=20)
        self.release_button = ttk.Button(master, text="Release Ports", style='Release.TButton', command=self.release_ports)
        self.release_button.pack(side=tk.RIGHT, padx=10, pady=20)

        # Status Label
        self.status_label = ttk.Label(master, text="", font=('Arial', 10))
        self.status_label.pack(pady=5)

        # Output Frame and Text Widget
        self.output_frame = ttk.Frame(master)
        self.output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.output_text = tk.Text(self.output_frame, height=15)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.output_text.configure(yscrollcommand=self.scrollbar.set)

        # Copyright Notice
        ttk.Label(master, text="Copyright R&D BioTech Alaska", font=('Arial', 8, 'italic')).pack(side=tk.BOTTOM, pady=5)

    def check_ports(self, all_ports):
        ports_input = self.ports_entry.get().strip()
        ports = [int(p.strip()) for p in ports_input.split(',') if p.strip().isdigit()] if ports_input else range(1, 1025)
        if all_ports:
            ports = range(1, 65536)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, f"Checking ports: {', '.join(map(str, ports)) if not all_ports else 'All ports'}\n")
        for port in ports:
            self.check_single_port(port)

    def check_single_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    self.output_text.insert(tk.END, f"Port {port} is open.\n")
                else:
                    self.output_text.insert(tk.END, f"Port {port} is closed.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error checking port {port}: {e}\n")

    def block_port(self):
        ports_input = self.ports_entry.get().strip()
        if ports_input:
            self.output_text.insert(tk.END, f"Blocking port(s): {ports_input}\n")
        else:
            messagebox.showinfo("Block Port", "Please enter a port number to block.")

    def unblock_port(self):
        ports_input = self.ports_entry.get().strip()
        if ports_input:
            self.output_text.insert(tk.END, f"Unblocking port(s): {ports_input}\n")
        else:
            messagebox.showinfo("Unblock Port", "Please enter a port number to unblock.")

    def panic_block(self):
        # Simulated functionality
        messagebox.showinfo("Panic Block", "Simulating a panic block of all ports.")

    def release_ports(self):
        # Simulated functionality
        messagebox.showinfo("Release Ports", "Simulating a release of all ports.")

    def display_system_info(self):
        info = f"System: {platform.system()} {platform.release()}\n"
        info += f"Processor: {platform.processor()}\n"
        messagebox.showinfo("System Information", info)

def main():
    root = tk.Tk()
    app = PortBlocker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
