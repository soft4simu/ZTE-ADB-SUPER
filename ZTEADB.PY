import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os, mmap, threading, time

class TurboPatcherV2:
    def __init__(self, root):
        self.root = root
        self.root.title("ZTE ADB SUPER")
        self.root.geometry("650x700")
        self.root.configure(bg="#020202")  # Ultra Black Background

        self.neon = "#39ff14"
        self.owner_phone = "Eddy Mori"

        # --- DATA CONFIG ---
        self.original_hex = "504B030400000000080021082102580390ED276C0000A4D2020013000000416E64726F69644D616E69666573742E786D6CD55D07601DC5D1BEA76AB001378C31068C31B671917BC1186359C51256434F72A158C8926CCB966521C98D5E1D624A68A18592D07B4B42716801FE04082D"
        self.pattern_bytes = bytes.fromhex(self.original_hex)
        self.zero_pattern = bytes([0x00]) * len(self.pattern_bytes)
        self.fill_size = int("21F000", 16)

        # --- TOP HEADER ---
        header_frame = tk.Frame(root, bg="#0a0a0a", height=100)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="ZTE ADB SUPER 2026", font=("Impact", 45), bg="#0a0a0a", fg=self.neon).pack(pady=10)
        tk.Label(header_frame, text="ADB VERSION 2.0 | BLACKMAN V2", font=("Consolas", 10), bg="#0a0a0a", fg="white").pack()

        # --- MAIN CONSOLE AREA ---
        main_frame = tk.Frame(root, bg="#020202")
        main_frame.pack(pady=30, padx=40, fill="both")

        # Digital Percentage
        self.percent_lbl = tk.Label(main_frame, text="0%", font=("Courier New", 80, "bold"), bg="#020202", fg=self.neon)
        self.percent_lbl.pack()

        # Custom Styled Progress Bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Cyber.Horizontal.TProgressbar", thickness=15, troughcolor="#0a0a0a", background=self.neon, bordercolor="#020202", lightcolor=self.neon, darkcolor=self.neon)
        
        self.prog_bar = ttk.Progressbar(main_frame, length=500, mode='determinate', style="Cyber.Horizontal.TProgressbar")
        self.prog_bar.pack(pady=20, fill="x")

        self.status_lbl = tk.Label(main_frame, text="> SYSTEM INITIALIZED", bg="#020202", fg="#00ff00", font=("Consolas", 11))
        self.status_lbl.pack()

        # --- CONTROL BUTTONS ---
        btn_container = tk.Frame(root, bg="#020202")
        btn_container.pack(pady=20)

        button_config = {"font": ("Arial", 10, "bold"), "width": 20, "height": 2, "relief": "flat", "cursor": "hand2"}

        self.btn_browse = tk.Button(btn_container, text="[ SELECT BINARY ]", command=self.browse, bg="#1a1a1a", fg="white", **button_config)
        self.btn_browse.grid(row=0, column=0, padx=10, pady=10)

        self.btn_start = tk.Button(btn_container, text="EXECUTE PATCH", command=lambda: self.run_task("patch"), bg=self.neon, fg="black", **button_config)
        self.btn_start.grid(row=0, column=1, padx=10, pady=10)

        self.btn_restore = tk.Button(btn_container, text="RESTORE SYSTEM", command=lambda: self.run_task("restore"), bg="#0066cc", fg="white", **button_config)
        self.btn_restore.grid(row=1, column=0, padx=10, pady=10)

        self.btn_reset = tk.Button(btn_container, text="RESET CONSOLE", command=self.reset_ui, bg="#cc0000", fg="white", **button_config)
        self.btn_reset.grid(row=1, column=1, padx=10, pady=10)

        # --- FOOTER ---
        footer = tk.Frame(root, bg="#0a0a0a", height=40)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text=f"DEVELOPER: {self.owner_phone} // SECURITY: ENCRYPTED", font=("Consolas", 9), bg="#0a0a0a", fg="#444").pack(pady=10)

        self.file_path = ""

    def browse(self):
        f = filedialog.askopenfilename()
        if f:
            self.file_path = f
            self.reset_ui()
            self.status_lbl.config(text=f"> TARGET LOADED: {os.path.basename(f)}", fg="#00ffff")

    def reset_ui(self):
        self.prog_bar['value'] = 0
        self.percent_lbl.config(text="0%")
        self.status_lbl.config(text="> CONSOLE IDLE", fg="#00ff00")

    def run_task(self, mode):
        if not self.file_path:
            return messagebox.showerror("System Error", "No target binary selected!")
        threading.Thread(target=self.engine, args=(mode,), daemon=True).start()

    def engine(self, mode):
        try:
            with open(self.file_path, "r+b") as f:
                with mmap.mmap(f.fileno(), 0) as mm:
                    
                    if mode == "patch":
                        off = mm.find(self.pattern_bytes)
                        status_msg = "> INJECTING NULL BYTES..."
                        data = bytes([0x00]) * self.fill_size
                    else:
                        off = mm.find(self.zero_pattern)
                        status_msg = "> RECONSTRUCTING ORIGINAL..."
                        data = self.pattern_bytes

                    if off != -1:
                        self.root.after(0, lambda: self.status_lbl.config(text=status_msg, fg="yellow"))
                        mm.seek(off)
                        
                        for i in range(1, 101):
                            time.sleep(0.012) 
                            self.root.after(0, self.update_ui, i)
                            if i == 50: 
                                mm.write(data)
                                mm.flush()
                        
                        self.root.after(0, lambda: self.status_lbl.config(text="> OPERATION SUCCESSFUL", fg=self.neon))
                        messagebox.showinfo("Security Center", f"{mode.upper()} process completed.")
                    else:
                        messagebox.showerror("Pattern Error", "Signature mismatch! File cannot be processed.")
        except Exception as e:
            messagebox.showerror("Kernel Error", str(e))

    def update_ui(self, val):
        self.prog_bar['value'] = val
        self.percent_lbl.config(text=f"{val}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = TurboPatcherV2(root)
    root.mainloop()
