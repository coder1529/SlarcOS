import tkinter as tk
import os
import threading
import time
import psutil

class CyberdeckShell:
    def __init__(self, root):
        self.root = root
        
        # 화면 전체화면 레이아웃 설정
        self.root.overrideredirect(True) 
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg="black") 
        self.root.config(cursor="none")

        # 시스템 루프 종료 안전장치 (ESC 누르면 종료)
        self.root.bind("<Escape>", lambda e: self.shutdown())

        self.running = True

        # 🚀 [오프닝 미션] 켜지자마자 부팅 연출 화면 먼저 만들기
        self.boot_frame = tk.Frame(root, bg="black")
        self.boot_frame.pack(expand=True, fill="both")
        
        self.boot_text = tk.Text(self.boot_frame, bg="black", fg="#00FF00", font=("Courier", 11), borderwidth=0, highlightthickness=0)
        self.boot_text.pack(expand=True, fill="both", padx=50, pady=50)

        # 백그라운드 스레드에서 부팅 연출 시퀀스 가동
        self.boot_thread = threading.Thread(target=self.run_boot_sequence, daemon=True)
        self.boot_thread.start()

    def run_boot_sequence(self):
        # SF 영화 스타일의 가상 커널 부팅 로그 리스트
        logs = [
            "SLARCOS KERNEL v1.0.4-RELEASE (gcc version 13.2.0)",
            "CPU: ARM Cortex-A76 (r1p4) architecture detected at 2.40GHz",
            "MEM: Total Physical Memory Synchronized: 8,192 MB",
            "STORAGE: NVMe Slide-Deck hardware mapping established at address 0x3F004000",
            "GPIO: Pogo-Pin magnetic interconnect serial driver loaded.",
            "DISPLAY: 7.2-inch High-Density panel calibration... [ OK ]",
            "NETWORK: Intercepting local area network frequencies...",
            "SECURITY: Firewall bypass protocol: INACTIVE (Standby Mode)",
            "CRITICAL: System cartridge signature corrupted or missing.",
            "BOOT_STAGE_2: Handing over control to custom shell interface...\n",
            "LOADING SLARCOS DASHBOARD INTERFACE..."
        ]

        for log in logs:
            if not self.running: return
            # 한 줄씩 화면에 파파팍 출력하는 효과
            self.boot_text.insert(tk.END, f"[  OK  ] {log}\n")
            self.boot_text.see(tk.END) # 스크롤을 맨 아래로 내림
            time.sleep(0.12) # 줄 간격 딜레이 (취향에 맞게 수정 가능)

        time.sleep(0.5) # 마지막 로딩 후 잠깐 멈추는 간지 연출

        # 부팅 화면을 파괴하고 메인 대시보드를 그리는 함수 호출 (메인 스레드에서 실행)
        self.root.after(0, self.load_main_dashboard)

    def load_main_dashboard(self):
        # 부팅 연출 프레임 제거
        self.boot_frame.destroy()

        # 1. 상단 시스템 상태 표시줄 생성
        self.top_bar = tk.Frame(self.root, bg="#050505", height=30)
        self.top_bar.pack(fill="x", side="top")
        
        self.sys_title = tk.Label(self.top_bar, text=" PARADIGM SHIFT OS v1.0", fg="#00FF00", bg="#050505", font=("Courier", 10, "bold"))
        self.sys_title.pack(side="left", padx=10)
        
        self.pogo_status = tk.Label(self.top_bar, text="[ POGO-KEYBOARD: ACTIVE ] ", fg="#00AA00", bg="#050505", font=("Courier", 10))
        self.pogo_status.pack(side="right", padx=10)

        # 2. 메인 워크스페이스 프레임 생성
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(expand=True, fill="both")

        # 📊 [좌측 대시보드]
        self.left_panel = tk.Frame(self.main_frame, bg="black", width=200)
        self.left_panel.pack(side="left", fill="y", padx=30, pady=50)
        self.cpu_title = tk.Label(self.left_panel, text="--- CPU CORE ---", fg="#00AA00", bg="black", font=("Courier", 12, "bold"))
        self.cpu_title.pack(anchor="w")
        self.cpu_label = tk.Label(self.left_panel, text="USAGE: 00.0%", fg="#00FF00", bg="black", font=("Courier", 11))
        self.cpu_label.pack(anchor="w", pady=5)
        
        self.cpu_bar_bg = tk.Frame(self.left_panel, bg="#111111", width=150, height=15, highlightbackground="#00AA00", highlightthickness=1)
        self.cpu_bar_bg.pack_propagate(False)
        self.cpu_bar_bg.pack(anchor="w", pady=5)
        self.cpu_bar = tk.Frame(self.cpu_bar_bg, bg="#00FF00", width=0, height=15)
        self.cpu_bar.pack(side="left")

        # 🔋 [우측 대시보드]
        self.right_panel = tk.Frame(self.main_frame, bg="black", width=200)
        self.right_panel.pack(side="right", fill="y", padx=30, pady=50)
        self.bat_title = tk.Label(self.right_panel, text="--- POWER SYS ---", fg="#00AA00", bg="black", font=("Courier", 12, "bold"))
        self.bat_title.pack(anchor="e")
        self.bat_label = tk.Label(self.right_panel, text="BATTERY: 100%", fg="#00FF00", bg="black", font=("Courier", 11))
        self.bat_label.pack(anchor="e", pady=5)
        
        self.bat_bar_bg = tk.Frame(self.right_panel, bg="#111111", width=150, height=15, highlightbackground="#00AA00", highlightthickness=1)
        self.bat_bar_bg.pack_propagate(False)
        self.bat_bar_bg.pack(anchor="e", pady=5)
        self.bat_bar = tk.Frame(self.bat_bar_bg, bg="#00FF00", width=150, height=15)
        self.bat_bar.pack(side="left")

        # 📼 [중앙 대시보드] 거대 경고 박스
        self.alert_box = tk.Label(self.main_frame, 
                                  text="CRITICAL: NO SYSTEM CARTRIDGE FOUND\n\n[ PLEASE INSERT SSD TO SLIDE-DECK ]", 
                                  fg="#FF3333", bg="#100505", font=("Courier", 14, "bold"),
                                  highlightbackground="#FF3333", highlightthickness=2,
                                  width=42, height=8)
        self.alert_box.pack(expand=True, side="left")

        # 3. 하단 로그 터미널 생성
        self.bottom_bar = tk.Frame(self.root, bg="#020202", height=40)
        self.bottom_bar.pack(fill="x", side="bottom")
        self.log_label = tk.Label(self.bottom_bar, text="[BOOT] Kernel linked. Monitoring hardware registers...", fg="#555555", bg="#020202", font=("Courier", 9))
        self.log_label.pack(side="left", padx=10, pady=5)

        # 진짜 하드웨어 데이터 감시 스레드 가동
        self.monitor_thread = threading.Thread(target=self.hardware_monitor, daemon=True)
        self.monitor_thread.start()

    def hardware_monitor(self):
        while self.running:
            cpu_usage = psutil.cpu_percent()
            battery = psutil.sensors_battery()
            bat_percent = battery.percent if battery else 100
            
            self.cpu_label.config(text=f"USAGE: {cpu_usage:.1f}%")
            self.cpu_bar.config(width=int(150 * (cpu_usage / 100)))
            self.bat_label.config(text=f"BATTERY: {int(bat_percent)}%")
            self.bat_bar.config(width=int(150 * (bat_percent / 100)))

            # 라즈베리 파이 타깃 감지 (맥북 가상 드라이브 예외 처리 포함)
            usb_mounted = False
            if os.path.exists("/Volumes"):
                drives = os.listdir("/Volumes")
                system_drives = ["Macintosh HD", "Recovery", "VM", "Preboot", "Update"]
                real_usbs = [d for d in drives if d not in system_drives and not d.startswith("Macintosh HD")]
                if len(real_usbs) > 0: usb_mounted = True
            elif os.path.exists("/media/pi"):
                if os.listdir("/media/pi"): usb_mounted = True

            if usb_mounted:
                self.alert_box.config(text="ACCESS GRANTED\n\n[ SYSTEM CARTRIDGE MOUNTED SUCCESSFULLY ]", fg="#00FF00", bg="#051005", highlightbackground="#00FF00")
                self.log_label.config(text="[SYS] NVMe SSD Slide-Deck active. Synchronizing system blocks...", fg="#00FF00")
            else:
                self.alert_box.config(text="CRITICAL: NO SYSTEM CARTRIDGE FOUND\n\n[ PLEASE INSERT SSD TO SLIDE-DECK ]", fg="#FF3333", bg="#100505", highlightbackground="#FF3333")
                self.log_label.config(text="[WARN] Hardware link severed. System locked. Awaiting cartridge...", fg="#FF3333")
            
            time.sleep(0.5)

    def shutdown(self):
        self.running = False
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberdeckShell(root)
    root.mainloop()
