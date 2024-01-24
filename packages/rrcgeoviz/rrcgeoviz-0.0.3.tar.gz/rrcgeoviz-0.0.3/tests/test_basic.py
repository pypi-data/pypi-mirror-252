import pytest
from rrcgeoviz.geoviz_cli import main


def test_sysargs():
    main(["--options", "jello"])
