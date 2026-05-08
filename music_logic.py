class MusicLogic:
    def __init__(self, note_data):
        self.notes = note_data # Liste de dictionnaires venant du formulaire

    def transformer_articulation(self, note):
        """ Transforme les durées selon les règles demandées """
        duree_totale = float(note['valeur_temporelle'])
        
        if note['articulation'] == 'spiccato':
            # 1/2 note + 1/2 silence
            return {"son": duree_totale * 0.5, "silence": duree_totale * 0.5}
        
        elif note['articulation'] == 'staccato':
            # 3/4 note + 1/4 silence
            return {"son": duree_totale * 0.75, "silence": duree_totale * 0.25}
        
        return {"son": duree_totale, "silence": 0}

    def comparer_notes(self, index1, index2):
        """ Logique comparative entre deux moments choisis par l'utilisateur """
        n1 = self.notes[index1]
        n2 = self.notes[index2]
        conseils = []

        # 1. Analyse de la Vitesse d'Archet (V = L / T)
        # On compare la longueur d'archet utilisée sur la durée réelle du son
        v1 = n1['longueur_archet'] / n1['duree_son']
        v2 = n2['longueur_archet'] / n2['duree_son']

        if v2 > v1:
            conseils.append(f"Accélérez l'archet de {round((v2/v1-1)*100)}% pour la deuxième note.")
        elif v2 < v1:
            conseils.append("Ralentissez l'archet : économisez la longueur pour garder l'intensité.")

        # 2. Point de contact et Cordes
        if n2['corde'] == 'Sol' and n1['corde'] != 'Sol':
            conseils.append("Corde de Sol : Rapprochez l'archet du chevalet et augmentez le poids naturel.")
        elif n2['corde'] == 'Mi':
            conseils.append("Corde de Mi : Éloignez-vous légèrement du chevalet pour éviter le sifflement.")

        # 3. Pression et Intensité
        if n2['pression'] > n1['pression']:
            conseils.append("Augmentez l'index (pression) tout en gardant le crin bien à plat.")

        return conseils
mydata=[
  {
    "id": 1,
    "pitch": "c''",
    "duration_val": 1.0,
    "articulation": "normal",
    "slur": "start",
    "bow_division": "1/2B",
    "bow_position": "fr",
    "pressure": 7,
    "string": "Sol",
    "contact_point": "proche chevalet",
    "markup": {
      "header": "Exercice 1",
      "dynamic": "f",
      "fingering": "1"
    }
  },
  {
    "id": 2,
    "pitch": "e''",
    "duration_val": 1.0,
    "articulation": "normal",
    "slur": "end",
    "bow_division": "1/2B",
    "bow_position": "M",
    "pressure": 5,
    "string": "Sol",
    "contact_point": "milieu",
    "markup": {
      "dynamic": "mf"
    }
  },
  {
    "id": 3,
    "pitch": "g''",
    "duration_val": 0.5,
    "articulation": "spiccato",
    "slur": "none",
    "bow_division": "1/4B",
    "bow_position": "M*",
    "pressure": 3,
    "string": "Mi",
    "contact_point": "loin chevalet",
    "markup": {
      "text_mark": "leggiero",
      "fingering": "3"
    }
  }
]
