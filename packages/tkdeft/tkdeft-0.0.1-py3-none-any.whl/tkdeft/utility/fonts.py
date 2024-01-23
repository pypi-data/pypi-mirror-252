from os.path import abspath, dirname, join

path = abspath(dirname(__file__))

segoefont = join(path, "segoe_font.ttf")


def SegoeFont():
    from _tkinter import TclError
    try:
        from tkextrafont import Font
        font = Font(file=segoefont, size=10, family="Segoe UI", weight="normal")
    except TclError:
        try:
            from tkinter.font import Font
            font = Font(size=10, family="Segoe UI", weight="normal")
        except TclError:
            from tkinter.font import nametofont
            font = nametofont("TkDefaultFont").configure(size=10)
    return font
