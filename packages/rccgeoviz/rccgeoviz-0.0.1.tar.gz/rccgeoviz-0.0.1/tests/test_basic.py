import pytest
from rccgeoviz.geoviz_cli import main


def test_sysargs():
    main(["--options", "jello"])
