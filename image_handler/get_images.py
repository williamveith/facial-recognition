import mimetypes
from pathlib import Path
from typing import List, Union

def is_image(path) -> bool:
    """
    Checks if a given file path corresponds to an image file based on its MIME type.

    Args:
        path (Union[str, Path]): The path to the file. Can be provided as a string or a Path object.

    Returns:
        bool: Returns True if the file is an image, otherwise returns False. If an error occurs,
              such as an invalid path or MIME type detection failure, it returns False.

    Example:
        >>> is_image("example_image.jpg")
        True

        >>> is_image(Path("example_document.pdf"))
        False

    This function checks the MIME type of the file based on its extension and determines whether
    it belongs to the "image" category (e.g., "image/jpeg", "image/png", etc.).
    
    If the path is provided as a Path object, it is converted to a string before checking the MIME type.
    If an exception occurs (e.g., invalid path or MIME type issue), the function catches the exception and returns False.
    """
    try:
        if isinstance(path, Path):
            path = str(path)
        
        mimetype = mimetypes.guess_type(path)[0]
        
        if mimetype is not None:
            return mimetypes.guess_type(path)[0].split('/')[0] == "image"
        else:
            return False

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def get_images(path: Union[str, Path]) -> List[Path]:
    """
    Retrieves all image files from a given directory or a single image file.

    Args:
        path (Union[str, Path]): The path to a directory or a file. Can be provided as a string or a Path object.

    Returns:
        List[Path]: A list of Path objects representing the image files found. 
                    If a directory is provided, it recursively searches for images in that directory.
                    If a single file is provided and it is an image, it returns a list with just that image.
                    If no images are found, an empty list is returned.

    Example:
        >>> get_images("path_to_directory")
        [PosixPath('path_to_directory/image1.jpg'), PosixPath('path_to_directory/image2.png')]

        >>> get_images("path_to_directory/single_image.jpg")
        [PosixPath('path_to_directory/single_image.jpg')]

        >>> get_images("path_to_directory/non_image.txt")
        []

    This function checks if the provided path is a directory or a single file. If it's a directory, 
    it recursively searches for all image files within the directory and its subdirectories.
    If the provided path is a single file, it checks if the file is an image and, if so, adds it to the result list.
    """
    if isinstance(path, str):
        path = Path(path)
    
    images = []
    
    if path.is_dir():
        images.extend(filter(lambda file_path: is_image(file_path), path.rglob("*")))
    elif path.is_file():
        if is_image(path):
            images.append(path)
    else:
        print("No images found")
    
    return images