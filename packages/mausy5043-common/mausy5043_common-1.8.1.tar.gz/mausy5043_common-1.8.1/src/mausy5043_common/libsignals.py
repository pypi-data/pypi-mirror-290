#!/usr/bin/env python3

"""Provide a class to intercept signals."""

# TODO: migrate to https://pypi.org/project/GracefulKiller/

import signal
import warnings

warnings.warn("This module is deprecated. Use https://pypi.org/project/GracefulKiller/ instead.")


class GracefulKiller:  # pylint: disable=R0903
    """A class to intercept kill signals."""

    kill_now = False

    def __init__(self) -> None:
        """Set-up signals to intercept."""
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame) -> None:  # pylint: disable=W0613
        """Intercept signals and set the state appropriately.

        Args:
            signum: n/a
            frame: n/a
        """
        self.kill_now = True
