from typing import Any, Callable, List, Union

import csv
import logging
from logging.handlers import RotatingFileHandler

"""
Module Overview:

This module defines a custom logger class, `Logger`, designed to log attributes
from class instances to a CSV file. It extends the `logging.Logger` class.

Key Class:

- `Logger`: Logs attributes of class instances to a CSV file. It supports
setting different logging levels for file and stream handlers.

Usage Guide:

1. Create an instance of the `Logger` class.
2. Optionally, set the logging levels for file and stream handlers using
   `set_file_level` and `set_stream_level` methods.
3. Add class instances and attributes to log using the `add_attributes` method.
4. Start logging data using the `update` method.
5. Optionally, close the CSV file using the `close` method.

Note:

This file is referenced by the OSL class and is instantiated manually when an OSL
is instantiated.

"""


class Logger(logging.Logger):
    """
    Logger class is a class that logs attributes from a class to a csv file

    Methods:
        __init__(self, container: object, file_path: str, logger: logging.Logger = None) -> None
        log(self) -> None
    """

    def __init__(
        self,
        file_path: str = "./osl",
        log_format: str = "[%(asctime)s] %(levelname)s: %(message)s",
    ) -> None:

        self._file_path: str = file_path + ".log"

        self._containers: list[Union[object, dict[Any, Any]]] = []
        self._container_names: list[str] = []
        self._attributes: list[list[str]] = []

        self._file = open(file_path + ".csv", "w", newline="")
        self._writer = csv.writer(self._file)

        self._log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        super().__init__(__name__)
        self.setLevel(logging.DEBUG)

        self._std_formatter = logging.Formatter(log_format)

        self._file_handler = RotatingFileHandler(
            filename=self._file_path,
            mode="w",
            maxBytes=0,
            backupCount=10,
        )
        self._file_handler.setLevel(level=logging.DEBUG)
        self._file_handler.setFormatter(fmt=self._std_formatter)

        self._stream_handler = logging.StreamHandler()
        self._stream_handler.setLevel(level=logging.INFO)
        self._stream_handler.setFormatter(fmt=self._std_formatter)

        self.addHandler(hdlr=self._stream_handler)
        self.addHandler(hdlr=self._file_handler)

        self._is_logging = False

        self._header_data: list[str] = []
        self._data: list[Any] = []

    def __repr__(self) -> str:
        return f"Logger"

    def set_file_level(self, level: str = "DEBUG") -> None:
        """
        Sets the level of the logger

        Args:
            level (str): Level of the logger
        """
        if level not in self._log_levels.keys():
            self.warning(msg=f"Invalid logging level: {level}")

        self._file_handler.setLevel(level=self._log_levels[level])

    def set_stream_level(self, level: str = "INFO") -> None:
        """
        Sets the level of the logger

        Args:
            level (str): Level of the logger
        """
        if level not in self._log_levels.keys():
            self.warning(msg=f"Invalid logging level: {level}")

        self._stream_handler.setLevel(level=self._log_levels[level])

    def add_attributes(
        self,
        container: Union[object, dict[Any, Any]],
        attributes: list[str],
        container_name: str = None,
    ) -> None:
        """
        Adds class instance and attributes to log

        Args:
            container (object, dict): Container can either be an object (instance of a class)
                or a Dict containing the attributes to be logged.
            attributes (list[str]): List of attributes to log
            container_name (str): An alternative name for the container that you want to be used in the log.
                                  Otherwise, the class's __repr__() method is used.
        """
        if container_name is None:
            if type(container) is dict:
                if "__main__" in container.values():
                    self._container_names.append("")
                else:
                    self._container_names.append(f"{container}:")
            else:
                if type(container).__repr__ is not object.__repr__:
                    self._container_names.append(f"{container}:")
                else:
                    self._container_names.append(f"")
        else:
            self._container_names.append(container_name + ":")

        self._containers.append(container)
        self._attributes.append(attributes)

    def update(self) -> None:
        """
        Logs the attributes of the class instance to the csv file
        """
        if not self._containers:
            return

        if not self._is_logging:
            for container, attributes, container_name in zip(
                self._containers, self._attributes, self._container_names
            ):
                for attribute in attributes:
                    self._header_data.append(container_name + f"{attribute}")

            self._writer.writerow(self._header_data)
            self._is_logging = True

        for container, attributes in zip(self._containers, self._attributes):
            if isinstance(container, dict):
                for attribute in attributes:
                    self._data.append(container.get(attribute))
            else:
                for attribute in attributes:
                    self._data.append(getattr(container, attribute))

        self._writer.writerow(self._data)

        self._data.clear()
        self._header_data.clear()
        self._file.flush()

    def __del__(self) -> None:
        """
        Closes the file when the object is deleted
        """
        self._file.close()


if __name__ == "__main__":
    local_logger = Logger(file_path="./test_log")
    local_variable_1 = 100
    local_variable_2 = 101200

    class SimpleClass:
        def __init__(self):
            self.a = 1
            self.b = 2
            self.c = 3

        def __repr__(self) -> str:
            return f"SimpleClass"

    simple_class = SimpleClass()

    local_logger.add_attributes(locals(), ["local_variable_1"])
    local_logger.add_attributes(locals(), ["local_variable_2"], "custom_container")
    local_logger.add_attributes(simple_class, ["a", "b", "c"])
    local_logger.update()
