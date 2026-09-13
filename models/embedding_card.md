# 🧬 Embedding Card – `skin_color_embedding_v1`

## 🧾 Description
Vecteur 128D représentant la couleur dominante de la peau d’un individu extrait via modèle CNN.

## ⚙️ Détails
- Dimension : 128
- Méthode : ResNet50 + couche FC
- Données d’entrée : image du visage
- Données de sortie : vecteur `[0.12, 0.45, ..., 0.87]`

## 🧪 Données d'entraînement
- Dataset : `color_faces_dataset v1.0`
- Échantillons : 2 500
- Split : 80/20

## 📏 Performances
| Metric   | Value |
|----------|-------|
| Accuracy | 83%   |
| F1-score | 0.81  |

## 📆 Version
- Date d'entraînement : 2025-07-02

## 📦 Exemple d’usage
```python
embedding = model.extract_embedding(image_path="user001.jpg")
```

## ⚠️ Limites
- Perturbé par des maquillages / filtres
- Sensible à l’éclairage
