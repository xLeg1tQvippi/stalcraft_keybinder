import keyboard as kb
from pynput import mouse
import json
import time
from colorama import Fore, init
import threading

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
        self.running = True # Флаг для работы цикла

    def on_click(self, x, y, button, pressed):
        if not self.active:
            return
    
        if button == mouse.Button.right:
            active_win = str(self.window_manager.get_active_window())
            target_win = self.hotkey_data.get('window', '')
            
            # Используем 'in', так как заголовки окон в играх бывают динамическими
            if target_win in active_win:
                # Оптимальный бинд для Сталкрафта (скрытие интерфейса)
                hotkey = self.hotkey_data.get('action_key', 'f1') 
                # Нажимаем/отпускаем в зависимости от состояния ПКМ
                if pressed:
                    kb.press_and_release(hotkey)
            else:
                # Чтобы не спамить в консоль при каждом клике вне игры
                pass

    def toggle_script(self):
        self.active = not self.active
        status = f"{Fore.GREEN}ВКЛЮЧЕН" if self.active else f"{Fore.RED}ВЫКЛЮЧЕН"
        print(f"Скрипт {status}")

    def stop_script(self):
        self.active = False
        self.running = False
        if self.listener:
            self.listener.stop()
        kb.unhook_all()
        print(f"{Fore.RED}Скрипт остановлен.")

    def run_script(self):
        self.hotkey_data = self.key_binder.load_hotkeys()
        start_key = self.hotkey_data.get('keybind', 'f6')
        quit_key = self.hotkey_data.get('quit_hotkey', 'esc')
        
        print(f"{Fore.GREEN}Скрипт запущен! Нажмите {start_key} для активации.")

        # Запуск мыши в отдельном потоке (daemon=True чтобы не вис при выходе)
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.daemon = True
        self.listener.start() 

        kb.add_hotkey(start_key, self.toggle_script)
        
        # Вместо kb.wait используем цикл, чтобы не вешать программу
        while self.running:
            if kb.is_pressed(quit_key):
                self.stop_script()
                break
            time.sleep(0.1)

    def main_menu(self):
        while True:
            print(f"\n{Fore.WHITE}=== ГЛАВНОЕ МЕНЮ ==={Fore.RESET}")
            print("1. Настроить бинды")
            print("2. Запустить скрипт")
            print("3. Выйти")
            
            choice = input(f"{Fore.CYAN}>>> {Fore.RESET}")
            if choice == "1":
                self.key_binder.main()
            elif choice == "2":
                self.running = True
                self.run_script()
            elif choice == "3":
                break

if __name__ == "__main__":
    runscript = RunScript()
    runscript.main_menu()