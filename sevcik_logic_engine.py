import re

class SevcikLogicEngine:
    def __init__(self):
        self.pos_actuelle = 0.0  # 0=Talon, 1=Pointe
        self.derniere_note_physique = None
def test_de_logique(script):
    # Cas test : Noire, Tout l'archet, Forte, Pointe
    res = script.analyser('c4\downbow^"Sp."^"WB"\\f')
    
    # Vérifications logiques :
    assert "Pression" in str(res) and "Index" in str(res) # Doit conseiller l'index à la pointe
    assert "Chevalet" in str(res)                        # Doit conseiller le chevalet pour un Forte
    
    # Cas test : Croche, Tout l'archet (Vitesse rapide)
    res2 = script.analyser('c8\downbow^"WB"')
    # Doit dire d'appuyer MOINS que pour la noire
    # ...
    def logique_pression_physique(position_val, nuance):
        """
        Position : 0.0 (Talon) à 1.0 (Pointe)
        Nuance : 'f', 'p', 'mf'
        """
        conseil = ""
        
        # Logique de compensation de la balance de l'archet
        if position_val < 0.2: # TALON
            conseil = "Au talon : le poids naturel est fort. Alléger la main pour ne pas écraser."
            if nuance == 'p': conseil += " (Soutenir l'archet avec le petit doigt)."
            
        elif position_val > 0.8: # POINTE
            conseil = "À la pointe : l'archet est léger. Appuyer davantage avec l'index (levier)."
            if nuance == 'f': conseil += " (Rapprocher fortement du chevalet)."
            
        else: # MILIEU
            conseil = "Au milieu : l'équilibre est naturel. Appuyer normalement avec le poids de l'avant-bras."
    
        return conseil

    def traiter_liaison(self, notes_liees):
        """
        Fusionne plusieurs notes liées en une seule 'unité d'archet'.
        Exemple : (c4 d4 e2) devient une seule unité de durée '1/1' (ronde).
        """
        duree_totale = 0
        for note in notes_liees:
            # Extraction de la valeur rythmique (4->0.25, 2->0.5, etc.)
            match = re.search(r'\d+', note)
            if match:
                duree_totale += 1.0 / int(match.group())
        
        # On garde la première note comme référence pour la direction et les symboles
        note_fusionnee = notes_liees[0]
        return {
            'brut': note_fusionnee,
            'duree_physique': duree_totale, # La durée réelle du geste
            'est_liaison': True,
            'nb_notes': len(notes_liees)
        }

    def analyser_logique(self, unite_note):
        """Calcule la logique sans montrer les chiffres."""
        # Extraction des paramètres de la note (ou de la liaison fusionnée)
        n = self._extraire_parametres(unite_note)
        conseils = []

        # 1. LOGIQUE DE VITESSE (Calculée par le script)
        # Vitesse = Longueur d'archet / Durée temporelle
        vitesse_actuelle = n['longueur_archet'] / n['duree_physique']

        # 2. LA RÈGLE D'OR : COMPARAISON VITESSE / PRESSION
        if self.derniere_note_physique:
            prev = self.derniere_note_physique
            vitesse_prev = prev['longueur_archet'] / prev['duree_physique']

            # Cas : Même longueur d'archet (ex: tout l'archet), mais durée différente
            if n['longuer_nominale'] == prev['longuer_nominale']:
                if n['duree_physique'] > prev['duree_physique']:
                    # Note plus longue (ex: Noire vs Croche)
                    conseils.append("Vitesse plus lente : pour garder la même intensité, appuyer PLUS (compenser le manque de vitesse).")
                elif n['duree_physique'] < prev['duree_physique']:
                    # Note plus courte (ex: Croche vs Noire)
                    conseils.append("Vitesse plus rapide : pour garder la même intensité, appuyer MOINS (la vitesse crée naturellement le son).")

        # 3. LOGIQUE DES LIAISONS
        if n.get('est_liaison'):
            conseils.append(f"Gérer la liaison de {n['nb_notes']} notes comme un seul geste fluide et continu.")

        # 4. POINT DE CONTACT ET POSITION
        depart = self._nommer_zone(n['start_force'] if n['start_force'] is not None else self.pos_actuelle)
        instructions_pos = f"Poser au {depart}."
        
        if n['nuance'] == 'f':
            instructions_pos += " Point de contact près du chevalet."
        else:
            instructions_pos += " Point de contact neutre."
        
        conseils.append(instructions_pos)

        # Mise à jour de la position
        deplacement = n['longueur_archet'] * n['direction']
        self.pos_actuelle = max(0, min(1, (n['start_force'] or self.pos_actuelle) + deplacement))
        self.derniere_note_physique = n
        
        return conseils

    def _extraire_parametres(self, unite):
        # Si c'est une liaison fusionnée, on récupère ses données, sinon on parse
        if isinstance(unite, dict):
            s = unite['brut']
            duree = unite['duree_physique']
            nb = unite['nb_notes']
            liaison = True
        else:
            s = unite
            duree = 1.0 / int(re.search(r'\d+', s).group()) if re.search(r'\d+', s) else 0.25
            nb = 1
            liaison = False

        return {
            'direction': -1 if "\\upbow" in s else 1,
            'longueur_archet': 1.0 if "WB" in s or "G.B." in s else 0.5 if "1/2" in s else 0.25,
            'longuer_nominale': "Tout" if ("WB" in s or "G.B." in s) else "Fraction",
            'start_force': 0.0 if '"Fr."' in s else 1.0 if '"Sp."' in s else None,
            'nuance': 'f' if '\\f' in s else 'p' if '\\p' in s else 'mf',
            'articulation': 'staccato' if '-.' in s else 'normale',
            'duree_physique': duree,
            'est_liaison': liaison,
            'nb_notes': nb
        }

    def _nommer_zone(self, val):
        if val <= 0.2: return "Talon"
        if val >= 0.8: return "Pointe"
        return "Milieu"

# --- EXEMPLE D'APPLICATION ---
moteur = SevcikLogicEngine()

# Scénario : Une noire tout l'archet, puis une croche tout l'archet
# Puis une liaison de 3 notes
partition = [
    'c4\\downbow^"Fr."^"WB"\\f',  # Noire, tout l'archet, forte
    'd8\\upbow^"Sp."^"WB"\\f',    # Croche, tout l'archet, forte
    moteur.traiter_liaison(['e8', 'f8', 'g4\\downbow']) # Liaison fusionnée
]

for item in partition:
    txt = item['brut'] if isinstance(item, dict) else item
    print(f"\nANALYSE DE : {txt}")
    for c in moteur.analyser_logique(item):
        print(f"  • {c}")
