import subprocess
import os
import sys
import time
import ctypes
from ctypes import wintypes

def set_dark_mode(window_title):
    """Windowsのタイトルバーをダークモードに強制設定する"""
    # ウィンドウが見つかるまで少し待つ
    for _ in range(20):
        hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
        if hwnd:
            # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            # これを設定することで、Windows 10/11の白いタイトルバーを黒くできます
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 
                DWMWA_USE_IMMERSIVE_DARK_MODE, 
                ctypes.byref(value), 
                ctypes.sizeof(value)
            )
            # 再描画を促す
            ctypes.windll.user32.ShowWindow(hwnd, 5) # SW_SHOW
            return True
        time.sleep(0.5)
    return False

def launch():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    editor_path = os.path.join(current_dir, "index.html")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    
    chrome_exe = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_exe = path
            break
            
    if not chrome_exe:
        return

    # アプリモードで起動
    # ウィンドウタイトルを確定させるために index.html の <title> と一致させる必要があります
    cmd = [chrome_exe, f"--app=file:///{editor_path}", "--window-size=1280,850"]
    subprocess.Popen(cmd)
    
    # タイトルバーの色を黒く染める処理を実行
    # Solid Square Editor は HTML内の <title> タグに依存します
    set_dark_mode("Solid Square Editor")

if __name__ == "__main__":
    launch()
