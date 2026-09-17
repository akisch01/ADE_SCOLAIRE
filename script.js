/**
 * Gestion de l'emploi du temps ADE Scolaire - EILCO
 * Base de données chargée directement depuis cours.json et stockée dans LocalStorage
 */

const STORAGE_KEY = 'ade_cours_db';

// Ordre des créneaux horaires
const CRENEAUX_ORDRE = [
    "08h00",
    "09h00",
    "10h15",
    "11h15",
    "12h15", // Pause déjeuner
    "13h15",
    "14h15",
    "15h30",
    "16h30",
    "17h30"
];

// Mapping jour -> index de colonne dans le tableau HTML
const MAPPING_JOURS = {
    "Lundi": 1,
    "Mardi": 2,
    "Mercredi": 3,
    "Jeudi": 4,
    "Vendredi": 5
};

let niveauActuel = "ING2";
let lundiActuel = obtenirLundi(new Date());

/**
 * Calcule le lundi de la semaine courante
 * @param {Date} date 
 * @returns {Date}
 */
function obtenirLundi(date) {
    const lundi = new Date(date);
    const jour = lundi.getDay();
    const joursDepuisLundi = jour === 0 ? 6 : jour - 1;
    lundi.setHours(0, 0, 0, 0);
    lundi.setDate(lundi.getDate() - joursDepuisLundi);
    return lundi;
}

/**
 * Formate une date au format YYYY-MM-DD
 * @param {Date} date 
 * @returns {string}
 */
function formaterDate(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

/**
 * Calcule la date exacte d'un jour donné de la semaine en cours
 * @param {Date} lundi 
 * @param {string} jourNom 
 * @returns {string}
 */
function obtenirDateDuJour(lundi, jourNom) {
    const indexJour = Object.keys(MAPPING_JOURS).indexOf(jourNom);
    const date = new Date(lundi);
    date.setDate(date.getDate() + indexJour);
    return formaterDate(date);
}

/**
 * Met à jour l'affichage des dates dans les en-têtes des colonnes
 */
function mettreAJourDatesSemaine() {
    Object.keys(MAPPING_JOURS).forEach((jourNom, index) => {
        const date = new Date(lundiActuel);
        date.setDate(date.getDate() + index);
        const element = document.getElementById(jourNom.toLowerCase());
        if (element) {
            element.textContent = `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}`;
        }
    });
}

/**
 * Navigation entre les semaines (+1 ou -1)
 * @param {number} nombreDeSemaines 
 */
function changerDeSemaine(nombreDeSemaines) {
    lundiActuel.setDate(lundiActuel.getDate() + nombreDeSemaines * 7);
    mettreAJourDatesSemaine();
    afficherEmploiDuTemps(niveauActuel);
}

/**
 * Initialise la base de données LocalStorage à partir du fichier cours.json
 */
async function initialiserBaseDeDonnees() {
    try {
        const reponse = await fetch('cours.json');
        if (!reponse.ok) throw new Error("Erreur de chargement du fichier cours.json");
        const cours = await reponse.json();
        sauvegarderTousLesCours(cours);
        console.log("Base de données initialisée depuis cours.json (total : " + cours.length + " cours).");
    } catch (error) {
        console.error("Erreur lors de l'initialisation de la base :", error);
    }
}

/**
 * Récupère tous les cours stockés dans le LocalStorage
 * @returns {Array}
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
 * Récupère un cours par son identifiant unique
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
    afficherEmploiDuTemps(niveauActuel);
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
        afficherEmploiDuTemps(niveauActuel);
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
    afficherEmploiDuTemps(niveauActuel);
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
 * Remplit les cellules du tableau HTML existant avec les cours filtrés par niveau
 * @param {string} niveau Niveau sélectionné (CP1, CP2, ING1, ING2, ING3)
 */
function afficherEmploiDuTemps(niveau = niveauActuel) {
    niveauActuel = niveau;

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

    // 2. Récupérer et filtrer les cours selon le niveau sélectionné
    const tousLesCours = getTousLesCours();
    const listeCours = tousLesCours.filter(c => {
        if (c.niveau) {
            if (c.niveau.toUpperCase() !== niveau.toUpperCase()) return false;
        } else if (c.groupe) {
            if (!c.groupe.toUpperCase().startsWith(niveau.toUpperCase())) return false;
        } else {
            return false;
        }

        const dateCours = obtenirDateDuJour(lundiActuel, c.jour);

        // Les cours génériques sans date restent visibles sur la semaine courante
        if (!c.date) {
            return formaterDate(lundiActuel) === formaterDate(obtenirLundi(new Date()));
        }

        return c.date === dateCours;
    });

    // 3. Remplir chaque cours filtré dans sa case correspondante
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

/**
 * Initialisation des boutons de sélection de niveau (CP1, CP2, ING1, ING2, ING3)
 */
function initialiserBoutonsNiveaux() {
    const boutonsNiveau = document.querySelectorAll('.level-button');

    boutonsNiveau.forEach(bouton => {
        bouton.addEventListener('click', () => {
            boutonsNiveau.forEach(element => {
                element.classList.remove('active');
            });

            bouton.classList.add('active');
            const niveau = bouton.textContent.trim();
            afficherEmploiDuTemps(niveau);
        });
    });

    const boutonActif = document.querySelector('.level-button.active');
    if (boutonActif) {
        niveauActuel = boutonActif.textContent.trim();
    }
}

/**
 * Initialisation des boutons de navigation entre les semaines
 */
function initialiserNavigationSemaines() {
    document.getElementById('semaine-suivante')?.addEventListener('click', () => {
        changerDeSemaine(1);
    });

    document.getElementById('semaine-precedente')?.addEventListener('click', () => {
        changerDeSemaine(-1);
    });
}

// Initialisation générale au chargement du DOM
document.addEventListener('DOMContentLoaded', async () => {
    await initialiserBaseDeDonnees();
    initialiserBoutonsNiveaux();
    initialiserNavigationSemaines();
    mettreAJourDatesSemaine();
    afficherEmploiDuTemps(niveauActuel);
});
