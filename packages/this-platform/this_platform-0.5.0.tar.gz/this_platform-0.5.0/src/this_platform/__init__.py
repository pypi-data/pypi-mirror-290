from __future__ import annotations

from enum import IntEnum, auto
from functools import cache
from platform import platform
from typing import Final


PLATFORM: Final[str] = platform().casefold()


class Platform(IntEnum):
  LINUX = auto()
  MACOS = auto()
  WINDOWS = auto()
  BSD = auto()
  HAIKU = auto()
  OTHER = auto()

  @staticmethod
  @cache
  def this() -> Platform:
    if Platform.is_linux():
      return Platform.LINUX

    elif Platform.is_macos():
      return Platform.MACOS

    elif Platform.is_windows():
      return Platform.WINDOWS

    elif Platform.is_bsd():
      return Platform.BSD

    elif Platform.is_haiku():
      return Platform.HAIKU

    return Platform.OTHER

  @staticmethod
  @cache
  def is_windows() -> bool:
    return 'windows' in PLATFORM or 'nt' in PLATFORM

  @staticmethod
  @cache
  def is_macos() -> bool:
    return 'mac' in PLATFORM or 'darwin' in PLATFORM

  @staticmethod
  @cache
  def is_linux() -> bool:
    return 'linux' in PLATFORM

  @staticmethod
  @cache
  def is_bsd() -> bool:
    return 'bsd' in PLATFORM or 'illumos' in PLATFORM

  @staticmethod
  @cache
  def is_haiku() -> bool:
    return 'haiku' in PLATFORM

  @staticmethod
  @cache
  def is_unix_like() -> bool:
    return Platform.is_linux() or Platform.is_bsd() or Platform.is_macos()

  @staticmethod
  @cache
  def is_other() -> bool:
    return not (
      Platform.is_windows()
      or Platform.is_macos()
      or Platform.is_linux()
      or Platform.is_bsd()
      or Platform.is_haiku()
    )


def name() -> str:
  return Platform.this().name.casefold()


def main():
  print(name())
