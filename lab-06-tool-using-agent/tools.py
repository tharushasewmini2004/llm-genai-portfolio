"""Tools for the Lab 6 agent. Each function decorated with @tool can be called by the LLM."""
import ast
import ctypes
import datetime
import operator
import os
import platform
import subprocess
import time

from langchain_core.tools import tool

# ---------- safe maths ----------
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Only numbers and + - * / ** % are allowed")


def clean_expression(text):
    """Turn 25 x 4 / 25 × 4 / 10 ÷ 2 / 2^3 into a Python expression."""
    return (text.replace("×", "*").replace("x", "*").replace("X", "*")
                .replace("÷", "/").replace("^", "**").replace(",", "").strip())


def calculate(expression):
    return _eval(ast.parse(clean_expression(expression), mode="eval").body)


def _type_into_calculator(expression):
    """Open Windows Calculator and type the sum, so the user can watch it work."""
    import pyautogui
    import pygetwindow as gw
    subprocess.Popen("calc.exe")
    time.sleep(2.5)
    try:
        wins = gw.getWindowsWithTitle("Calculator")
        if wins:
            wins[0].activate()
            time.sleep(0.5)
    except Exception:
        pass
    pyautogui.write(expression.replace(" ", ""), interval=0.15)
    pyautogui.press("enter")


@tool
def calculator(expression: str) -> str:
    """Open the Windows Calculator and calculate a maths expression. Only use this when the user asks to calculate numbers."""
    try:
        result = calculate(expression)
    except Exception as e:
        return f"Could not calculate '{expression}': {e}"
    try:
        _type_into_calculator(clean_expression(expression))
    except Exception as e:  # the answer is still correct even if the GUI part fails
        return f"{expression} = {result} (could not drive the Calculator window: {e})"
    return f"{expression} = {result}"


# ---------- exercise tools ----------
@tool
def get_date_time() -> str:
    """Get the current date and time."""
    return datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


@tool
def open_notepad(text: str) -> str:
    """Open Windows Notepad and write the given text into it."""
    import pyautogui
    subprocess.Popen("notepad.exe")
    time.sleep(2)
    pyautogui.write(text, interval=0.05)
    return f"Opened Notepad and wrote: {text}"


@tool
def file_search(directory: str, name_or_extension: str) -> str:
    """Search a directory for files by name or extension, for example directory 'D:\\MSC AI' and '.pdf'."""
    if not os.path.isdir(directory):
        return f"Directory not found: {directory}"
    key = name_or_extension.lower().lstrip("*")
    found = []
    for root, _, files in os.walk(directory):
        for f in files:
            if key in f.lower():
                found.append(os.path.join(root, f))
            if len(found) >= 50:
                break
    if not found:
        return f"No files matching '{name_or_extension}' in {directory}"
    return f"Found {len(found)} file(s):\n" + "\n".join(found)


@tool
def create_file(path: str, content: str) -> str:
    """Create a text file at the given path with the given content, for example path 'D:\\MSC AI\\test.txt'."""
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Created {path}"
    except Exception as e:
        return f"Could not create the file: {e}"


class _MemStatus(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]


@tool
def system_info() -> str:
    """Get the operating system, processor and memory (RAM) information of this computer."""
    info = [f"OS: {platform.system()} {platform.release()} ({platform.version()})",
            f"Processor: {platform.processor()}",
            f"CPU cores: {os.cpu_count()}"]
    try:
        m = _MemStatus()
        m.dwLength = ctypes.sizeof(_MemStatus)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        info.append(f"Memory: {m.ullTotalPhys / 1024**3:.1f} GB total, {m.ullAvailPhys / 1024**3:.1f} GB free")
    except Exception:
        info.append("Memory: not available on this system")
    return "\n".join(info)
