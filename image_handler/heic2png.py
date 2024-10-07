import pillow_heif
from PIL import Image
from pathlib import Path
import mimetypes
from typing import Union, Optional

def is_heic(path) -> bool:
    """
    Checks if a given file path corresponds to a HEIC image format.

    Args:
        path (Union[str, Path]): The path to the file. Can be provided as a string or a Path object.

    Returns:
        bool: Returns True if the file is a HEIC image, otherwise returns False.
               If an error occurs (e.g., invalid path), it returns False.

    Example:
        >>> is_heic("example_image.heic")
        True

        >>> is_heic(Path("example_image.jpg"))
        False

    This function checks the MIME type of the file based on the file extension and determines
    whether it is in HEIC format (High-Efficiency Image Format used by Apple).
    
    If the path is provided as a Path object, it is converted to a string before checking the MIME type.
    """
    try:
        if isinstance(path, Path):
            path = str(path)
            
        return mimetypes.guess_type(path)[0] == "image/heic"
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
def heic2png(file_path: Union[str, Path], keep_original: bool = True) -> Optional[Path]:
    """
    Converts a HEIC image file to PNG format.

    Args:
        file_path (Union[str, Path]): Path to the HEIC image file.
        keep_original (bool): If False, the original HEIC file will be deleted after conversion.
                              Defaults to True, meaning the original HEIC file will be kept.

    Returns:
        Optional[Path]: The path to the converted PNG file if successful, None if an error occurs.

    Example:
        >>> heic2png("example_image.heic")
        PosixPath('example_image.png')

        >>> heic2png("example_image.heic", keep_original=False)
        PosixPath('example_image.png')

    This function reads a HEIC file, converts it to PNG format using the Pillow library, and saves it
    with the same name but with a `.png` extension in the same directory.

    If the input file path is provided as a string, it is converted to a `Path` object for easier handling.

    If `keep_original` is set to False, the original HEIC file is deleted after conversion.
    """
    try:
        if isinstance(file_path, str):
            file_path = Path(file_path)

        heif_file = pillow_heif.read_heif(file_path)
        image = Image.frombytes(
            mode=heif_file.mode, size=heif_file.size, data=heif_file.data
        )

        png_file_path = file_path.with_suffix(".png")
        image.save(png_file_path, "PNG")
        
        if keep_original == False:
            file_path.unlink()
            
        return png_file_path

    except Exception as e:
        print(f"Error: {str(e)}")
        return None