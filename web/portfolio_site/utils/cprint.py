"""This module is to print console with color.
"""
class ColorPrint():
    """Static class to print console with color.
    """
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

    @staticmethod
    def print(msg:str, color:str):
        """print console with color.

        Args:
            msg (str): message to print on the console.
            color (str): color. Constants are prepared.
        """
        print(ColorPrint.raw(msg, color))

    @staticmethod
    def raw(msg:str, color:str):
        """get raw string with color.

        Args:
            msg (str): message to print on the console.
            color (str): color. Constants are prepared.
        Returns:
            str: a raw string with color codes.
        """
        return color + msg + ColorPrint.END
