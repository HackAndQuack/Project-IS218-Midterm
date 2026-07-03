########################
# Logger                #
########################

import logging
from pathlib import Path


class Logger:
    """
    Centralized logging access point for the calculator application.

    Wraps a single named `logging.Logger` so every module logs through one
    consistent configuration instead of calling the root `logging` module
    directly. `configure()` sets up the file handler/format/level once
    (normally from `Calculator._setup_logging`); every other module just
    calls `Logger.info/warning/error(...)`.
    """

    _logger = logging.getLogger("calculator")

    @classmethod
    def configure(cls, log_file: Path, level: int = logging.INFO) -> None:
        """
        Configure logging to write to the given file.

        Args:
            log_file (Path): Path to the log file.
            level (int, optional): Logging level. Defaults to logging.INFO.
        """
        logging.basicConfig(
            filename=str(log_file),
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True  # Overwrite any existing logging configuration
        )

    @classmethod
    def info(cls, message: str) -> None:
        """Log an informational message."""
        cls._logger.info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """Log a warning message."""
        cls._logger.warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        """Log an error message."""
        cls._logger.error(message)
