/**
 * Gestion de la base de données des cours (LocalStorage + cours.json)
 * Projet : ADE Scolaire - EILCO
 */

const STORAGE_KEY = 'ade_cours_db';

// Données par défaut au cas où le chargement fetch('cours.json') échoue ou est exécuté via le protocole file://
const COURS_DEFAUT = [
    {
        id: 1,
        matiere: "Méthodologies Agiles",
        enseignant: "M. Dupont",
        salle: "Salle B204",
        jour: "Lundi",
        heureDebut: "08h00",
        heureFin: "10h00",
        type: "TD",
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
        groupe: "ING2-S7",
        couleur: "#4a5568"
    },
    {
        id: 10,
        matiere: "Gestion de Projet",
        enseignant: "Mme. Petit",
        salle: "Salle A201",
        jour: "Jeudi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "TD",
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
        groupe: "ING2-S7",
        couleur: "#2b6cb0"
    },
    {
        id: 13,
        matiere: "Conférences & Retours d'exp",
        enseignant: "Intervenants",
        salle: "Grand Amphi",
        jour: "Vendredi",
        heureDebut: "10h15",
        heureFin: "12h15",
        type: "CM",
        groupe: "ING2-S7",
        couleur: "#4fd1c5"
    }
];

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
 * Affiche dynamiquement les cours dans le tableau de l'emploi du temps
 */
function afficherEmploiDuTemps() {
    const tbody = document.getElementById('calendar-body');
    if (!tbody) return;

    // Vider les cellules du tableau sauf la colonne des heures
    const rows = tbody.querySelectorAll('tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        for (let i = 1; i < cells.length; i++) {
            cells[i].innerHTML = '';
        }
    });

    const mappingJours = {
        "Lundi": 1,
        "Mardi": 2,
        "Mercredi": 3,
        "Jeudi": 4,
        "Vendredi": 5
    };

    const listeCours = getTousLesCours();

    rows.forEach(row => {
        const heureCell = row.querySelector('.hour-cell');
        if (!heureCell) return;
        const horaireTexte = heureCell.textContent.trim(); // ex: "08h00 - 9h00"

        listeCours.forEach(cours => {
            const jourIndex = mappingJours[cours.jour];
            if (!jourIndex) return;

            // Vérifie si le créneau correspond
            if (horaireTexte.startsWith(cours.heureDebut)) {
                const targetCell = row.children[jourIndex];
                if (targetCell) {
                    const card = document.createElement('div');
                    card.className = 'cours-card';
                    if (cours.couleur) {
                        card.style.backgroundColor = cours.couleur;
                    }
                    card.innerHTML = `
                        <span class="cours-badge">${cours.type || 'COURS'}</span>
                        <div class="cours-matiere">${cours.matiere}</div>
                        <div class="cours-infos">
                            <span>${cours.salle || ''}</span>
                            <span>${cours.enseignant || ''}</span>
                        </div>
                    `;
                    targetCell.appendChild(card);
                }
            }
        });
    });
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    await initialiserBaseDeDonnees();
    afficherEmploiDuTemps();
});
