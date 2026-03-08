import keyboard as kb
from pynput import mouse
import json
from pathlib import Path
import time
from colorama import Fore, init

init(autoreset=True)

class RunScript:
    def __init__(self):
        from window_selector import WindowManager
        from key_binder import SC_KeyBinder
        self.window_manager = WindowManager()
        self.key_binder = SC_KeyBinder()
        self.hotkey_data = {}
        self.listener = None
        self.active = False
        
    def on_click(self, x, y, button, pressed):
        if not self.active:
            return
    
        if button == mouse.Button.right:
            active_win: str = self.window_manager.get_active_window()
            if active_win == self.hotkey_data['window']:
                print("window matches!")
                hotkey = self.hotkey_data.get('action_key', 'ctrl+f1')
                if pressed:
                    print(f"Интерфейс скрыт (Статус: Прицеливание)")
                    kb.press_and_release(hotkey)
                else:
                    kb.press_and_release(hotkey)
                print("Интерфейс открыт обратно (Статус: Прицеливание отменено)")
            else:
                print("windows does not match! script was not activated. Swap to settled window in settings.")

    def toggle_script(self):
        self.active = not self.active
        status = f"{Fore.GREEN}ВКЛЮЧЕН" if self.active else f"{Fore.RED}ВЫКЛЮЧЕН"
        print(f"Скрипт {status}{Fore.RESET}")
        if self.active:
            print("Ожидаем прицеливания (ПКМ).")

    def stop_script(self):
        print(f"\n{Fore.RED}Выход из скрипта...{Fore.RESET}")
        self.active = False
        if self.listener:
            self.listener.stop()
        kb.unhook_all()

    def run_script(self):
        self.hotkey_data = self.key_binder.load_hotkeys()
        start_key = self.hotkey_data.get('keybind', 'f6')
        quit_key = self.hotkey_data.get('quit_hotkey', 'esc')
        
        print(f"{Fore.GREEN}Скрипт активирован!{Fore.RESET}")
        print()
        print(f"{Fore.CYAN}Режим ожидания запуска...{Fore.RESET}")
        print(f"Клавиша запуска/остановки: {Fore.YELLOW}{start_key}{Fore.RESET}")
        print(f"Клавиша выхода: {Fore.RED}{quit_key}{Fore.RESET}")

        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start() 

        kb.add_hotkey(start_key, self.toggle_script)
        
        kb.wait(quit_key)
        self.stop_script()

    def main_menu(self):
        while True:
            print(f"\n{Fore.WHITE}=== ГЛАВНОЕ МЕНЮ ==={Fore.RESET}")
            print("1. Настроить бинды")
            print("2. Запустить скрипт")
            print("3. Выйти из программы")
            
            choice = input(f"{Fore.CYAN}>>> {Fore.RESET}")
            
            if choice == "1":
                self.key_binder.main()
            elif choice == "2":
                self.run_script()
            elif choice == "3":
                break
            else:
                print("Неверный выбор")

if __name__ == "__main__":
    try:
        print('running')
        runner = RunScript()
        runner.main_menu()
    except Exception as error:
        print(error)
