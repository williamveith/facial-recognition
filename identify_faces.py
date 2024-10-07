from deepface import DeepFace
from image_handler import get_image_files
from represent_faces import get_vector

def get_identity(img_path, db_path, detector_backend="retinaface", model_name='ArcFace', distance_metric="cosine"):
    try:
        return DeepFace.find(
            img_path=img_path,
            db_path=db_path, 
            model_name=model_name,
            distance_metric=distance_metric,
            detector_backend=detector_backend
        )
        
    except Exception as e:
        return f"Error: {str(e)}"

database_path = "/Users/main/Projects/Docker/faces/database"
images = get_image_files("/Users/main/Projects/Docker/faces/0.png")[0]
vector = get_vector(images)
result = DeepFace.find(img_path = images, db_path = database_path)
# result = get_identity(images, database_path)
# print(result)