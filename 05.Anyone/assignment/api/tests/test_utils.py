import os
from io import BytesIO

import app.utils as utils
import pytest
from fastapi import UploadFile
from werkzeug.datastructures import FileStorage


def test_allowed_file():
    assert utils.allowed_file("cat.JPG")
    assert utils.allowed_file("cat.jpeg")
    assert utils.allowed_file("cat.JPEG")
    assert utils.allowed_file("../../car.PNG")
    assert utils.allowed_file("/usr/var/src/car.gif")

    assert not utils.allowed_file("cat.JPGG")
    assert not utils.allowed_file("invoice.pdf")
    assert not utils.allowed_file("/usr/src/slides.odt")
    assert not utils.allowed_file("/usr/src/api")
    assert not utils.allowed_file("/usr/src/api/")
    assert not utils.allowed_file("/usr/src/dog.")
    assert not utils.allowed_file("/usr/src/dog./")


@pytest.mark.asyncio
async def test_get_file_hash():
    filename = "tests/dog.jpeg"
    md5_filename = "0a7c757a80f2c5b13fa7a2a47a683593.jpeg"
    with open(filename, "rb") as fp:
        file = FileStorage(fp)
        file = UploadFile(file=BytesIO(file.read()), filename="dog.jpeg")

    new_filename = await utils.get_file_hash(file)

    assert md5_filename == new_filename
