# ADE Scolaire - EILCO

Application web de consultation d'emploi du temps scolaire inspirée d'ADE Campus, développée dans le cadre du module **Méthodologies Agiles** (EILCO - ING2 S7).

🌐 **Version en ligne :** [https://akisch01.github.io/ADE_SCOLAIRE/](https://akisch01.github.io/ADE_SCOLAIRE/)

---

## 📌 Fonctionnalités

- **Vue hebdomadaire :** Grille du lundi au vendredi avec créneaux de 08h00 à 19h00.
- **Filtrage par niveau :** Changement dynamique d'emploi du temps (CP1, CP2, ING1, ING2, ING3).
- **Calcul automatique des dates :** Affichage des dates réelles de la semaine en cours avec boutons de navigation (semaine précédente / suivante).
- **Gestion des créneaux :** Fusion visuelle automatique des cours de 2h (`rowspan`) et affichage de la pause déjeuner (12h15 - 13h15).
- **Base de données locale :** Chargement initial depuis `cours.json` et gestion via `LocalStorage`.

---

## 🛠️ Technologies utilisées

- **Front-end :** HTML5, CSS3, JavaScript (Vanilla ES6)
- **Données :** JSON, Web Storage API (LocalStorage)
- **Conteneurisation :** Docker, Nginx Alpine, Docker Compose
- **CI/CD :** GitHub Actions (Vérification syntaxe JSON, test de build Docker, déploiement automatique sur GitHub Pages)

---

## 🚀 Comment lancer le projet ?

### Option 1 : Directement dans le navigateur
Ouvrez simplement le fichier `index.html` dans votre navigateur web.

### Option 2 : Avec Docker (Recommandé pour les tests)
Pour tester l'application dans un environnement de production Nginx :

```bash
# Lancer le conteneur
docker compose up -d
```

L'application sera accessible sur : **http://localhost:8080**

Pour arrêter le conteneur :
```bash
docker compose down
```

---

## 👥 Équipe Dev projet

- Akisch AKPO
- Noah BROUART
- Hajar BRECH