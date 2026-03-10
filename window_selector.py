import pygetwindow as gw
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt

class WindowManager:
    def get_all_windows(self):
        ignored = ['Settings', 'Microsoft Store', 'Program Manager', 'Calculated']
        windows = gw.getAllTitles()
        return sorted([w for w in windows if w.strip() and w not in ignored])

    def get_active_window(self):
        win = gw.getActiveWindowTitle()
        return win if win else ""

    def check_if_inputed_window_is_valid(self, chosen_window: str, window_list: list[str]):
        if any(chosen_window == w for w in window_list):
            return True
        print("(!) Окно не найдено. Выберите из списка автодополнения.")
        return False

    def choose_window_capture(self):
        titles = self.get_all_windows()
        win_completer = WordCompleter(titles, match_middle=True, ignore_case=True)
        
        while True:
            print("\n> Начните вводить название (Tab для списка). '0' для выхода.")
            choice = prompt("Выберите окно: ", completer=win_completer).strip()
            
            if choice == '0': return None
            if self.check_if_inputed_window_is_valid(choice, titles):
                return choice
        
    def main(self):
        return self.choose_window_capture()