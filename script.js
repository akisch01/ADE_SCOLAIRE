/**
 * Gestion de la base de données des cours (LocalStorage + cours.json)
 * Support du filtrage par niveau (CP1, CP2, ING1, ING2, ING3)
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

// Données par défaut pour tous les niveaux
const COURS_DEFAUT = [
    // --- CP1 ---
    {
        id: 101,
        matiere: "Mathématiques : Algèbre",
        enseignant: "M. Legrand",
        salle: "Salle CP1",
        jour: "Lundi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "CM",
        niveau: "CP1",
        groupe: "CP1-A",
        couleur: "#2b6cb0"
    },
    {
        id: 102,
        matiere: "Physique : Mécanique",
        enseignant: "Mme. Renard",
        salle: "Amphi B",
        jour: "Lundi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TD",
        niveau: "CP1",
        groupe: "CP1-A",
        couleur: "#319795"
    },
    {
        id: 103,
        matiere: "Initiation Algorithmique",
        enseignant: "M. Robert",
        salle: "Labo Info 1",
        jour: "Mardi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TP",
        niveau: "CP1",
        groupe: "CP1-A",
        couleur: "#dd6b20"
    },
    {
        id: 104,
        matiere: "Chimie Générale",
        enseignant: "Mme. Simon",
        salle: "Labo Chimie",
        jour: "Mercredi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TP",
        niveau: "CP1",
        groupe: "CP1-A",
        couleur: "#d69e2e"
    },
    {
        id: 105,
        matiere: "Anglais LV1",
        enseignant: "Mme. Smith",
        salle: "Salle C102",
        jour: "Jeudi",
        heureDebut: "13h15",
        heureFin: "15h15",
        type: "TD",
        niveau: "CP1",
        groupe: "CP1-A",
        couleur: "#805ad5"
    },
    {
        id: 106,
        matiere: "Électronique Fondamentale",
        enseignant: "M. Blanc",
        salle: "Labo Elec 1",
        jour: "Vendredi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "CM",
        niveau: "CP1",
        groupe: "CP1-A",
        couleur: "#3182ce"
    },

    // --- CP2 ---
    {
        id: 201,
        matiere: "Mathématiques : Analyse",
        enseignant: "M. Legrand",
        salle: "Amphi A",
        jour: "Lundi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "CM",
        niveau: "CP2",
        groupe: "CP2-A",
        couleur: "#2b6cb0"
    },
    {
        id: 202,
        matiere: "Programmation C++",
        enseignant: "M. Leclerc",
        salle: "Labo Info 2",
        jour: "Lundi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TP",
        niveau: "CP2",
        groupe: "CP2-A",
        couleur: "#dd6b20"
    },
    {
        id: 203,
        matiere: "Électromagnétisme",
        enseignant: "Mme. Renard",
        salle: "Amphi B",
        jour: "Mardi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "CM",
        niveau: "CP2",
        groupe: "CP2-A",
        couleur: "#319795"
    },
    {
        id: 204,
        matiere: "Thermodynamique",
        enseignant: "M. Blanc",
        salle: "Salle B102",
        jour: "Mercredi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TD",
        niveau: "CP2",
        groupe: "CP2-A",
        couleur: "#d69e2e"
    },
    {
        id: 205,
        matiere: "Projet de Conception",
        enseignant: "Mme. Simon",
        salle: "Salle Projet",
        jour: "Jeudi",
        heureDebut: "13h15",
        heureFin: "15h15",
        type: "Projet",
        niveau: "CP2",
        groupe: "CP2-A",
        couleur: "#38a169"
    },
    {
        id: 206,
        matiere: "Optique Ondulatoire",
        enseignant: "M. Roux",
        salle: "Labo Physique",
        jour: "Vendredi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TP",
        niveau: "CP2",
        groupe: "CP2-A",
        couleur: "#805ad5"
    },

    // --- ING1 ---
    {
        id: 301,
        matiere: "POO & Java Avancé",
        enseignant: "M. Robert",
        salle: "Labo Info 1",
        jour: "Lundi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TP",
        niveau: "ING1",
        groupe: "ING1-S5",
        couleur: "#dd6b20"
    },
    {
        id: 302,
        matiere: "Systèmes & Linux",
        enseignant: "M. Thomas",
        salle: "Salle B201",
        jour: "Lundi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TD",
        niveau: "ING1",
        groupe: "ING1-S5",
        couleur: "#4a5568"
    },
    {
        id: 303,
        matiere: "Architecture Ordinateurs",
        enseignant: "Mme. Martin",
        salle: "Amphi A",
        jour: "Mardi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "CM",
        niveau: "ING1",
        groupe: "ING1-S5",
        couleur: "#319795"
    },
    {
        id: 304,
        matiere: "Bases de Données SQL",
        enseignant: "M. Leclerc",
        salle: "Labo Info 3",
        jour: "Mercredi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TP",
        niveau: "ING1",
        groupe: "ING1-S5",
        couleur: "#d69e2e"
    },
    {
        id: 305,
        matiere: "Génie Logiciel",
        enseignant: "M. Dupont",
        salle: "Salle B204",
        jour: "Jeudi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "CM",
        niveau: "ING1",
        groupe: "ING1-S5",
        couleur: "#2b6cb0"
    },
    {
        id: 306,
        matiere: "Réseaux Locaux",
        enseignant: "Mme. Moreau",
        salle: "Labo Réseau",
        jour: "Vendredi",
        heureDebut: "13h15",
        heureFin: "15h15",
        type: "TP",
        niveau: "ING1",
        groupe: "ING1-S5",
        couleur: "#3182ce"
    },

    // --- ING2 ---
    {
        id: 1,
        matiere: "Méthodologies Agiles",
        enseignant: "M. Dupont",
        salle: "Salle B204",
        jour: "Lundi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TD",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#2b6cb0"
    },
    {
        id: 2,
        matiere: "Architecture Logicielle",
        enseignant: "Mme. Martin",
        salle: "Amphi A",
        jour: "Lundi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "CM",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#319795"
    },
    {
        id: 3,
        matiere: "Base de Données Avancées",
        enseignant: "M. Robert",
        salle: "Labo Info 3",
        jour: "Lundi",
        heureDebut: "13h15",
        heureFin: "15h15",
        type: "TP",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#d69e2e"
    },
    {
        id: 4,
        matiere: "Anglais Professionnel",
        enseignant: "Mme. Smith",
        salle: "Salle C101",
        jour: "Mardi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TD",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#805ad5"
    },
    {
        id: 5,
        matiere: "Développement Web Fullstack",
        enseignant: "M. Leclerc",
        salle: "Labo Info 1",
        jour: "Mardi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TP",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#dd6b20"
    },
    {
        id: 6,
        matiere: "Sécurité Informatique",
        enseignant: "M. Bernard",
        salle: "Amphi B",
        jour: "Mardi",
        heureDebut: "13h15",
        heureFin: "15h15",
        type: "CM",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#e53e3e"
    },
    {
        id: 7,
        matiere: "Réseaux & Protocoles",
        enseignant: "Mme. Moreau",
        salle: "Salle B105",
        jour: "Mercredi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "CM",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#3182ce"
    },
    {
        id: 8,
        matiere: "Projet Agile & Sprint",
        enseignant: "M. Dupont",
        salle: "Salle Projet",
        jour: "Mercredi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "Projet",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#38a169"
    },
    {
        id: 9,
        matiere: "DevOps & CI/CD",
        enseignant: "M. Thomas",
        salle: "Labo Info 2",
        jour: "Jeudi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TP",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#4a5568"
    },
    {
        id: 10,
        matiere: "Gestion de Projet & Économie",
        enseignant: "Mme. Petit",
        salle: "Salle A201",
        jour: "Jeudi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TD",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#9f7aea"
    },
    {
        id: 11,
        matiere: "Intelligence Artificielle",
        enseignant: "M. Roux",
        salle: "Amphi A",
        jour: "Jeudi",
        heureDebut: "13h15",
        heureFin: "15h15",
        type: "CM",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#d53f8c"
    },
    {
        id: 12,
        matiere: "Atelier Méthodes Agiles",
        enseignant: "M. Dupont",
        salle: "Salle B204",
        jour: "Vendredi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TD",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#2b6cb0"
    },
    {
        id: 13,
        matiere: "Conférences & Retours d'expérience",
        enseignant: "Invités",
        salle: "Grand Amphi",
        jour: "Vendredi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "CM",
        niveau: "ING2",
        groupe: "ING2-S7",
        couleur: "#4fd1c5"
    },

    // --- ING3 ---
    {
        id: 501,
        matiere: "Cloud & Kubernetes",
        enseignant: "M. Thomas",
        salle: "Labo Cloud",
        jour: "Lundi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TP",
        niveau: "ING3",
        groupe: "ING3-S9",
        couleur: "#4a5568"
    },
    {
        id: 502,
        matiere: "Big Data & Machine Learning",
        enseignant: "M. Roux",
        salle: "Amphi A",
        jour: "Lundi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "CM",
        niveau: "ING3",
        groupe: "ING3-S9",
        couleur: "#d53f8c"
    },
    {
        id: 503,
        matiere: "Management de l'Innovation",
        enseignant: "Mme. Petit",
        salle: "Salle A202",
        jour: "Mardi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "CM",
        niveau: "ING3",
        groupe: "ING3-S9",
        couleur: "#9f7aea"
    },
    {
        id: 504,
        matiere: "Cybersécurité Avancée",
        enseignant: "M. Bernard",
        salle: "Labo Sécu",
        jour: "Mercredi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TP",
        niveau: "ING3",
        groupe: "ING3-S9",
        couleur: "#e53e3e"
    },
    {
        id: 505,
        matiere: "Projet de Fin d'Études (PFE)",
        enseignant: "Tuteurs",
        salle: "Salle Projet",
        jour: "Jeudi",
        heureDebut: "08h00",
        heureFin: "12h15",
        type: "Projet",
        niveau: "ING3",
        groupe: "ING3-S9",
        couleur: "#38a169"
    },
    {
        id: 506,
        matiere: "Droit & Éthique du Numérique",
        enseignant: "Mme. Smith",
        salle: "Amphi B",
        jour: "Vendredi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "CM",
        niveau: "ING3",
        groupe: "ING3-S9",
        couleur: "#805ad5"
    }
];

let niveauActuel = "ING2";

/**
 * Initialise la base de données dans le LocalStorage
 */
