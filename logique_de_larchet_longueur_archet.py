import re

# --- CONFIGURATION INITIALE ---
BPM = 120  

DUREE_FACTEURS = {
    '1': 4.0, '2': 2.0, '4': 1.0, '8': 0.5, '16': 0.25, '32': 0.125
}

COEFF_ARTICULATIONS = {
    'staccatissimo': 0.25, 'staccato': 0.5, 'tenuto': 0.75, 'normal': 1.0
}

# Cartographie des zones d'archet (en % de l'archet, du talon 0% à la pointe 100%)
ZONES_ARCHET = {
    'G.':   {"nom": "Tout archet",         "debut": 0,   "fin": 100},
    'H.':   {"nom": "Moitié",              "debut": 25,  "fin": 75},
    'u.H.': {"nom": "Moitié inférieure",    "debut": 0,   "fin": 50},
    'o.H.': {"nom": "Moitié supérieure",    "debut": 50,  "fin": 100},
    'Fr.':  {"nom": "Talon (un tiers)",    "debut": 0,   "fin": 33},
    'Sp.':  {"nom": "Pointe (un tiers)",   "debut": 66,  "fin": 100},
    'M.':   {"nom": "Milieu (un tiers)",   "debut": 33,  "fin": 66},
}

note_names = [
    'aes', 'bes', 'ces', 'des', 'ees', 'fes', 'ges',
    'ais', 'bis', 'cis', 'dis', 'eis', 'fis', 'gis',
    'as', 'bs', 'cs', 'ds', 'es', 'fs', 'gs',
    'a', 'b', 'c', 'd', 'e', 'f', 'g'
]
note_pattern = '|'.join(sorted(note_names, key=len, reverse=True))

# REGEX ENRICHIE : Captures des articulations ET des markups de texte LilyPond du type ^"G." ou _"M."
# Groupes de capture importants :
# group(6) -> articulation texte (\staccato)
# group(7) -> articulation signe (-.)
# group(8) -> zone d'archet (-"G.", ^"o.H.", etc.)
NOTE_REGEX = rf"\b({note_pattern})('*)(?:([0-9]+))?(\.)?(\~)?(?:\\(staccatissimo|staccato|tenuto)|(-\.|-\||--))?(?:[-_^]\"(G\.|H\.|u\.H\.|o\.H\.|Fr\.|Sp\.|M\.|u\.H)|[^\s()]+)?"

def calculer_duree_reelle(duree_ly, a_point, articulation, bpm):
    facteur_noire = DUREE_FACTEURS.get(duree_ly, 1.0)
    if a_point: facteur_noire *= 1.5
    temps_par_noire = 60.0 / bpm
    durée_brute = facteur_noire * temps_par_noire
    coeff = COEFF_ARTICULATIONS.get(articulation, 1.0)
    return durée_brute * coeff, durée_brute

def simuler_physique_archet(direction, duree_reelle, articulation, code_zone):
    """Calcule la physique de l'archet en fonction de l'articulation et de la zone imposée."""
    # Si une zone spécifique est demandée, on se base sur ses limites réelles
    if code_zone in ZONES_ARCHET:
        zone = ZONES_ARCHET[code_zone]
        longueur = zone["fin"] - zone["debut"]
        # En fonction du sens, le point de départ change (0 = talon, 100 = pointe)
        pos_depart = zone["debut"] if direction == "\\downbow" else zone["fin"]
        pos_fin = zone["fin"] if direction == "\\downbow" else zone["debut"]
    else:
        # Logique par défaut si aucune zone n'est spécifiée
        longueur = min(100.0, duree_reelle * 40.0)
        pos_depart = 0 if direction == "\\downbow" else longueur
        pos_fin = longueur if direction == "\\downbow" else 0

    # Ajustement de la vitesse et de la pression selon l'articulation
    if articulation == 'staccatissimo':
        pression = 75
        vitesse = longueur / max(0.05, duree_reelle) * 1.5
    elif articulation == 'staccato':
        pression = 65
        vitesse = longueur / max(0.05, duree_reelle) * 1.2
    elif articulation == 'tenuto':
        pression = 45
        vitesse = longueur / max(0.1, duree_reelle)
    else:
        pression = 50 + (5 if direction == "\\downbow" else -5)
        vitesse = longueur / max(0.1, duree_reelle)
        
    return {
        "pression": round(pression, 2),
        "vitesse": round(vitesse, 2),
        "longueur_archet_pct": round(longueur, 2),
        "zone_depart_pct": pos_depart,
        "zone_fin_pct": pos_fin
    }

