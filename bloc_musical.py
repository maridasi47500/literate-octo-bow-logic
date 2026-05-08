import re

class BlocMusical:
    def __init__(self, notes, articulation=None, bow_dir=None, sevcik="G", duration=1.0):
        self.notes = notes  # Liste des notes dans ce bloc (si liaison)
        self.articulation = articulation # staccato, staccatissimo, tenuto
        self.bow_dir = bow_dir # downbow, upbow
        self.sevcik = sevcik # G, H, uH, oH, 1/3B, M, Sp, M*
        self.duration = duration # Durée totale du bloc
def calculer_logique_archet(note_data):
    # Mapping des longueurs d'archet selon tes définitions
    sevcik_map = {
        "G": {"longueur": 1.0, "nom": "Tout l'archet"},
        "H": {"longueur": 0.5, "nom": "Moitié d'archet"},
        "uH": {"longueur": 0.5, "zone": "Talon", "nom": "Moitié inférieure"},
        "oH": {"longueur": 0.5, "zone": "Pointe", "nom": "Moitié supérieure"},
        "1/3B": {"longueur": 0.33, "nom": "Un tiers d'archet"},
        "M": {"longueur": 0.33, "zone": "Milieu", "nom": "Milieu"},
        "Sp": {"longueur": 0.33, "zone": "Pointe", "nom": "Pointe"},
        "M*": {"longueur": 0.33, "cycle": ["Milieu", "Pointe", "Talon"], "nom": "Cycle complet"}
    }

    # Calcul de la durée réelle (Articulations)
    duree_nominale = note_data['duree']
    articulation = note_data['articulation']
    
    if articulation == "spiccato":
        duree_reelle = duree_nominale * 0.5
    elif articulation == "staccato":
        duree_reelle = duree_nominale * 0.75
    elif articulation == "staccatissimo":
        duree_reelle = duree_nominale * 0.25
    else:
        duree_reelle = duree_nominale

    return {
        "duree_sonore": duree_reelle,
        "silence": duree_nominale - duree_reelle,
        "physique": sevcik_map.get(note_data['sevcik'])
    }

def calculer_physique(bloc):
    # Transformation des durées réelles selon tes règles
    facteurs = {
        "staccatissimo": 0.25,
        "spiccato": 0.5,
        "staccato": 0.75,
        "tenuto": 1.0
    }
    facteur = facteurs.get(bloc.articulation, 1.0)
    duree_sonore = bloc.duration * facteur
    silence_articulé = bloc.duration * (1 - facteur)
    
    return duree_sonore, silence_articulé

def comparer_logique(b1, b2):
    logique = []
    ds1, sil1 = calculer_physique(b1)
    ds2, sil2 = calculer_physique(b2)
    
    # Logique de vitesse (V = Distance archet / Temps sonore)
    # Si b2 est plus court mais utilise la même quantité d'archet (ex: G)
    if ds2 < ds1 and b1.sevcik == b2.sevcik:
        logique.append(f"Vitesse : Accélérez l'archet sur la 2ème note ({b2.notes[0]}) pour compenser la durée courte.")
    
    # Logique de pression (Talon vs Pointe)
    if b2.sevcik == "Sp":
        logique.append("Pression : Augmentez la pronation de l'index pour compenser la perte de poids naturel à la pointe.")
    elif b2.sevcik == "uH":
        logique.append("Pression : Allégez le bras, le poids naturel du talon suffit.")

    # Logique de point de contact
    if any(n in b1.notes[0] for n in ['g', 'a', 'b']): # Cordes graves
        logique.append("Point de contact : Éloignez l'archet du chevalet (vers la touche) pour la corde de Sol.")
    
    return logique
