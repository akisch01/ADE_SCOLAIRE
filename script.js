/**
 * Gestion de la base de données des cours (LocalStorage + cours.json)
 * Projet : ADE Scolaire - EILCO
 */

const STORAGE_KEY = 'ade_cours_db';

// Ordre des créneaux horaires
const CRENEAUX_ORDRE = [
    "08h00",
    "09h00",
    "10h15",
    "11h15",
    "12h15", // Pause
    "13h15",
    "14h15",
    "15h30",
    "16h30",
    "17h30"
];

// Mapping jour -> index de colonne dans les <tr> (0 = hour-cell, 1 = Lundi, ...)
const MAPPING_JOURS = {
    "Lundi": 1,
    "Mardi": 2,
    "Mercredi": 3,
    "Jeudi": 4,
    "Vendredi": 5
};

/**
 * Initialise la base de données dans le LocalStorage
 */
async function initialiserBaseDeDonnees() {
    const dataExistante = localStorage.getItem(STORAGE_KEY);
    
    if (!dataExistante) {
        try {
            const reponse = await fetch('cours.json');
            if (!reponse.ok) throw new Error("Erreur réseau");
            const cours = await reponse.json();
            sauvegarderTousLesCours(cours);
            console.log("BD initialisée depuis cours.json :", cours);
        } catch (error) {
            console.warn("Chargement direct du JSON impossible (ex: protocole file://), utilisation des données de secours.");
            sauvegarderTousLesCours(COURS_DEFAUT);
        }
    } else {
        console.log("BD chargée depuis le LocalStorage.");
    }
}

/**
 * Récupère tous les cours stockés dans le LocalStorage
 * @returns {Array} Liste des cours
 */
function getTousLesCours() {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
}

/**
 * Sauvegarde la liste complète des cours dans le LocalStorage
 * @param {Array} cours 
 */
function sauvegarderTousLesCours(cours) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cours));
}

/**
 * Récupère un cours par son ID
 * @param {number} id 
 * @returns {Object|null}
 */
function getCoursParId(id) {
    const cours = getTousLesCours();
    return cours.find(c => c.id === Number(id)) || null;
}

/**
 * Ajoute un nouveau cours dans la base
 * @param {Object} nouveauCours 
 */
function ajouterCours(nouveauCours) {
    const cours = getTousLesCours();
    nouveauCours.id = nouveauCours.id || Date.now();
    cours.push(nouveauCours);
    sauvegarderTousLesCours(cours);
    afficherEmploiDuTemps();
    return nouveauCours;
}

/**
 * Met à jour un cours existant
 * @param {number} id 
 * @param {Object} donneesModifiees 
 */
function modifierCours(id, donneesModifiees) {
    let cours = getTousLesCours();
    const index = cours.findIndex(c => c.id === Number(id));
    if (index !== -1) {
        cours[index] = { ...cours[index], ...donneesModifiees };
        sauvegarderTousLesCours(cours);
        afficherEmploiDuTemps();
        return cours[index];
    }
    return null;
}

/**
 * Supprime un cours par son ID
 * @param {number} id 
 */
function supprimerCours(id) {
    let cours = getTousLesCours();
    cours = cours.filter(c => c.id !== Number(id));
    sauvegarderTousLesCours(cours);
    afficherEmploiDuTemps();
}

/**
 * Réinitialise la base de données avec les données par défaut
 */
function reinitialiserBaseDeDonnees() {
    localStorage.removeItem(STORAGE_KEY);
    sauvegarderTousLesCours(COURS_DEFAUT);
    afficherEmploiDuTemps();
}

/**
 * Calcule le nombre de créneaux (rowspan) qu'occupe un cours
 * @param {string} heureDebut 
 * @param {string} heureFin 
 * @returns {number} Nombre de créneaux
 */
function calculerRowspan(heureDebut, heureFin) {
    const start = parseInt(heureDebut.replace('h', ''), 10);
    const end = parseInt(heureFin.replace('h', ''), 10);
    const dureeHeures = end - start;

    return dureeHeures >= 2 ? 2 : 1;
}

/**
 * Remplit les cellules du tableau HTML existant avec les cours du LocalStorage
 */
function afficherEmploiDuTemps() {
    const rows = document.querySelectorAll('#calendar-body tr');
    if (!rows || rows.length === 0) return;

    // 1. Réinitialiser toutes les cellules existantes
    rows.forEach(row => {
        if (row.classList.contains('pause-row')) return;

        const cells = row.querySelectorAll('td:not(.hour-cell)');
        cells.forEach(td => {
            td.innerHTML = '';
            td.removeAttribute('rowspan');
            td.style.display = ''; // Réaffiche la case si elle avait été masquée
        });
    });

    // 2. Récupérer les cours
    const listeCours = getTousLesCours();

    // 3. Remplir chaque cours dans sa case correspondante
    listeCours.forEach(cours => {
        const jourIndex = MAPPING_JOURS[cours.jour];
        if (!jourIndex) return;

        const rowDebut = document.querySelector(`#calendar-body tr[data-heure="${cours.heureDebut}"]`);
        if (!rowDebut) return;

        const cellDebut = rowDebut.children[jourIndex];
        if (!cellDebut) return;

        const rowspan = calculerRowspan(cours.heureDebut, cours.heureFin);

        // Si le cours fait 2h ou plus, appliquer le rowspan et masquer la cellule du dessous
        if (rowspan > 1) {
            cellDebut.setAttribute('rowspan', rowspan);

            let nextRow = rowDebut.nextElementSibling;
            for (let r = 1; r < rowspan; r++) {
                if (nextRow && !nextRow.classList.contains('pause-row')) {
                    const cellToHide = nextRow.children[jourIndex];
                    if (cellToHide) {
                        cellToHide.style.display = 'none';
                    }
                    nextRow = nextRow.nextElementSibling;
                }
            }
        }

        // Insérer la carte du cours
        const card = document.createElement('div');
        card.className = 'cours-card';
        if (cours.couleur) {
            card.style.backgroundColor = cours.couleur;
        }

        card.innerHTML = `
            <div>
                <div class="cours-card-header">
                    <span class="cours-badge">${cours.type || 'COURS'}</span>
                    <span class="cours-horaire">${cours.heureDebut} - ${cours.heureFin}</span>
                </div>
                <div class="cours-matiere">${cours.matiere}</div>
            </div>
            <div class="cours-infos">
                <span>${cours.salle ? cours.salle : ''}</span>
                <span>${cours.enseignant ? cours.enseignant : ''}</span>
            </div>
        `;

        cellDebut.appendChild(card);
    });
}

const boutonsNiveau = document.querySelectorAll('.level-button');

boutonsNiveau.forEach(bouton => {
    bouton.addEventListener('click', () => {
        boutonsNiveau.forEach(element => {
            element.classList.remove('active');
        });

        bouton.classList.add('active');
    });
});s
// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    await initialiserBaseDeDonnees();
    afficherEmploiDuTemps();
});
