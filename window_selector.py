import pygetwindow as gw
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt


class WindowManager:
    def __init__(self):
        pass

    def get_all_windows(self):
        windows: list = gw.getAllTitles()
        return [window for window in windows if window.strip()]

    def get_active_window(self):
        activeWindow = gw.getActiveWindowTitle()
        return activeWindow

    def check_if_inputed_window_is_valid(self, chosen_window: str, window_list: list[str]):
        try:
            if chosen_window in window_list:
                return True
            else:
                raise
        
        except Exception as error:
            print("(!) Введенное окно - не открыто, либо не существует. Повторите попытку.")
            return False

    def choose_window_capture(self):
        win_completer: list[str] = WordCompleter(self.get_all_windows(), match_middle=True, ignore_case=True, sentence=True)
        while True:
            choose_win_to_capture: str = prompt("> Введите '0' чтобы выйти из меню.\nВыберите приложение для захвата комбинации:\n>>> ", completer=win_completer)
            if choose_win_to_capture.strip() == '0':
                print("(>) Выходим из меню выбора окон.")
                return
            
            if self.check_if_inputed_window_is_valid(chosen_window=choose_win_to_capture, window_list=self.get_all_windows()):
                return choose_win_to_capture
            
            else:
                continue
        
    def main(self):
        win_to_capture: str = self.choose_window_capture()
        return win_to_capture
        
if __name__ == "__main__":
    winmanager = WindowManager()
    winmanager.main()