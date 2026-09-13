# utils/vision_tools.py
import numpy as np
from PIL import Image
import streamlit as st
from ultralytics import YOLO

# Charger le modèle YOLOv8 (pré-entraîné COCO)
yolo_model = YOLO("yolov8n.pt")  # modèle léger nano → rapide sur CPU


def compare_images(img1_path, img2_path, min_area=500, threshold=50):
    # Load images
    object1 = detect_objects_yolo(Image.open(img1_path))
    object2 = detect_objects_yolo(Image.open(img2_path))
    if len(object1) != len(object2):
        # get the different on list of objects
        diff = list(set(object1) - set(object2)) + list(set(object2) - set(object1))
        return True, diff
    else:
        return False, "Aucun changement détecté."



def detect_objects_yolo(image: Image.Image):
    """
    Detecte les objets dans une image PIL et retourne les labels détectés.
    """
    # Convertir PIL en array numpy
    img_array = np.array(image)

    # Faire la détection
    results = yolo_model(img_array)

    # Récupérer les labels détectés
    labels = []
    for result in results:
        for cls_id in result.boxes.cls:
            labels.append(yolo_model.names[int(cls_id)])

    return labels
