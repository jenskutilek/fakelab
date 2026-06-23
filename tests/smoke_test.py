from unittest import TestCase

from FL.cmdline import FontLab5Console, environment


class SmokeTest(TestCase):
    def test_init(self) -> None:
        console = FontLab5Console(
            locals=environment,
            # local_exit=True,  # Python 3.13+
        )
        # console.push("import sys\nsys.exit(0)")  # Python 3.13+
