from . import get_images
from . import heic2png
from pathlib import Path
from typing import List, Union
from itertools import combinations

def get_image_files(path: Union[str, Path]) -> List[Path]:
    """
    Retrieves and converts image files from the given directory or single file path.

    Args:
        path (Union[str, Path]): The path to a directory or a file. This can be either a string 
                                 or a Path object. The path may contain image files of various formats, 
                                 including HEIC.

    Returns:
        List[Path]: A list of Path objects representing image files. HEIC files are converted to PNG format
                    before being added to the list. Other image files are added directly. 
                    The HEIC files are deleted after conversion if `keep_original=False`.

    Example:
        >>> get_image_files("path_to_directory")
        [PosixPath('path_to_directory/image1.jpg'), PosixPath('path_to_directory/image2.png'), PosixPath('path_to_directory/image3.png')]

        >>> get_image_files("path_to_directory/single_image.heic")
        [PosixPath('path_to_directory/single_image.png')]

    Description:
    - This function retrieves all image files from the provided path (which can be a directory or a single file).
    - If any HEIC images are found, they are converted to PNG using the `heic2png` module and added to the list of compatible images.
    - If `keep_original=False`, the original HEIC file is deleted after conversion.
    - Other image files (JPEG, PNG, etc.) are added directly to the list without modification.
    - The function returns a list of all compatible image files, ensuring that HEIC images are converted to PNG.
    """
    images = get_images.get_images(path)
    compatible_images = []
    
    for image in images:
        if heic2png.is_heic(image):
            compatible_images.append(heic2png.heic2png(file_path=image, keep_original=False))
        else:
            compatible_images.append(image)
    
    return compatible_images

def pairwise_comparison(images, callback):
    output = []
    for img1, img2 in combinations(images, 2):
        print(f"Running: {callback.__name__} | On: {img1.name}, {img2.name}...")
        try:
            output.append({
                "images": [img1.name, img2.name],
                "result": callback(img1, img2)
                })
        except Exception as e:
            print(f"Error comparing {img1.name} and {img2.name}: {str(e)}")
    
    return output