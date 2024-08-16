from inspect import currentframe, getframeinfo
from colorama import Fore, Back
from datetime import datetime
import re
import pathlib



class Logging:

    def __init__(self):

        self.clr_err = Fore.RED
        self.clr_warn = Fore.LIGHTYELLOW_EX
        self.clr_succ = Fore.LIGHTGREEN_EX
        self.clr_cyan = Fore.CYAN
        self.clr_magenta = Fore.MAGENTA






    def print(self, txt: str, fore_color: Fore = None, end: str = None, is_remove_prev: bool = False):

        frameinfo = getframeinfo(currentframe().f_back)
        filename = re.split(r"[/|\\]", frameinfo.filename)[-1]
        linenumber = frameinfo.lineno
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        txt = txt.replace('Completed', f'{self.clr_succ}Completed{self.clr_succ}')


        str_prefix = f"{Fore.BLACK}{Back.WHITE}{now}{Back.RESET} {Fore.BLUE}{filename}:{linenumber}{Fore.RESET}"
        str_suffix = f"{fore_color if fore_color else ""}{txt}{Fore.RESET}"

        str_content = f"{'\r' if is_remove_prev else ''}{str_prefix} {str_suffix}"

        if end is None:
            print(str_content)
        else:
            if end == '\n':
                print(f'\r{str_content}')
            else:
                print(f'\r{str_content}', end=end)










    # import inspect
    # @staticmethod
    # def print_link(*, txt, file=None, line=None):
    #     """ Print a link in PyCharm to a line in file.
    #         Defaults to line where this function was called. """
    #
    #     if file is None:
    #         file = inspect.stack()[1].filename
    #
    #     if line is None:
    #         line = inspect.stack()[1].lineno
    #
    #     str_out = f'File "{file}", line {max(line, 1)}'.replace("\\", "/")
    #
    #     # str_out = f"{txt} {Fore.LIGHTBLACK_EX}(file: {file}, line: {max(line, 1)}){Fore.RESET}"
    #
    #     print(str_out)

