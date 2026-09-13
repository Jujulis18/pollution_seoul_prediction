# 🧠 Model Card – `SkinToneClassifier_v1`

## 📋 Objectif
Classifier une personne dans l’une des 12 catégories de typologie colorimétrique à partir d’un embedding visage.

## ⚙️ Détails techniques
- Type : Classificateur MLP
- Entrée : vecteur embedding (128D)
- Sortie : classe (`light_summer`, `deep_autumn`, etc.)

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
