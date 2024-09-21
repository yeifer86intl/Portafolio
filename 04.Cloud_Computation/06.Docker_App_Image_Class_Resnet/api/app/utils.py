
import hashlib
import os

def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    # Implement the allowed_file function
    allowed_extensions = {".png", ".jpg", ".jpeg", ".gif"}
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in allowed_extensions

async def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # Read file content and generate md5 hash
    file_content = await file.read()
    file_hash = hashlib.md5(file_content).hexdigest()

    # Return file pointer to the beginning
    await file.seek(0)

    # Get original file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    print("--------------------------------------------")
    print(file_extension)
    print("--------------------------------------------")
    # Return new filename with hash and original extension
    return f"{file_hash}{file_extension}"