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
 * Calcule tous les jours fériés français pour une année donnée (détection 100% automatique)
 * @param {number} annee 
 * @returns {Map<string, string>} Map avec date au format "YYYY-MM-DD" -> Nom du jour férié
 */
function obtenirJoursFeries(annee) {
    const feries = new Map();

    // Fêtes à dates fixes
    const fixes = {
        "01-01": "Jour de l'An",
        "05-01": "Fête du Travail",
        "05-08": "Victoire 1945",
        "07-14": "Fête Nationale",
        "08-15": "Assomption",
        "11-01": "Toussaint",
        "11-11": "Armistice",
        "12-25": "Noël"
    };
    Object.entries(fixes).forEach(([dateFixe, nom]) => {
        feries.set(`${annee}-${dateFixe}`, nom);
    });

    // Calcul du dimanche de Pâques (algorithme de Meeus)
    const a = annee % 19;
    const b = Math.floor(annee / 100);
    const c = annee % 100;
    const d = Math.floor(b / 4);
    const e = b % 4;
    const f = Math.floor((b + 8) / 25);
    const g = Math.floor((b - f + 1) / 3);
    const h = (19 * a + b - d - g + 15) % 30;
    const i = Math.floor(c / 4);
    const k = c % 4;
    const l = (32 + 2 * e + 2 * i - h - k) % 7;
    const m = Math.floor((a + 11 * h + 22 * l) / 451);
    const moisPaques = Math.floor((h + l - 7 * m + 114) / 31);
    const jourPaques = ((h + l - 7 * m + 114) % 31) + 1;

    const paques = new Date(annee, moisPaques - 1, jourPaques);

    // Fêtes mobiles (Lundi de Pâques, Ascension, Pentecôte)
    const lundiPaques = new Date(paques);
    lundiPaques.setDate(paques.getDate() + 1);
    feries.set(formaterDate(lundiPaques), "Lundi de Pâques");

    const ascension = new Date(paques);
    ascension.setDate(paques.getDate() + 39);
    feries.set(formaterDate(ascension), "Ascension");

    const lundiPentecote = new Date(paques);
    lundiPentecote.setDate(paques.getDate() + 50);
    feries.set(formaterDate(lundiPentecote), "Lundi de Pentecôte");

    return feries;
}

/**
 * Met à jour l'affichage des dates et des jours fériés dans les en-têtes des colonnes
 */
function mettreAJourDatesSemaine() {
    const anneeActuelle = lundiActuel.getFullYear();
    const joursFeries = new Map([
        ...obtenirJoursFeries(anneeActuelle - 1),
        ...obtenirJoursFeries(anneeActuelle),
        ...obtenirJoursFeries(anneeActuelle + 1)
    ]);

    Object.keys(MAPPING_JOURS).forEach((jourNom, index) => {
        const date = new Date(lundiActuel);
        date.setDate(date.getDate() + index);
        const dateStr = formaterDate(date);
        const element = document.getElementById(jourNom.toLowerCase());
        if (element) {
            const dateAffichee = `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}`;
            if (joursFeries.has(dateStr)) {
                element.innerHTML = `${dateAffichee} <span class="badge-ferie">(${joursFeries.get(dateStr)})</span>`;
            } else {
                element.textContent = dateAffichee;
            }
        }
    });
}

/**
 * Navigation entre les semaines (+1 ou -1)
 * @param {number} nombreDeSemaines 
 */
function changerDeSemaine(nombreDeSemaines) {
    if (nombreDeSemaines == -2) {
        lundiActuel = new Date(2026,0,1)
        lundiActuel = obtenirLundi(lundiActuel);
        changerDeSemaine(1)
        mettreAJourDatesSemaine();
        afficherEmploiDuTemps(niveauActuel); 
        console.log(lundiActuel.getDate().toString())
    }
    else if (nombreDeSemaines == 2 ) {
        lundiActuel = new Date(2026, 11, 31)
        lundiActuel = obtenirLundi(lundiActuel);
        changerDeSemaine(-1)
        mettreAJourDatesSemaine();
        afficherEmploiDuTemps(niveauActuel); 
        console.log(lundiActuel.getDate().toString())
    }
    else {
        lundiActuel.setDate(lundiActuel.getDate() + nombreDeSemaines * 7);
        mettreAJourDatesSemaine();
        afficherEmploiDuTemps(niveauActuel);
    }
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
            td.style.display = '';
            td.classList.remove('ferie-cell');
        });
    });

    // 2. Détection et grisé des jours fériés (automatique)
    const anneeActuelle = lundiActuel.getFullYear();
    const joursFeries = new Map([
        ...obtenirJoursFeries(anneeActuelle - 1),
        ...obtenirJoursFeries(anneeActuelle),
        ...obtenirJoursFeries(anneeActuelle + 1)
    ]);

    const colonnesFeriees = new Map();
    Object.keys(MAPPING_JOURS).forEach(jourNom => {
        const dateStr = obtenirDateDuJour(lundiActuel, jourNom);
        if (joursFeries.has(dateStr)) {
            colonnesFeriees.set(MAPPING_JOURS[jourNom], joursFeries.get(dateStr));
        }
    });

    // Appliquer le style grisé à toutes les lignes des colonnes fériées
    rows.forEach((row, rowIdx) => {
        if (row.classList.contains('pause-row')) return;
        colonnesFeriees.forEach((nomFerie, colIndex) => {
            const cell = row.children[colIndex];
            if (cell) {
                cell.classList.add('ferie-cell');
            }
        });
    });

    // 3. Récupérer et filtrer les cours
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

        // Si le jour est férié, ne pas afficher de cours
        if (joursFeries.has(dateCours)) return false;

        if (!c.date) {
            return formaterDate(lundiActuel) === formaterDate(obtenirLundi(new Date()));
        }

        return c.date === dateCours;
    });

    // 4. Insérer chaque cours dans le tableau
    listeCours.forEach(cours => {
        const jourIndex = MAPPING_JOURS[cours.jour];
        if (!jourIndex) return;

        const rowDebut = document.querySelector(`#calendar-body tr[data-heure="${cours.heureDebut}"]`);
        if (!rowDebut) return;

        const cellDebut = rowDebut.children[jourIndex];
        if (!cellDebut) return;

        const rowspan = calculerRowspan(cours.heureDebut, cours.heureFin);

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
    document.getElementById('derniere-semaine')?.addEventListener('click', () => {
        changerDeSemaine(2);
    });

    document.getElementById('premiere-semaine')?.addEventListener('click', () => {
        changerDeSemaine(-2);
    });
}

function initialiserBoutonSemaineEnCours() {
    document.getElementById('semaine-encours')?.addEventListener('click', () => {
        lundiActuel = obtenirLundi(new Date());
        mettreAJourDatesSemaine();
        afficherEmploiDuTemps(niveauActuel);
    });
}

// Initialisation générale au chargement du DOM
document.addEventListener('DOMContentLoaded', async () => {
    await initialiserBaseDeDonnees();
    initialiserBoutonsNiveaux();
    initialiserNavigationSemaines();
    mettreAJourDatesSemaine();
    afficherEmploiDuTemps(niveauActuel);
    initialiserBoutonSemaineEnCours();
});
