# 📈 Résultats – Analyse des modèles

## 🎯 Objectif
Comparer plusieurs architectures pour la classification colorimétrique

## 🧪 Modèles testés

| Modèle          | Accuracy | F1-score | Notes                            |
|-----------------|----------|----------|----------------------------------|
| SVM             | 72%      | 0.69     | Simple mais peu flexible         |
| Random Forest   | 78%      | 0.74     | Bonne baseline                   |
| MLP (final)     | **83%**  | **0.81** | Choisi pour déploiement          |

## 🖼️ Visualisations
- Confusion matrix : `results/visualizations/cm_final.png`
- Embeddings (TSNE) : `results/visualizations/tsne_plot.png`
