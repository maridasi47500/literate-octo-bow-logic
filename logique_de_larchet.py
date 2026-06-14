import re

# --- CONFIGURATION INITIALE ---
BPM = 120  # Vitesse du morceau (Battements Par Minute)
# Base de temps pour une noire (4) = 60 secondes / BPM
# Une noire dure donc 60 / 120 = 0.5 seconde.

# Dictionnaire de conversion des durées LilyPond en facteurs de noire
# (ex: une blanche '2' vaut 2 noires, une croche '8' vaut 0.5 noire)
DUREE_FACTEURS = {
    '1': 4.0,
    '2': 2.0,
    '4': 1.0,
    '8': 0.5,
    '16': 0.25,
    '32': 0.125
}

note_names = [
    'aes', 'bes', 'ces', 'des', 'ees', 'fes', 'ges',
    'ais', 'bis', 'cis', 'dis', 'eis', 'fis', 'gis',
    'as', 'bs', 'cs', 'ds', 'es', 'fs', 'gs',
    'a', 'b', 'c', 'd', 'e', 'f', 'g'
]
note_pattern = '|'.join(sorted(note_names, key=len, reverse=True))

# Expression régulière pour capturer une note LilyPond complète avec sa durée, ses octaves, ses points et ses liaisons
# Exemple capturé : "cis''4.~" -> Note: cis, Octave: '', Durée: 4, Point: ., Liaison: ~
NOTE_REGEX = rf"\b({note_pattern})('*)(?:([0-9]+))?(\.)?(\~)?(?:\s|$)?"

def calculer_duree_reelle(duree_ly, a_point, bpm):
    """Calcule la durée en secondes d'une note selon le BPM."""
    facteur_noire = DUREE_FACTEURS.get(duree_ly, 1.0) # Par défaut noire si non spécifié
    if a_point:
        facteur_noire *= 1.5
    
    temps_par_noire = 60.0 / bpm
    return facteur_noire * temps_par_noire

def simuler_physique_archet(direction, duree_reelle):
    """
    Simule les données physiques de l'archet (pression, vitesse, longueur).
    Modifiable selon vos propres règles physiques / algorithmes.
    """
    # Exemple de logique simple : 
    # Plus la note est longue, plus on utilise de longueur d'archet
    longueur = min(100.0, duree_reelle * 40.0)  # en % de l'archet
    vitesse = longueur / max(0.1, duree_reelle) # vitesse relative
    
    # Le poussé (upbow) a souvent une pression naturelle légèrement différente du tiré (downbow)
    pression_de_base = 50 # échelle arbitraire sur 100
    pression = pression_de_base + 5 if direction == "\\downbow" else pression_de_base - 5
    
    return {
        "pression": round(pression, 2),
        "vitesse": round(vitesse, 2),
        "longueur_archet_pct": round(longueur, 2)
    }

def analyser_et_générer_hashes(score_text, bpm):
    # Étape 1 : Nettoyage grossier des balises de direction de liaison de Lilypond (ex: \slurUp)
    score_clean = re.sub(r'\\slur[A-Za-z]+', '', score_text)
    
    # Étape 2 : Extraction de tous les blocs de notes (gère les parenthèses de liaisons de Lilypond)
    # On cherche les notes individuelles ou les blocs entre parenthèses (...)
    tokens = re.findall(r'\([^)]+\)|[^\s()]+', score_clean)
    
    liste_notes_analysees = []
    sens_archet_actuel = "\\downbow" # On commence généralement en tirant
    
    derniere_duree = "4" # Valeur par défaut Lilypond si non spécifiée au début
    
    for token in tokens:
        is_slur = token.startswith('(') and token.endswith(')')
        content = token[1:-1] if is_slur else token
        
        # Trouver toutes les notes à l'intérieur de ce token (une seule si note isolée, plusieurs si liaison)
        notes_dans_token = list(re.finditer(NOTE_REGEX, content))
        
        for idx, match in enumerate(notes_dans_token):
            nom_note = match.group(1)
            octave = match.group(2)
            duree = match.group(3)
            point = match.group(4) is not None
            liaison_prolongation = match.group(5) is not None
            
            # Lilypond conserve la dernière durée spécifiée si elle est omise
            if duree:
                derniere_duree = duree
            else:
                duree = derniere_duree
                
            # Calcul du temps réel
            duree_sec = calculer_duree_reelle(duree, point, bpm)
            
            # LOGIQUE DU SENS DE L'ARCHET :
            # On change de sens d'archet SAUF SI :
            # - On est au milieu d'une liaison d'articulation (idx > 0 dans le groupe entre parenthèses)
            # - La note précédente avait une liaison de prolongation (~), gérée via l'état précédent
            
            # Génération du dictionnaire (Hash) pour la note
            physique = simuler_physique_archet(sens_archet_actuel, duree_sec)
            
            note_hash = {
                "note": f"{nom_note}{octave}",
                "durée_lilypond": f"{duree}{'.' if point else ''}",
                "durée_secondes": round(duree_sec, 3),
                "archet": sens_archet_actuel,
                "pression": physique["pression"],
                "vitesse": physique["vitesse"],
                "longueur_archet_utilisee": physique["longueur_archet_pct"],
                "dans_liaison": is_slur or liaison_prolongation
            }
            
            liste_notes_analysees.append(note_hash)
            
            # Détermination de l'archet pour la PROCHAINE note
            # Si c'est la dernière note d'une liaison d'articulation ou une note isolée, ET qu'il n'y a pas de prolongation (~)
            if not liaison_prolongation:
                if not is_slur or (is_slur and idx == len(notes_dans_token) - 1):
                    # On change de sens
                    sens_archet_actuel = "\\upbow" if sens_archet_actuel == "\\downbow" else "\\downbow"
                    
    return liste_notes_analysees

# --- EXEMPLE D'UTILISATION ---
if __name__ == "__main__":
    # Exemple de chaîne LilyPond contenant une note isolée, une liaison d'articulation et une liaison de prolongation (~)
    exemple_score = "c'4 d'8( e' f') g'4~ g'2"
    
    resultat = analyser_et_générer_hashes(exemple_score, BPM)
    
    # Affichage propre des "hashes" générés
    import json
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
