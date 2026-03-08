import keyboard as kb
import json
from pathlib import Path
import time
from colorama import Fore, init

init(autoreset=True)

class SC_KeyBinder:
    def __init__(self):
        from window_selector import WindowManager
        self.window_manager = WindowManager()
        self.data_dir = Path(__file__).parent / "keybind_data"
        self.data_dir.mkdir(exist_ok=True)
        self.key_bind_data_path = self.data_dir / "key_binds.json"
        self._init_db()

    def _init_db(self):
        if not self.key_bind_data_path.exists():
            with open(self.key_bind_data_path, 'w', encoding='utf-8') as f:
                json.dump({"window": "None", "keybind": "None", "quit_hotkey": "None"}, f)

    def is_hotkey_valid(self, hotkey: str) -> bool:
        if not hotkey: return False
        try:
            kb.parse_hotkey(hotkey)
            return True
        except ValueError:
            return False

    def load_hotkeys(self) -> dict:
        with open(self.key_bind_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_hotkey(self, window: str, hotkey: str, quit_key: str):
        data = {"window": window, "keybind": hotkey, "quit_hotkey": quit_key}
        with open(self.key_bind_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=True)

    def capture_hotkey(self, label: str):
        while True:
            print(label)
            print()
            
            print(f"(?){Fore.CYAN} (Нажимайте на клавиатуре сочетание клавиш.){Fore.RESET}\n(>) {Fore.LIGHTCYAN_EX}Нажмите на {Fore.LIGHTGREEN_EX}'SPACE|ПРОБЕЛ'{Fore.LIGHTCYAN_EX} чтобы сохранить бинд.{Fore.RESET}")
            print(f"(>) {Fore.LIGHTWHITE_EX}Слушаем нажатия...{Fore.RESET}")
            
            while kb.is_pressed('space') or kb.is_pressed('enter'):
                time.sleep(0.1)
                
            recorded = kb.record(until='space')
            names = [e.name for e in recorded if e.event_type == 'down' and e.name not in ['space', 'enter']]
            hotkey = "+".join(list(dict.fromkeys(names)))
            
            if self.is_hotkey_valid(hotkey):
                print(f"Бинд: {hotkey} успешно создан.")
                save_bind = input("Сохранить?\n1 - Да\n2 - Нет\n>>> ")
                if save_bind.strip() == "1":
                    return hotkey
                
            else:
                print("Бинд не прошёл проверку. Повторите попытку.")
                continue
            
    def create_new_binds(self):
        target_window = self.window_manager.main()
        if not target_window: return

        start_key = self.capture_hotkey(f"(>){Fore.YELLOW} Привязка {Fore.GREEN}запуска{Fore.YELLOW} скрипта.")
        if not start_key:
            print(f"{Fore.RED}Ошибка валидации.{Fore.RESET}")
            return

        quit_key = self.capture_hotkey(f"(>) {Fore.YELLOW}Привязка {Fore.RED}выхода{Fore.YELLOW} скрипта.")
        if not quit_key:
            print(f"{Fore.RED}Ошибка валидации.{Fore.RESET}")
            return
        
        print(f"Данные:\nЗапуск: {start_key}\nВыход: {quit_key}")
        confirm = input(f"Сохранить? (1 - Да, 2 - Нет): ")
        if confirm == "1":
            self.write_hotkey(target_window, start_key, quit_key)
            print(f"{Fore.GREEN}Сохранено!{Fore.RESET}")

    def show_current_binds(self):
        data = self.load_hotkeys()
        print(f"\n{Fore.LIGHTMAGENTA_EX}--- ТЕКУЩИЕ НАСТРОЙКИ ---{Fore.RESET}")
        print(f"Окно: {Fore.GREEN}{data.get('window')}{Fore.RESET}")
        print(f"Запуск: {Fore.YELLOW}{data.get('keybind')}{Fore.RESET}")
        print(f"Выход: {Fore.RED}{data.get('quit_hotkey')}{Fore.RESET}")
        input("\nНажмите Enter чтобы вернуться...")

    def main(self):
        while True:
            print(f"\n{Fore.WHITE}=== KEYBINDER MENU ==={Fore.RESET}")
            print("1. Показать текущие бинды и окно")
            print("2. Создать новые бинды")
            print("3. Выход")
            
            choice = input(f"{Fore.CYAN}>>> {Fore.RESET}")
            
            if choice == "1":
                self.show_current_binds()
            elif choice == "2":
                self.create_new_binds()
            elif choice == "3":
                break
            else:
                print("Неверный ввод")

if __name__ == "__main__":
    app = SC_KeyBinder()
    app.main()
