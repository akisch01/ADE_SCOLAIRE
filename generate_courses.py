import json
import datetime

start_monday = datetime.date(2026, 8, 31)
weeks = []
for w in range(16):
    monday = start_monday + datetime.timedelta(days=w*7)
    weeks.append((w + 1, monday))

jours_map = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi"}
all_courses = []
current_id = 1

def obtenir_jours_feries(annee):
    """Calcule tous les jours fériés français automatiquement (fixes + mobiles via Meeus)."""
    feries = {}
    # Fêtes à dates fixes
    fixes = {
        "01-01": "Jour de l'An",
        "05-01": "Fête du Travail",
        "05-08": "Victoire 1945",
        "07-14": "Fête Nationale",
        "08-15": "Assomption",
        "11-01": "Toussaint",
        "11-11": "Armistice",
        "12-25": "Noël"
    }
    for date_str, nom in fixes.items():
        feries[f"{annee}-{date_str}"] = nom

    # Calcul de Pâques (algorithme de Meeus)
    a = annee % 19
    b = annee // 100
    c = annee % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mois_paques = (h + l - 7 * m + 114) // 31
    jour_paques = ((h + l - 7 * m + 114) % 31) + 1
    paques = datetime.date(annee, mois_paques, jour_paques)

    # Fêtes mobiles
    lundi_paques = paques + datetime.timedelta(days=1)
    ascension = paques + datetime.timedelta(days=39)
    lundi_pentecote = paques + datetime.timedelta(days=50)

    feries[lundi_paques.strftime("%Y-%m-%d")] = "Lundi de Pâques"
    feries[ascension.strftime("%Y-%m-%d")] = "Ascension"
    feries[lundi_pentecote.strftime("%Y-%m-%d")] = "Lundi de Pentecôte"

    return feries

def add_c(week_monday, jour_idx, heureDebut, heureFin, matiere, enseignant, salle, type_cours, niveau, groupe, couleur):
    global current_id
    date_jour = week_monday + datetime.timedelta(days=jour_idx)
    jour_nom = jours_map[jour_idx]
    date_str = date_jour.strftime("%Y-%m-%d")
    
    # Détection 100% automatique de n'importe quel jour férié français
    feries = obtenir_jours_feries(date_jour.year)
    if date_str in feries:
        return
        
    c = {
        "id": current_id,
        "matiere": matiere,
        "enseignant": enseignant,
        "salle": salle,
        "jour": jour_nom,
        "date": date_str,
        "heureDebut": heureDebut,
        "heureFin": heureFin,
        "type": type_cours,
        "niveau": niveau,
        "groupe": groupe,
        "couleur": couleur
    }
    all_courses.append(c)
    current_id += 1

C_BLUE = "#2b6cb0"
C_TEAL = "#319795"
C_ORANGE = "#dd6b20"
C_GOLD = "#d69e2e"
C_PURPLE = "#805ad5"
C_LIGHTBLUE = "#3182ce"
C_GREEN = "#38a169"
C_RED = "#e53e3e"
C_SLATE = "#4a5568"
C_PINK = "#d53f8c"
C_VIOLET = "#9f7aea"
C_CYAN = "#4fd1c5"