async function initialiserBaseDeDonnees() {
    let donneesValides = false;
    try {
        const reponse = await fetch('cours.json');
        if (reponse.ok) {
            const cours = await reponse.json();
            if (Array.isArray(cours) && cours.length >= 20) {
                sauvegarderTousLesCours(cours);
                donneesValides = true;
                console.log("BD initialisée depuis cours.json :", cours);
            }
        }
    } catch (error) {
        console.warn("Chargement direct du JSON impossible (ex: protocole file://), utilisation des données de secours.");
    }

    // Si pas de données valides ou si le LocalStorage contient l'ancien jeu de données (sans les autres niveaux)
    if (!donneesValides) {
        const data = localStorage.getItem(STORAGE_KEY);
        if (!data || JSON.parse(data).length < 20 || !JSON.parse(data).some(c => c.niveau === 'CP1')) {
            sauvegarderTousLesCours(COURS_DEFAUT);
            console.log("BD synchronisée avec COURS_DEFAUT (tous les niveaux).");
        }
    }
}

/**
 * Récupère tous les cours stockés dans le LocalStorage
 * @returns {Array} Liste des cours
 */
function getTousLesCours() {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : COURS_DEFAUT;
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
 * Réinitialise la base de données avec les données par défaut
 */
function reinitialiserBaseDeDonnees() {
    localStorage.removeItem(STORAGE_KEY);
    sauvegarderTousLesCours(COURS_DEFAUT);
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
            return c.niveau.toUpperCase() === niveau.toUpperCase();
        }
        if (c.groupe) {
            return c.groupe.toUpperCase().startsWith(niveau.toUpperCase());
        }
        return false;
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
 * Initialisation des événements pour les boutons de choix de niveau (CP1, CP2, ING1, ING2, ING3)
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

    // Détecter le niveau initialement actif dans le HTML (par défaut ING2)
    const boutonActif = document.querySelector('.level-button.active');
    if (boutonActif) {
        niveauActuel = boutonActif.textContent.trim();
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    await initialiserBaseDeDonnees();
    initialiserBoutonsNiveaux();
    afficherEmploiDuTemps(niveauActuel);
});
