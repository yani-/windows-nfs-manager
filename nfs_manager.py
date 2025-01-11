import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import psutil
import wmi
from tkinter.scrolledtext import ScrolledText

class MountSettingsDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Mount Settings")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Settings
        self.settings = {
            "uid": tk.StringVar(value="1000"),
            "gid": tk.StringVar(value="1002"),
            "rsize": tk.StringVar(value="1048576"),
            "wsize": tk.StringVar(value="1048576"),
            "timeout": tk.StringVar(value="0.8"),
            "fileaccess": tk.StringVar(value="755"),
            "casesensitive": tk.BooleanVar(value=False),
            "soft": tk.BooleanVar(value=True)
        }
        
        # Create settings frame
        settings_frame = ttk.LabelFrame(self, text="Mount Settings", padding=10)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # User/Group Settings
        ttk.Label(settings_frame, text="User ID:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(settings_frame, textvariable=self.settings["uid"], width=10).grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(settings_frame, text="Group ID:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(settings_frame, textvariable=self.settings["gid"], width=10).grid(row=1, column=1, sticky="w", pady=5)
        
        # Transfer Settings
        ttk.Label(settings_frame, text="Read Size (bytes):").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(settings_frame, textvariable=self.settings["rsize"], width=10).grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(settings_frame, text="Write Size (bytes):").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(settings_frame, textvariable=self.settings["wsize"], width=10).grid(row=3, column=1, sticky="w", pady=5)
        
        # Connection Settings
        ttk.Label(settings_frame, text="Timeout (seconds):").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Entry(settings_frame, textvariable=self.settings["timeout"], width=10).grid(row=4, column=1, sticky="w", pady=5)
        
        ttk.Label(settings_frame, text="File Access (octal):").grid(row=5, column=0, sticky="w", pady=5)
        ttk.Entry(settings_frame, textvariable=self.settings["fileaccess"], width=10).grid(row=5, column=1, sticky="w", pady=5)
        
        # Checkboxes
        ttk.Checkbutton(settings_frame, text="Soft Mount", variable=self.settings["soft"]).grid(row=6, column=0, columnspan=2, sticky="w", pady=5)
        ttk.Checkbutton(settings_frame, text="Case Sensitive", variable=self.settings["casesensitive"]).grid(row=7, column=0, columnspan=2, sticky="w", pady=5)
        
        # Help text
        help_text = """
Tips:
• User/Group IDs: Match with NFS server permissions
• Transfer Sizes: Larger = better performance (if stable)
• Timeout: Lower = faster reconnect on issues
• File Access: 755 = standard read/write/execute
• Soft Mount: Recommended for better reliability
        """
        help_label = ttk.Label(settings_frame, text=help_text, justify=tk.LEFT, wraplength=350)
        help_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        
    def ok(self):
        self.result = {k: v.get() for k, v in self.settings.items()}
        self.destroy()
        
    def cancel(self):
        self.result = None
        self.destroy()

class NFSManager(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("NFS Drive Manager")
        self.geometry("800x600")
        
        # Mount settings
        self.mount_settings = None
        
        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Mount frame
        mount_frame = ttk.LabelFrame(main_frame, text="Mount NFS Drive")
        mount_frame.pack(fill=tk.X, padx=5, pady=5)

        # Server input
        ttk.Label(mount_frame, text="Server:").grid(row=0, column=0, padx=5, pady=5)
        self.server_entry = ttk.Entry(mount_frame, width=40)
        self.server_entry.grid(row=0, column=1, padx=5, pady=5)

        # Share input
        ttk.Label(mount_frame, text="Share:").grid(row=1, column=0, padx=5, pady=5)
        self.share_entry = ttk.Entry(mount_frame, width=40)
        self.share_entry.grid(row=1, column=1, padx=5, pady=5)

        # Drive letter input
        ttk.Label(mount_frame, text="Drive Letter:").grid(row=2, column=0, padx=5, pady=5)
        self.drive_letter = ttk.Combobox(mount_frame, values=[f"{chr(x)}:" for x in range(67, 91)], width=5)
        self.drive_letter.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Mount buttons frame
        mount_btn_frame = ttk.Frame(mount_frame)
        mount_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Settings button
        self.settings_btn = ttk.Button(mount_btn_frame, text="⚙️ Settings", command=self.show_settings)
        self.settings_btn.pack(side=tk.LEFT, padx=5)

        # Mount button
        self.mount_btn = ttk.Button(mount_btn_frame, text="Mount", command=self.mount_drive)
        self.mount_btn.pack(side=tk.LEFT, padx=5)

        # Mounted drives frame
        drives_frame = ttk.LabelFrame(main_frame, text="Mounted NFS Drives")
        drives_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview for mounted drives
        self.drives_tree = ttk.Treeview(drives_frame, columns=("Drive", "Server", "Share", "Status"), show="headings")
        self.drives_tree.heading("Drive", text="Drive")
        self.drives_tree.heading("Server", text="Server")
        self.drives_tree.heading("Share", text="Share")
        self.drives_tree.heading("Status", text="Status")
        self.drives_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Properties text area
        properties_frame = ttk.LabelFrame(main_frame, text="Drive Properties")
        properties_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.properties_text = ScrolledText(properties_frame, height=6)
        self.properties_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_btn = ttk.Button(btn_frame, text="Refresh", command=self.refresh_drives)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)

        self.unmount_btn = ttk.Button(btn_frame, text="Unmount Selected", command=self.unmount_drive)
        self.unmount_btn.pack(side=tk.LEFT, padx=5)

        # Bind selection event
        self.drives_tree.bind("<<TreeviewSelect>>", self.show_properties)

        # Initial refresh
        self.refresh_drives()

    def show_settings(self):
        dialog = MountSettingsDialog(self)
        self.wait_window(dialog)
        if hasattr(dialog, 'result') and dialog.result is not None:
            self.mount_settings = dialog.result

    def mount_drive(self):
        server = self.server_entry.get()
        share = self.share_entry.get()
        drive = self.drive_letter.get()

        if not all([server, share, drive]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            # Use custom settings if available, otherwise use defaults
            if self.mount_settings is None:
                self.mount_settings = {
                    "uid": "1000",
                    "gid": "1002",
                    "rsize": "1048576",
                    "wsize": "1048576",
                    "timeout": "0.8",
                    "fileaccess": "755",
                    "casesensitive": False,
                    "soft": True
                }

            # Build mount options
            mount_options = [
                "anon",
                f"uid={self.mount_settings['uid']}",
                f"gid={self.mount_settings['gid']}",
                f"rsize={self.mount_settings['rsize']}",
                f"wsize={self.mount_settings['wsize']}",
                f"timeout={self.mount_settings['timeout']}",
                f"fileaccess={self.mount_settings['fileaccess']}",
                "soft" if self.mount_settings['soft'] else "hard",
                "casesensitive=yes" if self.mount_settings['casesensitive'] else "casesensitive=no",
                "retry=1",
                "locking=yes",
                "lang=ANSI",
                "sec=sys"
            ]
            
            cmd = f'mount -o {",".join(mount_options)} {server}:{share} {drive}'
            subprocess.run(cmd, shell=True, check=True)
            messagebox.showinfo("Success", f"Successfully mounted {server}:{share} to {drive}")
            self.refresh_drives()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to mount drive: {str(e)}")

    def unmount_drive(self):
        selected = self.drives_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a drive to unmount")
            return

        drive = self.drives_tree.item(selected[0])['values'][0]
        try:
            cmd = f'umount {drive}'
            subprocess.run(cmd, shell=True, check=True)
            messagebox.showinfo("Success", f"Successfully unmounted {drive}")
            self.refresh_drives()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to unmount drive: {str(e)}")

    def refresh_drives(self):
        # Clear existing items
        for item in self.drives_tree.get_children():
            self.drives_tree.delete(item)

        # Get mounted drives
        c = wmi.WMI()
        for drive in c.Win32_MappedLogicalDisk():
            if drive.ProviderName and drive.ProviderName.startswith('\\\\'):
                self.drives_tree.insert('', 'end', values=(
                    drive.DeviceID,
                    drive.ProviderName.split('\\')[2],
                    '\\'.join(drive.ProviderName.split('\\')[3:]),
                    "Connected"
                ))

    def show_properties(self, event):
        selected = self.drives_tree.selection()
        if not selected:
            return

        drive = self.drives_tree.item(selected[0])['values'][0]
        
        try:
            c = wmi.WMI()
            for disk in c.Win32_MappedLogicalDisk():
                if disk.DeviceID == drive:
                    # Format provider name to be more readable
                    provider = disk.ProviderName.replace('\\\\', '') if disk.ProviderName else 'N/A'
                    
                    properties = "📁 Drive Information:\n"
                    properties += "─" * 30 + "\n"
                    properties += f"💿 Drive Letter:     {disk.DeviceID}\n"
                    properties += f"📂 Server Location:  {provider}\n"
                    properties += f"🔧 File System:      {disk.FileSystem or 'NFS'}\n"
                    
                    # Safely handle size calculations with more readable format
                    try:
                        free_space = float(disk.FreeSpace) / (1024**3) if disk.FreeSpace else 0
                        total_size = float(disk.Size) / (1024**3) if disk.Size else 0
                        used_space = total_size - free_space
                        used_percent = (used_space / total_size * 100) if total_size > 0 else 0
                        
                        properties += "\n💾 Storage Usage:\n"
                        properties += "─" * 30 + "\n"
                        properties += f"Total Space:       {total_size:.1f} GB\n"
                        properties += f"Used Space:        {used_space:.1f} GB ({used_percent:.1f}%)\n"
                        properties += f"Free Space:        {free_space:.1f} GB\n"
                    except (TypeError, ValueError):
                        properties += "\n💾 Storage Usage:    Unable to calculate\n"
                    
                    properties += "\n🔒 Mount Settings:\n"
                    properties += "─" * 30 + "\n"
                    properties += "• User ID:          1000\n"
                    properties += "• Group ID:         1002\n"
                    properties += "• Transfer Size:    1MB (optimized)\n"
                    properties += "• Connection:       Soft mount\n"
                    properties += "• Timeout:          0.8 seconds\n"
                    properties += "• File Access:      Read/Write\n"
                    properties += "• Case Sensitive:   No\n"
                    
                    self.properties_text.delete(1.0, tk.END)
                    self.properties_text.insert(tk.END, properties)
                    break
        except Exception as e:
            self.properties_text.delete(1.0, tk.END)
            self.properties_text.insert(tk.END, "⚠️ Unable to retrieve drive properties")
            print(f"Error getting drive properties: {str(e)}")  # For debugging

if __name__ == "__main__":
    app = NFSManager()
    app.mainloop() 