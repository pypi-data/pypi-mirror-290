import datetime
import random
import MainShortcuts.os as m_os
import os
import sys
from typing import *
# Универсальные команды
exit = sys.exit
cd = os.chdir
pwd = os.getcwd
if not hasattr(sys, "MainShortcuts_imports"):
  setattr(sys, "MainShortcuts_imports", [])


def clear_ANSI():
  print("\u001b[2J")


def timedelta(time: Union[int, float, dict]) -> datetime.timedelta:
  if type(time) == dict:
    return datetime.timedelta(**time)
  return datetime.timedelta(seconds=time)


def randfloat(min: float, max: float = None) -> float:
  if max == None:
    max = min
    min = 0
  return min + (random.random() * (max - min))


cls_ANSI = clear_ANSI
# Команды для разных ОС
if m_os.platform == "Windows":  # Windows
  def clear():
    '''Очистить весь текст в терминале (использует "cls")'''
    os.system("cls")
  cls = clear
elif m_os.platform == "Linux":  # Linux
  def clear():
    '''Очистить весь текст в терминале (использует "clear")'''
    os.system("clear")
  cls = clear
elif m_os.platform == "Darwin":  # MacOS
  def clear():
    """На этой ОС функция недоступна. На других очищает весь текст в терминале"""
    raise Exception("This feature is not available on the current operating system")
  cls = clear
else:  # Неизвестный тип
  print("MainShortcuts WARN: Unknown OS \"" + m_os.platform + "\"", file=sys.stderr)
