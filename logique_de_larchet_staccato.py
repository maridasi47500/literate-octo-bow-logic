import re

# --- CONFIGURATION INITIALE ---
BPM = 120  

DUREE_FACTEURS = {
    '1': 4.0,
    '2': 2.0,
    '4': 1.0,
    '8': 0.5,
    '16': 0.25,
    '32': 0.125
}

# Configuration des coefficients d'articulation
COEFF_ARTICULATIONS = {
    'staccatissimo': 0.25,
    'staccato': 0.5,
    'tenuto': 0.75,
    'normal': 1.0
}

note_names = [
    'aes', 'bes', 'ces', 'des', 'ees', 'fes', 'ges',
    'ais', 'bis', 'cis', 'dis', 'eis', 'fis', 'gis',
    'as', 'bs', 'cs', 'ds', 'es', 'fs', 'gs',
    'a', 'b', 'c', 'd', 'e', 'f', 'g'
]
note_pattern = '|'.join(sorted(note_names, key=len, reverse=True))

# REGEX MODIFIÉE : On capture désormais les articulations post-fixées (ex: c4-. ou c4\staccato)
NOTE_REGEX = rf"\b({note_pattern})('*)(?:([0-9]+))?(\.)?(\~)?(?:\\(staccatissimo|staccato|tenuto)|(-\.|-\||--))?"

def calculer_duree_reelle(duree_ly, a_point, articulation, bpm):
    """Calcule la durée réelle en secondes en incluant le coefficient d'articulation."""
    facteur_noire = DUREE_FACTEURS.get(duree_ly, 1.0)
    if a_point:
        facteur_noire *= 1.5
    
    temps_par_noire = 60.0 / bpm
    durée_brute = facteur_noire * temps_par_noire
    
    # Application du multiplicateur selon l'articulation détectée
    coeff = COEFF_ARTICULATIONS.get(articulation, 1.0)
    return durée_brute * coeff, durée_brute

def simuler_physique_archet(direction, duree_reelle, articulation):
    """Simule la pression, vitesse et longueur d'archet selon l'articulation."""
    # Base de calcul
    longueur = min(100.0, duree_reelle * 40.0)
    
    # Ajustements physiques selon l'articulation
    if articulation == 'staccatissimo':
        pression = 75  # Attaque forte et brève
        vitesse = longueur / max(0.05, duree_reelle) * 1.5
    elif articulation == 'staccato':
        pression = 65
        vitesse = longueur / max(0.05, duree_reelle) * 1.2
    elif articulation == 'tenuto':
        pression = 45  # Plus doux, lissé sur toute la longueur
        vitesse = longueur / max(0.1, duree_reelle)
    else:
        pression = 50 + (5 if direction == "\\downbow" else -5)
        vitesse = longueur / max(0.1, duree_reelle)
        
    return {
        "pression": round(pression, 2),
        "vitesse": round(vitesse, 2),
        "longueur_archet_pct": round(longueur, 2)
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
            
            # Identification de l'articulation (via texte ou via raccourci comme -. ou --)
            articulation_texte = match.group(6)
            articulation_signe = match.group(7)
            
            type_articulation = 'normal'
            if articulation_texte:
                type_articulation = articulation_texte
            elif articulation_signe == '-.':
                type_articulation = 'staccato'
            elif articulation_signe == '-\\|':
                type_articulation = 'staccatissimo'
            elif articulation_signe == '--':
                type_articulation = 'tenuto'

            if duree:
                derniere_duree = duree
            else:
                duree = derniere_duree
                
            # Calcul des durées (avec et sans coefficient)
            duree_articulee, duree_nominale = calculer_duree_reelle(duree, point, type_articulation, bpm)
            
            physique = simuler_physique_archet(sens_archet_actuel, duree_articulee, type_articulation)
            
            note_hash = {
                "note": f"{nom_note}{octave}",
                "durée_lilypond": f"{duree}{'.' if point else ''}",
                "articulation": type_articulation,
                "durée_nominale_secondes": round(duree_nominale, 3),
                "durée_réelle_articulée_secondes": round(duree_articulee, 3),
                "archet": sens_archet_actuel,
                "pression": physique["pression"],
                "vitesse": physique["vitesse"],
                "longueur_archet_utilisee": physique["longueur_archet_pct"],
                "dans_liaison": is_slur or liaison_prolongation
            }
            
            liste_notes_analysees.append(note_hash)
            
            # Gestion du sens d'archet
            if not liaison_prolongation:
                if not is_slur or (is_slur and idx == len(notes_dans_token) - 1):
                    sens_archet_actuel = "\\upbow" if sens_archet_actuel == "\\downbow" else "\\downbow"
                    
    return liste_notes_analysees

# --- TEST DU SCRIPT ---
if __name__ == "__main__":
    # Test avec une note staccatissimo ( rousseau / signe ), staccato, tenuto et normale
    exemple_score = "c'4-\\staccatissimo d'4-. e'4-- f'4"
    
    resultat = analyser_et_générer_hashes(exemple_score, BPM)
    
    import json
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
