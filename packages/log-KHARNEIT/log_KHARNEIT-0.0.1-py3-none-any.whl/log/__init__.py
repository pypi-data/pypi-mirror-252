from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from os import linesep
import time

class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Log(ABC):
    _log_level: LogLevel = LogLevel.NOTSET
    _timer_start: time = time.perf_counter()
    _instance = None
    _file_path: str

    @classmethod
    def reset_timer(cls) -> None:
        cls._timer_start = time.perf_counter()

    @classmethod
    def set_log_level(cls, log_level: LogLevel) -> None:
        cls._log_level = log_level

    @classmethod
    def set_file_path(cls, path: str):
        cls._file_path = path

    @classmethod
    def format(self, msg: str, log_level: LogLevel) -> str:
        datetime_now = datetime.now()
        process_time_str = f"{time.perf_counter() - self._timer_start:0.4f}s"
        datetime_str = f"{datetime_now.strftime('%Y-%m-%d %H:%m:%S')}"
        log_level_str = f"{log_level.name}"

        return f"{datetime_str} - {process_time_str} [{log_level_str}]: {msg}"

    @classmethod
    def log(self, msg: str, log_level: LogLevel) -> None:
        if log_level.value >= self._log_level.value:
            self.__print_log(self.format(msg, log_level))

    @classmethod
    def debug(self, msg: str) -> None:
        self.log(msg, LogLevel.DEBUG)

    @classmethod
    def info(self, msg: str) -> None:
        self.log(msg, LogLevel.INFO)

    @classmethod
    def warning(self, msg: str) -> None:
        self.log(msg, LogLevel.WARNING)

    @classmethod
    def error(self, msg: str) -> None:
        self.log(msg, LogLevel.ERROR)

    @classmethod
    def critical(self, msg: str) -> None:
        self.log(msg, LogLevel.CRITICAL)

    @abstractmethod
    def __print_log(self, msg: str) -> None:
        ...


class ConsoleLog(Log):
    @classmethod
    def _Log__print_log(self, msg: str) -> None:
        print(msg)


class FileLog(Log):
    @classmethod
    def _Log__print_log(cls, msg: str) -> None:
        with open(cls._file_path, 'a') as file:
            file.write(msg + linesep)

class HybridLog(Log):
    @classmethod
    def _Log__print_log(cls, msg: str) -> None:
        ConsoleLog._Log__print_log(msg)
        with open(cls._file_path, 'a', encoding="utf-8") as file:
            file.writelines (msg + linesep)