for week_num, monday in weeks:
    # ----------------------------------------------------
    # SEMAINE 1 (31/08 - 04/09) : RENTRÉE & INTÉGRATION
    # ----------------------------------------------------
    if week_num == 1:
        # CP1
        add_c(monday, 0, "08h00", "10h00", "Accueil & Rentrée CP1", "Direction EILCO", "Grand Amphi", "Conférence", "CP1", "CP1-A", C_CYAN)
        add_c(monday, 0, "10h15", "12h15", "Visite des Campus & Labos", "Tuteurs", "Campus", "Atelier", "CP1", "CP1-A", C_GREEN)
        add_c(monday, 1, "08h00", "10h00", "Mathématiques : Test de positionnement", "M. Legrand", "Salle CP1", "TD", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 1, "10h15", "12h15", "Physique : Introduction & Méthode", "Mme. Renard", "Amphi B", "CM", "CP1", "CP1-A", C_TEAL)
        add_c(monday, 2, "08h00", "10h00", "Expression & Dynamique de groupe", "Mme. Petit", "Salle C102", "TD", "CP1", "CP1-A", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "Découverte des Environnements Info", "M. Robert", "Labo Info 1", "TP", "CP1", "CP1-A", C_ORANGE)
        add_c(monday, 3, "10h15", "12h15", "Mathématiques : Notions de base", "M. Legrand", "Salle CP1", "CM", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 3, "13h15", "15h15", "Anglais LV1 : Évaluation de rentrée", "Mme. Smith", "Salle C102", "TD", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 4, "08h00", "10h00", "Électronique : Présentation Labo", "M. Blanc", "Labo Elec 1", "CM", "CP1", "CP1-A", C_LIGHTBLUE)
        add_c(monday, 4, "10h15", "12h15", "Tutorat & Méthodologie", "M. Blanc", "Salle CP1", "TD", "CP1", "CP1-A", C_CYAN)

        # CP2
        add_c(monday, 0, "08h00", "10h00", "Rentrée CP2 & Présentation du Programme", "Direction", "Amphi A", "Conférence", "CP2", "CP2-A", C_CYAN)
        add_c(monday, 0, "10h15", "12h15", "Programmation C++ : Prise en main IDE", "M. Leclerc", "Labo Info 2", "TP", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Électronique : Rappels & Composants", "M. Blanc", "Labo Elec 2", "TP", "CP2", "CP2-A", C_LIGHTBLUE)
        add_c(monday, 1, "10h15", "12h15", "Électromagnétisme : Lois fondamentales", "Mme. Renard", "Amphi B", "CM", "CP2", "CP2-A", C_TEAL)
        add_c(monday, 2, "08h00", "10h00", "Thermodynamique : Systèmes & Énergie", "M. Blanc", "Salle B102", "TD", "CP2", "CP2-A", C_GOLD)
        add_c(monday, 2, "10h15", "12h15", "Mathématiques : Analyse 2 - Séries", "M. Legrand", "Amphi A", "CM", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 3, "10h15", "12h15", "Anglais LV1 : Communication & Oral", "Mme. Smith", "Salle C101", "TD", "CP2", "CP2-A", C_PURPLE)
        add_c(monday, 3, "13h15", "15h15", "Projet de Conception : Lancement", "Mme. Simon", "Salle Projet", "Projet", "CP2", "CP2-A", C_GREEN)
        add_c(monday, 4, "08h00", "10h00", "Mathématiques : Algèbre bilinéaire", "M. Legrand", "Salle B102", "TD", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Optique : Ondes et propagation", "M. Roux", "Labo Physique", "TP", "CP2", "CP2-A", C_PURPLE)

        # ING1
        add_c(monday, 0, "08h00", "10h00", "Rentrée Cycle Ingénieur ING1", "Directeur des Études", "Amphi A", "Conférence", "ING1", "ING1-S5", C_CYAN)
        add_c(monday, 0, "10h15", "12h15", "Systèmes & Linux : Installation de l'OS", "M. Thomas", "Salle B201", "TD", "ING1", "ING1-S5", C_SLATE)
        add_c(monday, 0, "13h15", "15h15", "POO & Java : Rappels fondamentaux", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Architecture Ordinateurs : Circuits logiques", "Mme. Martin", "Amphi A", "CM", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "10h15", "12h15", "Mathématiques pour l'Ingénieur : Signaux", "M. Legrand", "Salle B201", "TD", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 1, "13h15", "15h15", "Anglais Technique : Vocabulaire IT", "Mme. Smith", "Salle C102", "TD", "ING1", "ING1-S5", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "Droit du Travail & Éthique de l'Ingénieur", "Mme. Petit", "Salle B201", "TD", "ING1", "ING1-S5", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "Bases de Données SQL : Modèle E/A", "M. Leclerc", "Labo Info 3", "TP", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 3, "08h00", "10h00", "Génie Logiciel : Cycles de développement", "M. Dupont", "Salle B204", "CM", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 3, "10h15", "12h15", "Web Frontend : HTML5/CSS3 Moderne", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 4, "10h15", "12h15", "Probabilités & Statistiques pour l'Ingénieur", "Mme. Renard", "Salle B201", "TD", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 4, "13h15", "15h15", "Réseaux : Modèle OSI & Adressage IP", "Mme. Moreau", "Labo Réseau", "TP", "ING1", "ING1-S5", C_LIGHTBLUE)

        # ING2
        add_c(monday, 0, "08h00", "10h00", "Méthodologies Agiles : Manifeste & Principes", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Architecture Logicielle : Modèles en couches", "Mme. Martin", "Amphi A", "CM", "ING2", "ING2-S7", C_TEAL)
        add_c(monday, 0, "13h15", "15h15", "Base de Données Avancées : Indexation & Performance", "M. Robert", "Labo Info 3", "TP", "ING2", "ING2-S7", C_GOLD)
        add_c(monday, 1, "08h00", "10h00", "Anglais Professionnel : Pitch & Présentation", "Mme. Smith", "Salle C101", "TD", "ING2", "ING2-S7", C_PURPLE)
        add_c(monday, 1, "10h15", "12h15", "Développement Web Fullstack : Node & Express", "M. Leclerc", "Labo Info 1", "TP", "ING2", "ING2-S7", C_ORANGE)
        add_c(monday, 1, "13h15", "15h15", "Sécurité Informatique : Menaces & Vecteurs", "M. Bernard", "Amphi B", "CM", "ING2", "ING2-S7", C_RED)
        add_c(monday, 2, "08h00", "10h00", "Réseaux & Protocoles : TCP/IP & Wireshark", "Mme. Moreau", "Salle B105", "CM", "ING2", "ING2-S7", C_LIGHTBLUE)
        add_c(monday, 2, "10h15", "12h15", "Projet Agile : Constitution des Équipes Scrum", "M. Dupont", "Salle Projet", "Projet", "ING2", "ING2-S7", C_GREEN)
        add_c(monday, 3, "08h00", "10h00", "DevOps & CI/CD : Introduction à Docker", "M. Thomas", "Labo Info 2", "TP", "ING2", "ING2-S7", C_SLATE)
        add_c(monday, 3, "10h15", "12h15", "Gestion de Projet & Modèles Économiques", "Mme. Petit", "Salle A201", "TD", "ING2", "ING2-S7", C_VIOLET)
        add_c(monday, 3, "13h15", "15h15", "Intelligence Artificielle : Panorama & Enjeux", "M. Roux", "Amphi A", "CM", "ING2", "ING2-S7", C_PINK)
        add_c(monday, 4, "08h00", "10h00", "Atelier Agile : Ice-breaker & Lego Scrum", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Conférence d'Ouverture Semestre ING2", "Invités", "Grand Amphi", "Conférence", "ING2", "ING2-S7", C_CYAN)

        # ING3
        add_c(monday, 0, "08h00", "10h00", "Cloud : Architecture AWS & GCP", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_SLATE)
        add_c(monday, 0, "10h15", "12h15", "Big Data : Enjeux & Écosystème Spark", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 0, "13h15", "15h15", "Microservices : Principes de découplage", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_LIGHTBLUE)
        add_c(monday, 1, "08h00", "10h00", "Gouvernance IT : Normes ISO 27001 & ITIL", "M. Bernard", "Salle A202", "TD", "ING3", "ING3-S9", C_RED)
        add_c(monday, 1, "10h15", "12h15", "Management de l'Innovation & Design Thinking", "Mme. Petit", "Salle A202", "CM", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 1, "13h15", "15h15", "IA Générative : LLMs & Architectures Transformers", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 2, "08h00", "10h00", "Cybersécurité : Audit & Tests d'intrusion", "M. Bernard", "Labo Sécu", "TP", "ING3", "ING3-S9", C_RED)
        add_c(monday, 2, "10h15", "12h15", "Architecture d'Entreprise : TOGAF & Urbanisation", "Mme. Martin", "Salle A202", "CM", "ING3", "ING3-S9", C_TEAL)
        add_c(monday, 3, "08h00", "12h15", "PFE : Attribution des Sujets & Rencontre Tuteurs", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "13h15", "15h15", "Entrepreneuriat : Du prototype au Business Model", "Mme. Petit", "Salle A202", "TD", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 4, "10h15", "12h15", "Droit du Numérique : RGPD & Propriété intellectuelle", "Mme. Smith", "Amphi B", "CM", "ING3", "ING3-S9", C_PURPLE)
        add_c(monday, 4, "13h15", "15h15", "Séminaire Insertion & Carrière Ingénieur", "Intervenants", "Grand Amphi", "Conférence", "ING3", "ING3-S9", C_CYAN)

    # ----------------------------------------------------
    # SEMAINE 4 (21/09 - 25/09) : SEMAINE CANONIQUE DE RÉFÉRENCE (EXACTE)
    # ----------------------------------------------------
    elif week_num == 4:
        # CP1
        add_c(monday, 0, "08h00", "10h00", "Mathématiques : Algèbre", "M. Legrand", "Salle CP1", "CM", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Physique : Mécanique", "Mme. Renard", "Amphi B", "TD", "CP1", "CP1-A", C_TEAL)
        add_c(monday, 1, "08h00", "10h00", "Initiation Algorithmique", "M. Robert", "Labo Info 1", "TP", "CP1", "CP1-A", C_ORANGE)
        add_c(monday, 1, "10h15", "12h15", "Optique Géométrique", "M. Roux", "Labo Physique", "CM", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "Expression & Communication", "Mme. Petit", "Salle C102", "TD", "CP1", "CP1-A", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "Chimie Générale", "Mme. Simon", "Labo Chimie", "TP", "CP1", "CP1-A", C_GOLD)
        add_c(monday, 3, "10h15", "12h15", "Mathématiques : Analyse 1", "M. Legrand", "Salle CP1", "TD", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 3, "13h15", "15h15", "Anglais LV1", "Mme. Smith", "Salle C102", "TD", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 4, "08h00", "10h00", "Électronique Fondamentale", "M. Blanc", "Labo Elec 1", "CM", "CP1", "CP1-A", C_LIGHTBLUE)
        add_c(monday, 4, "10h15", "12h15", "Tutorat & Méthodologie", "M. Blanc", "Salle CP1", "TD", "CP1", "CP1-A", C_CYAN)

        # CP2
        add_c(monday, 0, "08h00", "10h00", "Mathématiques : Analyse", "M. Legrand", "Amphi A", "CM", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Programmation C++", "M. Leclerc", "Labo Info 2", "TP", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Électronique Analogique", "M. Blanc", "Labo Elec 2", "TP", "CP2", "CP2-A", C_LIGHTBLUE)
        add_c(monday, 1, "10h15", "12h15", "Électromagnétisme", "Mme. Renard", "Amphi B", "CM", "CP2", "CP2-A", C_TEAL)
        add_c(monday, 2, "08h00", "10h00", "Thermodynamique", "M. Blanc", "Salle B102", "TD", "CP2", "CP2-A", C_GOLD)
        add_c(monday, 2, "10h15", "12h15", "Structures de Données & Algo", "M. Robert", "Labo Info 2", "TP", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 3, "10h15", "12h15", "Anglais LV1", "Mme. Smith", "Salle C101", "TD", "CP2", "CP2-A", C_PURPLE)
        add_c(monday, 3, "13h15", "15h15", "Projet de Conception", "Mme. Simon", "Salle Projet", "Projet", "CP2", "CP2-A", C_GREEN)
        add_c(monday, 4, "08h00", "10h00", "Mathématiques : Algèbre 2", "M. Legrand", "Salle B102", "TD", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Optique Ondulatoire", "M. Roux", "Labo Physique", "TP", "CP2", "CP2-A", C_PURPLE)

        # ING1
        add_c(monday, 0, "08h00", "10h00", "POO & Java Avancé", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 0, "10h15", "12h15", "Systèmes & Linux", "M. Thomas", "Salle B201", "TD", "ING1", "ING1-S5", C_SLATE)
        add_c(monday, 0, "13h15", "15h15", "Algorithmique Avancée", "M. Leclerc", "Labo Info 2", "TP", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "08h00", "10h00", "Architecture Ordinateurs", "Mme. Martin", "Amphi A", "CM", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "10h15", "12h15", "Mathématiques pour l'Ingénieur", "M. Legrand", "Salle B201", "TD", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 1, "13h15", "15h15", "Anglais Technique", "Mme. Smith", "Salle C102", "TD", "ING1", "ING1-S5", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "Droit du Travail & RSE", "Mme. Petit", "Salle B201", "TD", "ING1", "ING1-S5", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "Bases de Données SQL", "M. Leclerc", "Labo Info 3", "TP", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 3, "08h00", "10h00", "Génie Logiciel", "M. Dupont", "Salle B204", "CM", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 3, "10h15", "12h15", "Programmation Web Frontend", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 4, "10h15", "12h15", "Probabilités & Statistiques", "Mme. Renard", "Salle B201", "TD", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 4, "13h15", "15h15", "Réseaux Locaux", "Mme. Moreau", "Labo Réseau", "TP", "ING1", "ING1-S5", C_LIGHTBLUE)

        # ING2
        add_c(monday, 0, "08h00", "10h00", "Méthodologies Agiles", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Architecture Logicielle", "Mme. Martin", "Amphi A", "CM", "ING2", "ING2-S7", C_TEAL)
        add_c(monday, 0, "13h15", "15h15", "Base de Données Avancées", "M. Robert", "Labo Info 3", "TP", "ING2", "ING2-S7", C_GOLD)
        add_c(monday, 1, "08h00", "10h00", "Anglais Professionnel", "Mme. Smith", "Salle C101", "TD", "ING2", "ING2-S7", C_PURPLE)
        add_c(monday, 1, "10h15", "12h15", "Développement Web Fullstack", "M. Leclerc", "Labo Info 1", "TP", "ING2", "ING2-S7", C_ORANGE)
        add_c(monday, 1, "13h15", "15h15", "Sécurité Informatique", "M. Bernard", "Amphi B", "CM", "ING2", "ING2-S7", C_RED)
        add_c(monday, 2, "08h00", "10h00", "Réseaux & Protocoles", "Mme. Moreau", "Salle B105", "CM", "ING2", "ING2-S7", C_LIGHTBLUE)
        add_c(monday, 2, "10h15", "12h15", "Projet Agile & Sprint", "M. Dupont", "Salle Projet", "Projet", "ING2", "ING2-S7", C_GREEN)
        add_c(monday, 3, "08h00", "10h00", "DevOps & CI/CD", "M. Thomas", "Labo Info 2", "TP", "ING2", "ING2-S7", C_SLATE)
        add_c(monday, 3, "10h15", "12h15", "Gestion de Projet & Économie", "Mme. Petit", "Salle A201", "TD", "ING2", "ING2-S7", C_VIOLET)
        add_c(monday, 3, "13h15", "15h15", "Intelligence Artificielle", "M. Roux", "Amphi A", "CM", "ING2", "ING2-S7", C_PINK)
        add_c(monday, 4, "08h00", "10h00", "Atelier Méthodes Agiles", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Conférences & Retours d'expérience", "Invités", "Grand Amphi", "CM", "ING2", "ING2-S7", C_CYAN)

        # ING3
        add_c(monday, 0, "08h00", "10h00", "Cloud & Kubernetes", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_SLATE)
        add_c(monday, 0, "10h15", "12h15", "Big Data & Machine Learning", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 0, "13h15", "15h15", "Microservices & Event-Driven", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_LIGHTBLUE)
        add_c(monday, 1, "08h00", "10h00", "Gouvernance IT & Audit", "M. Bernard", "Salle A202", "TD", "ING3", "ING3-S9", C_RED)
        add_c(monday, 1, "10h15", "12h15", "Management de l'Innovation", "Mme. Petit", "Salle A202", "CM", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 1, "13h15", "15h15", "Intelligence Artificielle Générative", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 2, "08h00", "10h00", "Cybersécurité Avancée", "M. Bernard", "Labo Sécu", "TP", "ING3", "ING3-S9", C_RED)
        add_c(monday, 2, "10h15", "12h15", "Architecture d'Entreprise", "Mme. Martin", "Salle A202", "CM", "ING3", "ING3-S9", C_TEAL)
        add_c(monday, 3, "08h00", "10h00", "Projet de Fin d'Études (PFE) - Séance 1", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "10h15", "12h15", "Projet de Fin d'Études (PFE) - Séance 2", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "13h15", "15h15", "Entrepreneuriat & Startups", "Mme. Petit", "Salle A202", "TD", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 4, "10h15", "12h15", "Droit & Éthique du Numérique", "Mme. Smith", "Amphi B", "CM", "ING3", "ING3-S9", C_PURPLE)
        add_c(monday, 4, "13h15", "15h15", "Accompagnement & Suivi PFE", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)

    # ----------------------------------------------------
    # SEMAINE 6 (05/10 - 09/10) : ÉVALUATIONS CONTINUES (DS)
    # ----------------------------------------------------
    elif week_num == 6:
        # CP1
        add_c(monday, 0, "08h00", "10h00", "Contrôle Continu : Mathématiques Algèbre", "M. Legrand", "Salle CP1", "Examen", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Physique : Travaux Dirigés Cinématique", "Mme. Renard", "Amphi B", "TD", "CP1", "CP1-A", C_TEAL)
        add_c(monday, 1, "08h00", "10h00", "TP Évalué : Algorithmique en C", "M. Robert", "Labo Info 1", "TP", "CP1", "CP1-A", C_ORANGE)
        add_c(monday, 1, "13h15", "15h15", "Optique Géométrique : Dioptres et Miroirs", "M. Roux", "Labo Physique", "TP", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "Communication : Rapports Techniques", "Mme. Petit", "Salle C102", "TD", "CP1", "CP1-A", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "Chimie : TP Dosages Acido-Basiques", "Mme. Simon", "Labo Chimie", "TP", "CP1", "CP1-A", C_GOLD)
        add_c(monday, 3, "10h15", "12h15", "Mathématiques : Développements limités", "M. Legrand", "Salle CP1", "TD", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 3, "13h15", "15h15", "Anglais LV1 : Débat en groupe", "Mme. Smith", "Salle C102", "TD", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 4, "08h00", "10h00", "Contrôle Continu : Électronique Fondamentale", "M. Blanc", "Salle CP1", "Examen", "CP1", "CP1-A", C_LIGHTBLUE)
        add_c(monday, 4, "10h15", "12h15", "Séance de Tutorat & Exercices Corrigés", "M. Blanc", "Salle CP1", "TD", "CP1", "CP1-A", C_CYAN)

        # CP2
        add_c(monday, 0, "08h00", "10h00", "Contrôle Continu : Mathématiques Analyse", "M. Legrand", "Amphi A", "Examen", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "C++ : Programmation Orientée Objet", "M. Leclerc", "Labo Info 2", "TP", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Électronique : Filtres Actifs & AOP", "M. Blanc", "Labo Elec 2", "TP", "CP2", "CP2-A", C_LIGHTBLUE)
        add_c(monday, 1, "10h15", "12h15", "Électromagnétisme : Ondes dans le vide", "Mme. Renard", "Amphi B", "CM", "CP2", "CP2-A", C_TEAL)
        add_c(monday, 2, "08h00", "10h00", "Thermodynamique : Cycles & Rendements", "M. Blanc", "Salle B102", "TD", "CP2", "CP2-A", C_GOLD)
        add_c(monday, 2, "10h15", "12h15", "Contrôle Continu : Algorithmique C++", "M. Robert", "Labo Info 2", "Examen", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 3, "10h15", "12h15", "Anglais LV1 : Présentation Technique", "Mme. Smith", "Salle C101", "TD", "CP2", "CP2-A", C_PURPLE)
        add_c(monday, 3, "13h15", "15h15", "Projet de Conception : Point d'étape 1", "Mme. Simon", "Salle Projet", "Projet", "CP2", "CP2-A", C_GREEN)
        add_c(monday, 4, "08h00", "10h00", "Mathématiques : Réduction d'endomorphismes", "M. Legrand", "Salle B102", "TD", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Optique : Interférences & Diffraction", "M. Roux", "Labo Physique", "TP", "CP2", "CP2-A", C_PURPLE)

        # ING1
        add_c(monday, 0, "08h00", "10h00", "Java : Héritage, Interfaces & Polymorphisme", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 0, "10h15", "12h15", "Contrôle Continu : Systèmes & Scripts Bash", "M. Thomas", "Salle B201", "Examen", "ING1", "ING1-S5", C_SLATE)
        add_c(monday, 0, "13h15", "15h15", "Graphes & Algorithmes de Dijkstra / A*", "M. Leclerc", "Labo Info 2", "TP", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "08h00", "10h00", "Architecture : Pipeline & Mémoire Cache", "Mme. Martin", "Amphi A", "CM", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "10h15", "12h15", "Mathématiques : Transformation de Fourier", "M. Legrand", "Salle B201", "TD", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 1, "13h15", "15h15", "Anglais Technique : Écriture Documentation", "Mme. Smith", "Salle C102", "TD", "ING1", "ING1-S5", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "RSE & Développement Durable dans l'IT", "Mme. Petit", "Salle B201", "TD", "ING1", "ING1-S5", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "Bases de Données : Jointures & Triggers", "M. Leclerc", "Labo Info 3", "TP", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 3, "08h00", "10h00", "Contrôle Continu : Génie Logiciel & UML", "M. Dupont", "Salle B204", "Examen", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 3, "10h15", "12h15", "Frontend : DOM & JavaScript Asynchrone", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 4, "10h15", "12h15", "Probabilités : Lois Continues & Test Chi2", "Mme. Renard", "Salle B201", "TD", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 4, "13h15", "15h15", "Réseaux : TP Routage Statique & RIP", "Mme. Moreau", "Labo Réseau", "TP", "ING1", "ING1-S5", C_LIGHTBLUE)

        # ING2
        add_c(monday, 0, "08h00", "10h00", "Méthodologies Agiles : User Stories & Estimation", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Architecture Logicielle : Microservices vs Monolithe", "Mme. Martin", "Amphi A", "CM", "ING2", "ING2-S7", C_TEAL)
        add_c(monday, 0, "13h15", "15h15", "TP Évalué : Optimisation Requêtes SQL & Index", "M. Robert", "Labo Info 3", "TP", "ING2", "ING2-S7", C_GOLD)
        add_c(monday, 1, "08h00", "10h00", "Anglais Professionnel : Entretien d'Embauche IT", "Mme. Smith", "Salle C101", "TD", "ING2", "ING2-S7", C_PURPLE)
        add_c(monday, 1, "10h15", "12h15", "Web Fullstack : Authentification JWT & Sessions", "M. Leclerc", "Labo Info 1", "TP", "ING2", "ING2-S7", C_ORANGE)
        add_c(monday, 1, "13h15", "15h15", "Sécurité : Analyse de Vulnérabilités OWASP", "M. Bernard", "Amphi B", "CM", "ING2", "ING2-S7", C_RED)
        add_c(monday, 2, "08h00", "10h00", "Réseaux : Routage Dynamique OSPF & BGP", "Mme. Moreau", "Salle B105", "CM", "ING2", "ING2-S7", C_LIGHTBLUE)
        add_c(monday, 2, "10h15", "12h15", "Projet Agile : Revue de Sprint 1 & Démonstration", "M. Dupont", "Salle Projet", "Projet", "ING2", "ING2-S7", C_GREEN)
        add_c(monday, 3, "08h00", "10h00", "DevOps : GitHub Actions & Tests Automatisés", "M. Thomas", "Labo Info 2", "TP", "ING2", "ING2-S7", C_SLATE)
        add_c(monday, 3, "10h15", "12h15", "Gestion de Projet : Analyse Financière & ROI", "Mme. Petit", "Salle A201", "TD", "ING2", "ING2-S7", C_VIOLET)
        add_c(monday, 3, "13h15", "15h15", "IA : Algorithmes Génétiques & Heuristiques", "M. Roux", "Amphi A", "CM", "ING2", "ING2-S7", C_PINK)
        add_c(monday, 4, "08h00", "10h00", "Atelier Agile : Rétrospective Sprint 1", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Conférence : Architectures Cloud & Sécurité", "Invités", "Grand Amphi", "Conférence", "ING2", "ING2-S7", C_CYAN)

        # ING3
        add_c(monday, 0, "08h00", "10h00", "Kubernetes : Pods, Deployments & Services", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_SLATE)
        add_c(monday, 0, "10h15", "12h15", "Machine Learning : Régression & Classification", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 0, "13h15", "15h15", "Event-Driven : RabbitMQ & Event Sourcing", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_LIGHTBLUE)
        add_c(monday, 1, "08h00", "10h00", "Contrôle Continu : Gouvernance & Conformité IT", "M. Bernard", "Salle A202", "Examen", "ING3", "ING3-S9", C_RED)
        add_c(monday, 1, "10h15", "12h15", "Innovation : Stratégies de Croissance Tech", "Mme. Petit", "Salle A202", "CM", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 1, "13h15", "15h15", "IA Générative : Fine-tuning & RAG", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 2, "08h00", "10h00", "Cybersécurité : Exploitation de Failles Mémoire", "M. Bernard", "Labo Sécu", "TP", "ING3", "ING3-S9", C_RED)
        add_c(monday, 2, "10h15", "12h15", "Urbanisation du SI : Cartographie Applicative", "Mme. Martin", "Salle A202", "CM", "ING3", "ING3-S9", C_TEAL)
        add_c(monday, 3, "08h00", "12h15", "PFE : Revue d'Avancement Technique Sprint 1", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "13h15", "15h15", "Startups : Financement & Levée de fonds", "Mme. Petit", "Salle A202", "TD", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 4, "10h15", "12h15", "Droit de l'IA & Responsabilité Algorithmique", "Mme. Smith", "Amphi B", "CM", "ING3", "ING3-S9", C_PURPLE)
        add_c(monday, 4, "13h15", "15h15", "Séminaire : Retours d'Expérience d'Ingénieurs", "Intervenants", "Grand Amphi", "Conférence", "ING3", "ING3-S9", C_CYAN)

    # ----------------------------------------------------
    # SEMAINE 9 (26/10 - 30/10) : HACKATHON & PROJETS INTENSIFS
    # ----------------------------------------------------
    elif week_num == 9:
        # CP1
        add_c(monday, 0, "08h00", "10h00", "Mathématiques : Bilan mi-semestre Algèbre", "M. Legrand", "Salle CP1", "TD", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Physique : TP Mécanique du Solide", "Mme. Renard", "Labo Physique", "TP", "CP1", "CP1-A", C_TEAL)
        add_c(monday, 1, "08h00", "12h15", "Mini-Hackathon C : Création d'un Jeu Console", "M. Robert", "Labo Info 1", "Projet", "CP1", "CP1-A", C_ORANGE)
        add_c(monday, 2, "08h00", "10h00", "Expression : Pitch & Présentation Orale", "Mme. Petit", "Salle C102", "TD", "CP1", "CP1-A", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "Chimie : TP Synthèse Organique", "Mme. Simon", "Labo Chimie", "TP", "CP1", "CP1-A", C_GOLD)
        add_c(monday, 3, "10h15", "12h15", "Mathématiques : Analyse 1 - Intégrales", "M. Legrand", "Salle CP1", "CM", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 3, "13h15", "15h15", "Anglais : Mini-Présentations Équipes", "Mme. Smith", "Salle C102", "TD", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 4, "08h00", "12h15", "Challenge Électronique : Circuit PCB", "M. Blanc", "Labo Elec 1", "Projet", "CP1", "CP1-A", C_LIGHTBLUE)

        # CP2
        add_c(monday, 0, "08h00", "12h15", "Hackathon C++ : Moteur Graphique 2D", "M. Leclerc", "Labo Info 2", "Projet", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Électronique : Simulation LTSpice", "M. Blanc", "Labo Elec 2", "TP", "CP2", "CP2-A", C_LIGHTBLUE)
        add_c(monday, 1, "10h15", "12h15", "Électromagnétisme : Ondes Guidées", "Mme. Renard", "Amphi B", "CM", "CP2", "CP2-A", C_TEAL)
        add_c(monday, 2, "08h00", "10h00", "Thermodynamique : Machines Thermiques", "M. Blanc", "Salle B102", "TD", "CP2", "CP2-A", C_GOLD)
        add_c(monday, 2, "10h15", "12h15", "Algo C++ : Arbres Binaires & Tas", "M. Robert", "Labo Info 2", "TP", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 3, "08h00", "12h15", "Projet Conception : Prototypage 3D", "Mme. Simon", "Salle Projet", "Projet", "CP2", "CP2-A", C_GREEN)
        add_c(monday, 3, "13h15", "15h15", "Anglais : Démonstration Technique", "Mme. Smith", "Salle C101", "TD", "CP2", "CP2-A", C_PURPLE)
        add_c(monday, 4, "08h00", "10h00", "Mathématiques : Espaces Préhilbertiens", "M. Legrand", "Salle B102", "TD", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Optique : TP Polarisation & Lasers", "M. Roux", "Labo Physique", "TP", "CP2", "CP2-A", C_PURPLE)

        # ING1
        add_c(monday, 0, "08h00", "12h15", "Hackathon S5 : Client-Serveur Java/SQL", "M. Robert", "Labo Info 1", "Projet", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Architecture : Microcontrôleurs & Assembleur", "Mme. Martin", "Amphi A", "CM", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "10h15", "12h15", "Mathématiques : Équations Différentielles", "M. Legrand", "Salle B201", "TD", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 1, "13h15", "15h15", "Anglais : Pitch Solution Logicielle", "Mme. Smith", "Salle C102", "TD", "ING1", "ING1-S5", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "Propriété Industrielle & Brevets", "Mme. Petit", "Salle B201", "TD", "ING1", "ING1-S5", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", "SQL Avancé : Procédures Stockées", "M. Leclerc", "Labo Info 3", "TP", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 3, "08h00", "10h00", "Génie Logiciel : Design Patterns", "M. Dupont", "Salle B204", "CM", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 3, "10h15", "12h15", "Frontend : Responsive Web Design", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 4, "10h15", "12h15", "Statistiques Inférentielles & Tests", "Mme. Renard", "Salle B201", "TD", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 4, "13h15", "15h15", "Réseaux : TP Switchs & VLANs Cisco", "Mme. Moreau", "Labo Réseau", "TP", "ING1", "ING1-S5", C_LIGHTBLUE)

        # ING2
        add_c(monday, 0, "08h00", "10h00", "Méthodologies Agiles : TDD & BDD", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Architecture Logicielle : Domain Driven Design", "Mme. Martin", "Amphi A", "CM", "ING2", "ING2-S7", C_TEAL)
        add_c(monday, 0, "13h15", "17h30", "Hackathon Agile : Sprint Marathon 24h", "M. Dupont", "Salle Projet", "Projet", "ING2", "ING2-S7", C_GREEN)
        add_c(monday, 1, "08h00", "10h00", "Anglais Pro : Négociation & Contrat", "Mme. Smith", "Salle C101", "TD", "ING2", "ING2-S7", C_PURPLE)
        add_c(monday, 1, "10h15", "12h15", "Web Fullstack : Intégration React & State", "M. Leclerc", "Labo Info 1", "TP", "ING2", "ING2-S7", C_ORANGE)
        add_c(monday, 1, "13h15", "15h15", "Sécurité : Cryptographie & SSL", "M. Bernard", "Amphi B", "CM", "ING2", "ING2-S7", C_RED)
        add_c(monday, 2, "08h00", "10h00", "Réseaux : Pare-feu & Filtrage (iptables)", "Mme. Moreau", "Salle B105", "CM", "ING2", "ING2-S7", C_LIGHTBLUE)
        add_c(monday, 2, "10h15", "12h15", "Projet Agile : Démo Prototype Hackathon", "M. Dupont", "Salle Projet", "Projet", "ING2", "ING2-S7", C_GREEN)
        add_c(monday, 3, "08h00", "10h00", "DevOps : Pipelines CI/CD Automatisés", "M. Thomas", "Labo Info 2", "TP", "ING2", "ING2-S7", C_SLATE)
        add_c(monday, 3, "10h15", "12h15", "Gestion Budgétaire & Rentabilité Logicielle", "Mme. Petit", "Salle A201", "TD", "ING2", "ING2-S7", C_VIOLET)
        add_c(monday, 3, "13h15", "15h15", "IA : Apprentissage Supervisé Scikit-Learn", "M. Roux", "Amphi A", "CM", "ING2", "ING2-S7", C_PINK)
        add_c(monday, 4, "08h00", "10h00", "Atelier Agile : Revue Code SonarQube", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Conférence : Retours d'Expérience Scale-up", "Invités", "Grand Amphi", "Conférence", "ING2", "ING2-S7", C_CYAN)

        # ING3
        add_c(monday, 0, "08h00", "10h00", "Kubernetes : Ingress & Helm Charts", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_SLATE)
        add_c(monday, 0, "10h15", "12h15", "Deep Learning : Réseaux Convolutifs (CNN)", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 0, "13h15", "15h15", "Microservices : Service Mesh Istio", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_LIGHTBLUE)
        add_c(monday, 1, "08h00", "10h00", "Audit de Sécurité & Conformité Cloud", "M. Bernard", "Salle A202", "TD", "ING3", "ING3-S9", C_RED)
        add_c(monday, 1, "10h15", "12h15", "Innovation : Méthode Lean Startup", "Mme. Petit", "Salle A202", "CM", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 1, "13h15", "15h15", "IA Générative : Agents Autonomes & LangChain", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 2, "08h00", "10h00", "Cybersécurité : SIEM & Détection Intrusion", "M. Bernard", "Labo Sécu", "TP", "ING3", "ING3-S9", C_RED)
        add_c(monday, 2, "10h15", "12h15", "Architecture Cloud Native & 12-Factor", "Mme. Martin", "Salle A202", "CM", "ING3", "ING3-S9", C_TEAL)
        add_c(monday, 3, "08h00", "12h15", "PFE : Soutenance Intermédiaire Mi-Parcours", "Tuteurs", "Grand Amphi", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "13h15", "15h15", "Stratégie Go-To-Market & Acquisition", "Mme. Petit", "Salle A202", "TD", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 4, "10h15", "12h15", "Droit des Contrats Informatiques & SaaS", "Mme. Smith", "Amphi B", "CM", "ING3", "ING3-S9", C_PURPLE)
        add_c(monday, 4, "13h15", "15h15", "Table Ronde : Métiers de l'Ingénierie", "Intervenants", "Grand Amphi", "Conférence", "ING3", "ING3-S9", C_CYAN)

    # ----------------------------------------------------
    # SEMAINE 15 (07/12 - 11/12) : EXAMENS PARTIELS S1
    # ----------------------------------------------------
    elif week_num == 15:
        # CP1
        add_c(monday, 0, "08h00", "10h00", "Partiel : Mathématiques Algèbre", "M. Legrand", "Amphi B", "Examen", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 1, "08h00", "10h00", "Partiel : Physique Mécanique", "Mme. Renard", "Amphi B", "Examen", "CP1", "CP1-A", C_TEAL)
        add_c(monday, 2, "10h15", "12h15", "Partiel sur Machine : Algorithmique C", "M. Robert", "Labo Info 1", "Examen", "CP1", "CP1-A", C_ORANGE)
        add_c(monday, 3, "13h15", "15h15", "Partiel Écrit : Anglais LV1", "Mme. Smith", "Salle C102", "Examen", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 4, "08h00", "10h00", "Partiel : Électronique Fondamentale", "M. Blanc", "Amphi B", "Examen", "CP1", "CP1-A", C_LIGHTBLUE)

        # CP2
        add_c(monday, 0, "10h15", "12h15", "Partiel : Mathématiques Analyse", "M. Legrand", "Amphi A", "Examen", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 1, "10h15", "12h15", "Partiel sur Machine : C++", "M. Leclerc", "Labo Info 2", "Examen", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 2, "08h00", "10h00", "Partiel : Électromagnétisme", "Mme. Renard", "Amphi B", "Examen", "CP2", "CP2-A", C_TEAL)
        add_c(monday, 3, "10h15", "12h15", "Partiel : Thermodynamique", "M. Blanc", "Salle B102", "Examen", "CP2", "CP2-A", C_GOLD)
        add_c(monday, 4, "10h15", "12h15", "Partiel : Optique Ondulatoire", "M. Roux", "Labo Physique", "Examen", "CP2", "CP2-A", C_PURPLE)

        # ING1
        add_c(monday, 0, "08h00", "10h00", "Partiel sur Machine : POO & Java", "M. Robert", "Labo Info 1", "Examen", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Partiel : Architecture Ordinateurs", "Mme. Martin", "Amphi A", "Examen", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 2, "10h15", "12h15", "Partiel Pratique : Bases de Données SQL", "M. Leclerc", "Labo Info 3", "Examen", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 3, "08h00", "10h00", "Partiel : Génie Logiciel & Design Patterns", "M. Dupont", "Salle B204", "Examen", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 4, "13h15", "15h15", "Partiel Pratique : Réseaux Locaux", "Mme. Moreau", "Labo Réseau", "Examen", "ING1", "ING1-S5", C_LIGHTBLUE)

        # ING2
        add_c(monday, 0, "08h00", "10h00", "Partiel : Méthodologies Agiles & Scrum", "M. Dupont", "Salle B204", "Examen", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Partiel : Architecture Logicielle & DDD", "Mme. Martin", "Amphi A", "Examen", "ING2", "ING2-S7", C_TEAL)
        add_c(monday, 1, "10h15", "12h15", "Partiel sur Machine : Dev Web Fullstack", "M. Leclerc", "Labo Info 1", "Examen", "ING2", "ING2-S7", C_ORANGE)
        add_c(monday, 1, "13h15", "15h15", "Partiel : Sécurité Informatique", "M. Bernard", "Amphi B", "Examen", "ING2", "ING2-S7", C_RED)
        add_c(monday, 2, "08h00", "10h00", "Partiel : Réseaux & Protocoles", "Mme. Moreau", "Salle B105", "Examen", "ING2", "ING2-S7", C_LIGHTBLUE)
        add_c(monday, 3, "08h00", "10h00", "Partiel Pratique : DevOps & CI/CD", "M. Thomas", "Labo Info 2", "Examen", "ING2", "ING2-S7", C_SLATE)
        add_c(monday, 3, "13h15", "15h15", "Partiel : Intelligence Artificielle", "M. Roux", "Amphi A", "Examen", "ING2", "ING2-S7", C_PINK)

        # ING3
        add_c(monday, 0, "08h00", "10h00", "Partiel Pratique : Cloud & Kubernetes", "M. Thomas", "Labo Cloud", "Examen", "ING3", "ING3-S9", C_SLATE)
        add_c(monday, 0, "10h15", "12h15", "Partiel : Big Data & Machine Learning", "M. Roux", "Amphi A", "Examen", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 1, "10h15", "12h15", "Partiel : Management de l'Innovation", "Mme. Petit", "Salle A202", "Examen", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 2, "08h00", "10h00", "Partiel Pratique : Cybersécurité Avancée", "M. Bernard", "Labo Sécu", "Examen", "ING3", "ING3-S9", C_RED)
        add_c(monday, 4, "10h15", "12h15", "Partiel : Droit & Éthique du Numérique", "Mme. Smith", "Amphi B", "Examen", "ING3", "ING3-S9", C_PURPLE)

    # ----------------------------------------------------
    # SEMAINE 16 (14/12 - 18/12) : JURYS & SOUTENANCES
    # ----------------------------------------------------
    elif week_num == 16:
        # CP1
        add_c(monday, 0, "08h00", "10h00", "Bilan Pédagogique Mathématiques", "M. Legrand", "Salle CP1", "TD", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 1, "08h00", "10h00", "Présentation Mini-Projets Info", "M. Robert", "Labo Info 1", "Projet", "CP1", "CP1-A", C_ORANGE)
        add_c(monday, 2, "10h15", "12h15", "Synthèse Chimie & Posters", "Mme. Simon", "Labo Chimie", "TP", "CP1", "CP1-A", C_GOLD)
        add_c(monday, 3, "13h15", "15h15", "Évaluation Orale Anglais", "Mme. Smith", "Salle C102", "TD", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 4, "10h15", "12h15", "Bilan Semestriel CP1", "M. Blanc", "Salle CP1", "TD", "CP1", "CP1-A", C_CYAN)

        # CP2
        add_c(monday, 0, "10h15", "12h15", "Soutenance Projet C++", "M. Leclerc", "Labo Info 2", "Projet", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 1, "10h15", "12h15", "Correction Électromagnétisme", "Mme. Renard", "Amphi B", "CM", "CP2", "CP2-A", C_TEAL)
        add_c(monday, 3, "13h15", "15h15", "Grand Jury : Projet de Conception", "Mme. Simon", "Salle Projet", "Projet", "CP2", "CP2-A", C_GREEN)
        add_c(monday, 4, "10h15", "12h15", "Clôture Semestre & Orientation", "M. Legrand", "Salle B102", "Conférence", "CP2", "CP2-A", C_BLUE)

        # ING1
        add_c(monday, 0, "08h00", "10h00", "Soutenance Projet Java & Architecture", "M. Robert", "Labo Info 1", "Projet", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 2, "10h15", "12h15", "Restitution Projet SQL & Web", "M. Leclerc", "Labo Info 3", "Projet", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 3, "13h15", "15h15", "Soutenance Projet Transversal S5", "M. Dupont", "Salle Projet", "Projet", "ING1", "ING1-S5", C_GREEN)
        add_c(monday, 4, "13h15", "15h15", "Bilan Semestre 5 & Stage Ouvrier", "Mme. Moreau", "Salle B201", "Conférence", "ING1", "ING1-S5", C_LIGHTBLUE)

        # ING2
        add_c(monday, 0, "08h00", "10h00", "Rétrospective Finale & Démo Agile", "M. Dupont", "Salle B204", "Projet", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 1, "10h15", "12h15", "Soutenance Projet Web Fullstack", "M. Leclerc", "Labo Info 1", "Projet", "ING2", "ING2-S7", C_ORANGE)
        add_c(monday, 2, "10h15", "12h15", "Grand Jury Agile : Démo Finale", "M. Dupont", "Salle Projet", "Projet", "ING2", "ING2-S7", C_GREEN)
        add_c(monday, 3, "08h00", "10h00", "Restitution Pipeline DevOps & Qualité", "M. Thomas", "Labo Info 2", "TP", "ING2", "ING2-S7", C_SLATE)
        add_c(monday, 4, "10h15", "12h15", "Cérémonie de Clôture S7 & Prix Agiles", "Invités", "Grand Amphi", "Conférence", "ING2", "ING2-S7", C_CYAN)

        # ING3
        add_c(monday, 0, "08h00", "12h15", "Grand Jury PFE - Sessions Matin", "Tuteurs", "Grand Amphi", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 1, "08h00", "12h15", "Grand Jury PFE - Sessions Après-midi", "Tuteurs", "Grand Amphi", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "08h00", "12h15", "Délibérations Jury PFE & Validation", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 4, "10h15", "12h15", "Cérémonie de Départ en Stage PFE", "Direction EILCO", "Grand Amphi", "Conférence", "ING3", "ING3-S9", C_CYAN)

    # ----------------------------------------------------
    # AUTRES SEMAINES (2, 3, 5, 7, 8, 10, 11, 12, 13, 14) :
    # VARIATIONS PROGRESSIVES
    # ----------------------------------------------------
    else:
        sprint_idx = ((week_num - 1) % 4) + 1
        is_even = (week_num % 2 == 0)

        # CP1
        alg_topics = ["Espaces Vectoriels", "Applications Linéaires", "Matrices & Déterminants", "Systèmes Linéaires", "Diagonalisation", "Polynômes"]
        phys_topics = ["Dynamique du Point", "Travail & Énergie", "Oscillateurs Harmoniques", "Moment Cinétique", "Gravitation", "Thermodynamique du Point"]
        cp1_alg = alg_topics[week_num % len(alg_topics)]
        cp1_phys = phys_topics[week_num % len(phys_topics)]

        add_c(monday, 0, "08h00", "10h00", f"Mathématiques : Algèbre - {cp1_alg}", "M. Legrand", "Salle CP1", "CM", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", f"Physique : {cp1_phys}", "Mme. Renard", "Amphi B", "TD", "CP1", "CP1-A", C_TEAL)
        add_c(monday, 1, "08h00", "10h00", f"TP Algorithmique : Séance {week_num}", "M. Robert", "Labo Info 1", "TP", "CP1", "CP1-A", C_ORANGE)
        if is_even:
            add_c(monday, 1, "10h15", "12h15", "Optique Géométrique : TP Expérimental", "M. Roux", "Labo Physique", "TP", "CP1", "CP1-A", C_PURPLE)
        else:
            add_c(monday, 1, "10h15", "12h15", "Optique Géométrique : CM & Exercices", "M. Roux", "Amphi B", "CM", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "Expression & Communication Professionnelle", "Mme. Petit", "Salle C102", "TD", "CP1", "CP1-A", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", f"Chimie Générale : TP Séance {week_num}", "Mme. Simon", "Labo Chimie", "TP", "CP1", "CP1-A", C_GOLD)
        add_c(monday, 3, "10h15", "12h15", "Mathématiques : Analyse 1 - Exercices", "M. Legrand", "Salle CP1", "TD", "CP1", "CP1-A", C_BLUE)
        add_c(monday, 3, "13h15", "15h15", "Anglais LV1 : Compréhension & Débat", "Mme. Smith", "Salle C102", "TD", "CP1", "CP1-A", C_PURPLE)
        add_c(monday, 4, "08h00", "10h00", "Électronique Fondamentale : Circuits RLC", "M. Blanc", "Labo Elec 1", "CM", "CP1", "CP1-A", C_LIGHTBLUE)
        add_c(monday, 4, "10h15", "12h15", "Tutorat & Travaux en Autonomie", "M. Blanc", "Salle CP1", "TD", "CP1", "CP1-A", C_CYAN)

        # CP2
        add_c(monday, 0, "08h00", "10h00", f"Mathématiques : Analyse (Semaine {week_num})", "M. Legrand", "Amphi A", "CM", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", f"Programmation C++ : TP Séance {week_num}", "M. Leclerc", "Labo Info 2", "TP", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 1, "08h00", "10h00", "Électronique Analogique : Montages AOP", "M. Blanc", "Labo Elec 2", "TP", "CP2", "CP2-A", C_LIGHTBLUE)
        add_c(monday, 1, "10h15", "12h15", "Électromagnétisme : Ondes & Maxwell", "Mme. Renard", "Amphi B", "CM", "CP2", "CP2-A", C_TEAL)
        add_c(monday, 2, "08h00", "10h00", "Thermodynamique : Entropie & Potentiels", "M. Blanc", "Salle B102", "TD", "CP2", "CP2-A", C_GOLD)
        add_c(monday, 2, "10h15", "12h15", "Structures de Données : Pointeurs & Récursivité", "M. Robert", "Labo Info 2", "TP", "CP2", "CP2-A", C_ORANGE)
        add_c(monday, 3, "10h15", "12h15", "Anglais LV1 : Préparation TOEIC", "Mme. Smith", "Salle C101", "TD", "CP2", "CP2-A", C_PURPLE)
        add_c(monday, 3, "13h15", "15h15", f"Projet de Conception : Atelier CAO (S{week_num})", "Mme. Simon", "Salle Projet", "Projet", "CP2", "CP2-A", C_GREEN)
        add_c(monday, 4, "08h00", "10h00", "Mathématiques : Algèbre 2 - Formes Quadratiques", "M. Legrand", "Salle B102", "TD", "CP2", "CP2-A", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", "Optique Ondulatoire : Cohérence & Franges", "M. Roux", "Labo Physique", "TP", "CP2", "CP2-A", C_PURPLE)

        # ING1
        java_themes = ["Collections & Streams", "Threads & Concurrence", "Sockets & Réseaux", "JavaFX / UI", "Tests Unitaires JUnit"]
        java_theme = java_themes[week_num % len(java_themes)]

        add_c(monday, 0, "08h00", "10h00", f"POO & Java : {java_theme}", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 0, "10h15", "12h15", "Systèmes & Linux : Gestion des Processus & IPC", "M. Thomas", "Salle B201", "TD", "ING1", "ING1-S5", C_SLATE)
        add_c(monday, 0, "13h15", "15h15", f"Algorithmique Avancée : Session {week_num}", "M. Leclerc", "Labo Info 2", "TP", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "08h00", "10h00", "Architecture Ordinateurs : Jeu d'instructions RISC-V", "Mme. Martin", "Amphi A", "CM", "ING1", "ING1-S5", C_TEAL)
        add_c(monday, 1, "10h15", "12h15", "Mathématiques pour l'Ingénieur : Optimisation", "M. Legrand", "Salle B201", "TD", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 1, "13h15", "15h15", "Anglais Technique : Synthèse d'Articles IT", "Mme. Smith", "Salle C102", "TD", "ING1", "ING1-S5", C_PURPLE)
        add_c(monday, 2, "08h00", "10h00", "Droit du Travail & Propriété Intellectuelle", "Mme. Petit", "Salle B201", "TD", "ING1", "ING1-S5", C_VIOLET)
        add_c(monday, 2, "10h15", "12h15", f"Bases de Données SQL : TP Séance {week_num}", "M. Leclerc", "Labo Info 3", "TP", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 3, "08h00", "10h00", "Génie Logiciel : Modélisation & Qualité", "M. Dupont", "Salle B204", "CM", "ING1", "ING1-S5", C_BLUE)
        add_c(monday, 3, "10h15", "12h15", "Programmation Web : API REST & Fetch", "M. Robert", "Labo Info 1", "TP", "ING1", "ING1-S5", C_ORANGE)
        add_c(monday, 4, "10h15", "12h15", "Probabilités : Variables Multidimensionnelles", "Mme. Renard", "Salle B201", "TD", "ING1", "ING1-S5", C_GOLD)
        add_c(monday, 4, "13h15", "15h15", "Réseaux : Analyse de Trames & Protocoles", "Mme. Moreau", "Labo Réseau", "TP", "ING1", "ING1-S5", C_LIGHTBLUE)

        # ING2
        agile_step = f"Sprint {sprint_idx} - " + ("Planification & Standup" if is_even else "Développement & Revue")
        web_topic = ["API REST & Express", "State Management & React", "Sécurité Web & Auth", "Optimisation & Déploiement"][week_num % 4]
        sec_topic = ["Cryptographie Symétrique", "Attaques Réseaux (MITM)", "Sécurité des Conteneurs", "Gestion des Identités IAM"][week_num % 4]

        add_c(monday, 0, "08h00", "10h00", f"Méthodologies Agiles : {agile_step}", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 0, "10h15", "12h15", "Architecture Logicielle : Design Patterns & SOLID", "Mme. Martin", "Amphi A", "CM", "ING2", "ING2-S7", C_TEAL)
        add_c(monday, 0, "13h15", "15h15", f"Base de Données Avancées : NoSQL & Indexation (TP {week_num})", "M. Robert", "Labo Info 3", "TP", "ING2", "ING2-S7", C_GOLD)
        add_c(monday, 1, "08h00", "10h00", "Anglais Professionnel : Réunion Agile en Anglais", "Mme. Smith", "Salle C101", "TD", "ING2", "ING2-S7", C_PURPLE)
        add_c(monday, 1, "10h15", "12h15", f"Développement Web : {web_topic}", "M. Leclerc", "Labo Info 1", "TP", "ING2", "ING2-S7", C_ORANGE)
        add_c(monday, 1, "13h15", "15h15", f"Sécurité Informatique : {sec_topic}", "M. Bernard", "Amphi B", "CM", "ING2", "ING2-S7", C_RED)
        add_c(monday, 2, "08h00", "10h00", "Réseaux & Protocoles : Architecture Client-Serveur", "Mme. Moreau", "Salle B105", "CM", "ING2", "ING2-S7", C_LIGHTBLUE)
        add_c(monday, 2, "10h15", "12h15", f"Projet Agile : Itération Sprint {sprint_idx}", "M. Dupont", "Salle Projet", "Projet", "ING2", "ING2-S7", C_GREEN)
        add_c(monday, 3, "08h00", "10h00", f"DevOps : Pipeline CI/CD & Docker Compose (TP {week_num})", "M. Thomas", "Labo Info 2", "TP", "ING2", "ING2-S7", C_SLATE)
        add_c(monday, 3, "10h15", "12h15", "Gestion de Projet : Suivi des Coûts & Burndown", "Mme. Petit", "Salle A201", "TD", "ING2", "ING2-S7", C_VIOLET)
        add_c(monday, 3, "13h15", "15h15", f"Intelligence Artificielle : Séance {week_num}", "M. Roux", "Amphi A", "CM", "ING2", "ING2-S7", C_PINK)
        add_c(monday, 4, "08h00", "10h00", "Atelier Méthodes Agiles : Rétrospective & Kaizen", "M. Dupont", "Salle B204", "TD", "ING2", "ING2-S7", C_BLUE)
        add_c(monday, 4, "10h15", "12h15", f"Conférences & Retours d'Expérience (Édition {week_num})", "Invités", "Grand Amphi", "Conférence", "ING2", "ING2-S7", C_CYAN)

        # ING3
        cloud_topic = ["Déploiement Helm & Secrets", "Monitoring Prometheus & Grafana", "Stockage Persistant Ceph", "Autoscaling & Ingress"][week_num % 4]
        ai_topic = ["Réseaux Récurrents (LSTM)", "Transformers & Attention", "Apprentissage par Renforcement", "Vision par Ordinateur"][week_num % 4]

        add_c(monday, 0, "08h00", "10h00", f"Cloud & Kubernetes : {cloud_topic}", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_SLATE)
        add_c(monday, 0, "10h15", "12h15", f"Big Data & AI : {ai_topic}", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 0, "13h15", "15h15", f"Microservices & Event-Driven (TP {week_num})", "M. Thomas", "Labo Cloud", "TP", "ING3", "ING3-S9", C_LIGHTBLUE)
        add_c(monday, 1, "08h00", "10h00", "Gouvernance IT : Gestion des Risques EBIOS", "M. Bernard", "Salle A202", "TD", "ING3", "ING3-S9", C_RED)
        add_c(monday, 1, "10h15", "12h15", "Management de l'Innovation : Agil'Échelle", "Mme. Petit", "Salle A202", "CM", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 1, "13h15", "15h15", "IA Générative : Embeddings & Vector DBs", "M. Roux", "Amphi A", "CM", "ING3", "ING3-S9", C_PINK)
        add_c(monday, 2, "08h00", "10h00", f"Cybersécurité Avancée : Lab Sécurité {week_num}", "M. Bernard", "Labo Sécu", "TP", "ING3", "ING3-S9", C_RED)
        add_c(monday, 2, "10h15", "12h15", "Architecture d'Entreprise : Intégration SOA", "Mme. Martin", "Salle A202", "CM", "ING3", "ING3-S9", C_TEAL)
        add_c(monday, 3, "08h00", "10h00", f"PFE : Session de Travail {week_num}", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "10h15", "12h15", f"PFE : Encadrement Technique {week_num}", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)
        add_c(monday, 3, "13h15", "15h15", "Entrepreneuriat & Stratégie Commerciale", "Mme. Petit", "Salle A202", "TD", "ING3", "ING3-S9", C_VIOLET)
        add_c(monday, 4, "10h15", "12h15", "Droit du Numérique & Cyber-législation", "Mme. Smith", "Amphi B", "CM", "ING3", "ING3-S9", C_PURPLE)
        add_c(monday, 4, "13h15", "15h15", f"Suivi de Projet PFE : Point Sprint {sprint_idx}", "Tuteurs", "Salle Projet", "Projet", "ING3", "ING3-S9", C_GREEN)

print(f"Total courses generated: {len(all_courses)}")
with open("cours.json", "w", encoding="utf-8") as f:
    json.dump(all_courses, f, ensure_ascii=False, indent=2)

print("cours.json written successfully!")
