from .human import HumanBehaviorSimulator
from .stealth import StealthToolkit
import urllib.request
import urllib.error
import subprocess
import pychrome
import platform
import shutil
import time
import json
import os

_original_recv_loop = pychrome.Tab._recv_loop

def _safe_recv_loop(self):
    try:
        _original_recv_loop(self)
    except json.decoder.JSONDecodeError:
        pass

pychrome.Tab._recv_loop = _safe_recv_loop


class Zealium:
    def __init__(self,
                 browser="chrome",
                 chrome_path=None,
                 remote_debugging_port=9222,
                 user_data_dir=None,
                 lang="en-US",
                 window_size="1280,800",
                 speed_threshold=1.0,
                 stealth_level="normal",
                 timeout=15,
                 stealth_custom_methods=None):

        if browser not in ("chrome", "edge"):
            raise ValueError(f"Browser '{browser}' not supported. Use 'chrome' or 'edge'.")

        self.browser_choice = browser
        self.remote_debugging_port = remote_debugging_port
        self.lang = lang
        self.window_size = window_size
        self.speed_threshold = speed_threshold
        self.chrome_proc = None
        self.browser = None
        self.tab = None
        self.human = None
        self.stealth_level = stealth_level
        self.timeout = timeout
        self.stealth_custom_methods = stealth_custom_methods or []

        system = platform.system()
        home = os.path.expanduser("~")

        browser_exec_paths = {
            "Windows": {
                "chrome": [
                    os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Google\\Chrome\\Application\\chrome.exe"),
                    os.path.join(os.environ.get("PROGRAMFILES", ""), "Google\\Chrome\\Application\\chrome.exe"),
                    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google\\Chrome\\Application\\chrome.exe")
                ],
                "edge": [
                    os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Microsoft\\Edge\\Application\\msedge.exe"),
                    os.path.join(os.environ.get("PROGRAMFILES", ""), "Microsoft\\Edge\\Application\\msedge.exe"),
                    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft\\Edge\\Application\\msedge.exe")
                ]
            },
            "Darwin": {
                "chrome": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
                "edge": ["/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
            },
            "Linux": {
                "chrome": [shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser")],
                "edge": [shutil.which("microsoft-edge"), shutil.which("microsoft-edge-dev")]
            }
        }

        profile_base_dirs = {
            "Windows": lambda b: os.path.join(
                os.environ.get("USERPROFILE", ""),
                "AppData", "Local",
                "Google" if b == "chrome" else "Microsoft",
                b.capitalize(), "User Data", "BotProfile"
            ),
            "Darwin": lambda b: os.path.join(
                home, "Library", "Application Support",
                "Google" if b == "chrome" else "Microsoft",
                b.capitalize(), "BotProfile"
            ),
            "Linux": lambda b: os.path.join(home, f".{b}-bot-profile")
        }

        if system not in browser_exec_paths or system not in profile_base_dirs:
            raise EnvironmentError(f"OS not supported: {system}")

        exec_candidates = browser_exec_paths[system][browser]
        self.chrome_path = chrome_path or next((p for p in exec_candidates if p and os.path.isfile(p)), None)

        if not self.chrome_path:
            raise FileNotFoundError(f"{browser.capitalize()} not found on system {system}")

        if system == "Windows" and not os.environ.get("USERPROFILE"):
            raise EnvironmentError("Env Variable USERPROFILE not found")
        self.user_data_dir = user_data_dir or profile_base_dirs[system](browser)

        self.stealth_toolkit = None

    def await_proc(self, timeout=15, interval=0.5):
        start = time.time()
        url = f"http://127.0.0.1:{self.remote_debugging_port}/json/version"

        while True:
            try:
                with urllib.request.urlopen(url, timeout=timeout) as response:
                    if response.status == 200:
                        return True
            except urllib.error.URLError as e:

                if isinstance(e.reason, ConnectionRefusedError):
                    pass
                else:
                    raise
            except Exception as e:
                raise e

            if time.time() - start > timeout:
                raise TimeoutError(f"{self.browser_choice.capitalize()} DevTools without response after {timeout}s")
            time.sleep(interval)

    def launch(self):
        flags = [
            self.chrome_path,
            f"--remote-debugging-port={self.remote_debugging_port}",
            f"--user-data-dir={self.user_data_dir}_{self.remote_debugging_port}",
            "--no-first-run",
            "--disable-extensions",
            f"--lang={self.lang}",
            f"--window-size={self.window_size}",
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]

        self.chrome_proc = subprocess.Popen(flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.await_proc(self.timeout)

        self.browser = pychrome.Browser(url=f"http://127.0.0.1:{self.remote_debugging_port}")
        self.tab = self._get_active_tab()
        self.tab.start()

        self.human = HumanBehaviorSimulator(self.tab, speed_factor=self.speed_threshold)

        self.stealth_toolkit = StealthToolkit(
            tab=self.tab,
            level=self.stealth_level,
            custom_methods=self.stealth_custom_methods
        )
        self.stealth_toolkit.apply()

    def _get_active_tab(self):
        tabs = self.browser.list_tab()
        if not tabs:
            raise Exception("No tab on browser detected")
        return tabs[0]

    def close(self):
        if self.tab:
            self.tab.stop()
        if self.chrome_proc:
            self.chrome_proc.terminate()
            self.chrome_proc.wait()
