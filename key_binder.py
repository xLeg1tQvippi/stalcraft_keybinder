import keyboard as kb
import json
import time
from pathlib import Path
from colorama import Fore, init

init(autoreset=True)

class SC_KeyBinder:
    def __init__(self):
        from window_selector import WindowManager
        self.window_manager = WindowManager()
        self.data_path = Path(__file__).parent / "keybind_data" / "key_binds.json"
        self.data_path.parent.mkdir(exist_ok=True)
        self._init_db()

    def _init_db(self):
        if not self.data_path.exists():
            self.write_hotkey("STALCRAFT", "f6", "esc")

    def load_hotkeys(self) -> dict:
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"window": "STALCRAFT", "keybind": "f6", "quit_hotkey": "esc"}

    def write_hotkey(self, window, hotkey, quit_key):
        data = {"window": window, "keybind": hotkey, "quit_hotkey": quit_key, "action_key": "f1"}
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def capture_hotkey(self, label: str):
        print(f"\n{label}")
        print(f"{Fore.CYAN}Нажмите сочетание, затем SPACE для сохранения...{Fore.RESET}")
        
        while kb.read_key() if kb.is_pressed('space') else False: pass
        
        recorded = kb.record(until='space')
        names = []
        for e in recorded:
            if e.event_type == 'down' and e.name not in ['space', 'enter', 'shift']:
                if e.name not in names:
                    names.append(e.name)
        
        res = "+".join(names)
        if res:
            print(f"Записано: {Fore.GREEN}{res}{Fore.RESET}")
            return res
        return None

    def create_new_binds(self):
        target_win = self.window_manager.main()
        if not target_win: return

        time.sleep(0.5)
        start_key = self.capture_hotkey("Привязка запуска/паузы")
        
        time.sleep(0.5)
        quit_key = self.capture_hotkey("Привязка выхода")

        if start_key and quit_key:
            self.write_hotkey(target_win, start_key, quit_key)
            print(f"{Fore.GREEN}Настройки сохранены!{Fore.RESET}")

    def main(self):
        while True:
            print(f"\n{Fore.WHITE}=== НАСТРОЙКИ ==={Fore.RESET}")
            print("1. Показать текущие")
            print("2. Перезаписать")
            print("3. Назад")
            choice = input(">>> ")
            if choice == "1":
                d = self.load_hotkeys()
                print(f"Окно: {d['window']} | Старт: {d['keybind']} | Выход: {d['quit_hotkey']}")
            elif choice == "2":
                self.create_new_binds()
            elif choice == "3":
                break