def analyser_et_générer_hashes(score_text, bpm):
    score_clean = re.sub(r'\\slur[A-Za-z]+', '', score_text)
    tokens = re.findall(r'\([^)]+\)|[^\s()]+', score_clean)
    
    liste_notes_analysees = []
    sens_archet_actuel = "\\downbow"
    derniere_duree = "4"
    
    for token in tokens:
        is_slur = token.startswith('(') and token.endswith(')')
        content = token[1:-1] if is_slur else token
        
        notes_dans_token = list(re.finditer(NOTE_REGEX, content))
        
        for idx, match in enumerate(notes_dans_token):
            nom_note = match.group(1)
            octave = match.group(2)
            duree = match.group(3)
            point = match.group(4) is not None
            liaison_prolongation = match.group(5) is not None
            
            # 1. Extraction Articulation
            articulation_texte = match.group(6)
            articulation_signe = match.group(7)
            type_articulation = 'normal'
            if articulation_texte:   type_articulation = articulation_texte
            elif articulation_signe == '-.':   type_articulation = 'staccato'
            elif articulation_signe == '-\\|': type_articulation = 'staccatissimo'
            elif articulation_signe == '--':   type_articulation = 'tenuto'

            # 2. Extraction Zone d'archet (ex: "G.", "M.", etc.)
            # On nettoie la chaîne si elle a matché l'une des zones connues
            zone_detectee = None
            for code in ZONES_ARCHET.keys():
                if f'"{code}"' in match.group(0):
                    zone_detectee = code
                    break

            if duree:  derniere_duree = duree
            else:      duree = derniere_duree
                
            duree_articulee, duree_nominale = calculer_duree_reelle(duree, point, type_articulation, bpm)
            physique = simuler_physique_archet(sens_archet_actuel, duree_articulee, type_articulation, zone_detectee)
            
            note_hash = {
                "note": f"{nom_note}{octave}",
                "durée_lilypond": f"{duree}{'.' if point else ''}",
                "articulation": type_articulation,
                "zone_archet_demandee": ZONES_ARCHET[zone_detectee]["nom"] if zone_detectee else "Non spécifiée",
                "durée_nominale_secondes": round(duree_nominale, 3),
                "durée_réelle_articulée_secondes": round(duree_articulee, 3),
                "archet_direction": sens_archet_actuel,
                "physique_archet": {
                    "pression": physique["pression"],
                    "vitesse_relative": physique["vitesse"],
                    "longueur_utilisee_pct": physique["longueur_archet_pct"],
                    "point_contact_depart_pct": physique["zone_depart_pct"],
                    "point_contact_fin_pct": physique["zone_fin_pct"]
                },
                "dans_liaison": is_slur or liaison_prolongation
            }
            
            liste_notes_analysees.append(note_hash)
            
            if not liaison_prolongation:
                if not is_slur or (is_slur and idx == len(notes_dans_token) - 1):
                    sens_archet_actuel = "\\upbow" if sens_archet_actuel == "\\downbow" else "\\downbow"
                    
    return liste_notes_analysees

# --- TEST AVEC LES ZONES D'ARCHET ---
if __name__ == "__main__":
    # Test LilyPond avec articulations mixtes et zones d'archets (ex: Talon, Pointe, Moitié sup)
    exemple_score = "c'4-.-\"Fr.\" d'4--_\"o.H.\" e'4^\"G.\" f'2_\"M.\""
    
    resultat = analyser_et_générer_hashes(exemple_score, BPM)
    
    import json
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
