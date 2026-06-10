import tkinter as tk
import os
import threading
import time

class CyberdeckTest:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBERDECK TEST OS")
        self.root.geometry("800x480") # 7.2인치 가상 해상도
        self.root.configure(bg="black")
        
        # 타이틀 글자 생성
        self.title = tk.Label(root, text="[ PARADIGM SHIFT PI-TEST ]", 
                              fg="#00FF00", bg="black", font=("Courier", 16, "bold"))
        self.title.pack(pady=20)
        
        # 경고창 생성 (처음엔 빨간색)
        self.status_box = tk.Label(root, text="NO DATA FOUND\n\n[ INSERT USB CARTRIDGE ]", 
                                   fg="#FF3333", bg="#111111", font=("Courier", 14, "bold"),
                                   highlightbackground="#FF3333", highlightthickness=2, width=40, height=8)
        self.status_box.pack(pady=30)

        # 라즈베리 파이의 USB 경로 감지 스레드 시작
        # 사용자 이름(pi)에 맞게 경로를 설정합니다.
        self.usb_path = "/media/pi" 
        self.running = True
        self.check_thread = threading.Thread(target=self.check_usb, daemon=True)
        self.check_thread.start()

    def check_usb(self):
        while self.running:
            # /media/pi 폴더 안에 USB 폴더가 생겼는지 확인
            if os.path.exists(self.usb_path) and os.listdir(self.usb_path):
                # USB가 꽂혔을 때 초록색으로 변경
                self.status_box.config(text="ACCESS GRANTED\n\n[ CARTRIDGE MOUNTED ]", 
                                       fg="#00FF00", highlightbackground="#00FF00")
            else:
                # USB가 없을 때 빨간색으로 변경
                self.status_box.config(text="NO DATA FOUND\n\n[ INSERT USB CARTRIDGE ]", 
                                       fg="#FF3333", highlightbackground="#FF3333")
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberdeckTest(root)
    root.mainloop()
