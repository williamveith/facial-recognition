from deepface import DeepFace
from image_handler import get_image_files
import json

def analyze_face(image_path, detector_backend="retinaface", enforce_detection=True):
    return DeepFace.analyze(
            img_path=image_path,
            detector_backend=detector_backend, 
            enforce_detection=enforce_detection
    )

images = get_image_files("/Users/main/Projects/Docker/faces/test_images")

for image in images:
    results = analyze_face(image)
    print(f"File: {image.name}")
    print(json.dumps(results, indent=4, sort_keys=True))