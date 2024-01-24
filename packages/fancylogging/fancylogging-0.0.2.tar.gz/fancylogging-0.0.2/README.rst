Fancy Logging
====================

Introduction
------------

This Python module provides an advanced logging setup using `rich` for
console logging and `python-json-logger` for file logging. It allows for
detailed and formatted logging, ideal for applications requiring high-level
logging capabilities.

Installation
------------
This module requires the following dependencies:

* `rich <https://pypi.org/project/rich/>`_
* `python-json-logger <https://pypi.org/project/python-json-logger/>`_

Usage
-----
Import `setup_fancy_logging` from the module and configure your logging setup
by specifying parameters like `base_logger_name`, `console_log_level`,
`file_log_level`, `log_file_path`, and others.

Example:

.. code-block:: python3

  from fancy_logging import setup_fancy_logging

  setup_fancy_logging(
      base_logger_name="myapp",
      console_log_level="DEBUG",
      file_log_level="DEBUG",
      log_file_path="myapp.log",
  )
