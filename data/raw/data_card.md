# 📊 Data Card – Paris 2024 Olympic Summer Games – Médaillés

## 🗂️ Description
Nom : `Paris 2024 Olympic Medalists`  
Version : `1.0`  
Source : Kaggle - https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games  
Taille : ~3 000 lignes, 13 colonnes  
Résumé : Ce sous-ensemble du dataset des JO de Paris 2024 contient uniquement les athlètes médaillés, avec des informations détaillées sur l’âge au moment de la médaille, le sexe, la discipline, et l’épreuve.

## 🏷️ Variables
| Nom              | Type     | Description                                                    |
|------------------|----------|----------------------------------------------------------------|
| medal_date       | date     | Date officielle de l’attribution de la médaille               |
| medal_code       | int      | Code numérique de la médaille (1 = Or, 2 = Argent, 3 = Bronze) |
| name             | string   | Nom complet de l’athlète                                       |
| gender           | string   | Sexe de l’athlète (“M” ou “F”)                                 |
| country_long     | string   | Nom complet du pays représenté                                 |
| discipline       | string   | Discipline sportive spécifique                                 |
| url_event        | string   | URL ou ID unique de l’épreuve                                  |
| code_athlete     | string   | Identifiant unique de l’athlète                                |
| disciplines      | string   | Nom du sport général (ex. “Natation”)                          |
| birth_date       | date     | Date de naissance de l’athlète                                 |
| age_at_medal     | float    | Âge de l’athlète au moment de l’attribution de la médaille     |

## 🧼 Prétraitement
- Filtrage pour ne conserver que les athlètes médaillés  
- Calcul de `age_at_medal` à partir de `birth_date` et `medal_date`  
- Création de `medal_code` à partir de la médaille (Or = 1, Argent = 2, Bronze = 3)  
- Normalisation des noms de pays (`country_long`) pour les analyses géographiques  
- Jointures internes avec une table d'épreuves pour obtenir `url_event`  

## ⚠️ Limites
- Seuls les athlètes médaillés sont inclus (pas les participants)  
- Les données sont figées à un instant T et peuvent ne pas refléter les mises à jour officielles  

## 🔗 Exemple
```json
{
  "medal_date": "2024-07-28",
  "medal_code": 1,
  "name": "Emma Dubois",
  "gender": "Female",
  "country_long": "France",
  "discipline": "Judo",
  "url_event": "/en/paris-2024/results/cycling-road/men-s-individual-time-trial/fnl-000100--",
  "code_athlete": "1903136",
  "disciplines": ["Judo"],
  "birth_date": "2002-05-11",
  "age_at_medal": 22
}
