faire un programme note par note avec un formulaire qui demande comme pour remplir oqui montre note par note les liaison / avec un html form 
\header { title = \markup "Header" }

dyn =
#(make-dynamic-script #{ \markup \text "DynamicText" #})

\markup \box "Top-level markup"

\score {
  <<
    \new ChordNames
    \with {
      majorSevenSymbol = \markup "majorSevenSymbol"
    }
    \chordmode { c1:maj7 }
    \new Staff {
      \tempo \markup "MetronomeMark"
      \textMark "textMark"
      \once \override TupletNumber.text =
        \markup "TupletNumber"
      \tuplet 3/2 {
        \once \override NoteHead.stencil =
          #ly:text-interface::print
        \once \override NoteHead.text =
          \markup \lower #0.5 "NoteHead"
        c''8^\markup \italic "TextScript"
        a'\finger \markup \text "Fingering"
        \once \override Rest.stencil =
          #(lambda (grob)
             (grob-interpret-markup grob #{
               \markup  "Rest"
               #}))
        r
      }
    }
    \new Lyrics \lyricmode {
      \markup \smallCaps "LyricText" 1
    }
    \new Dynamics { s1\dyn }
  >>
}

au dessus /dessous de la portée début liaison note précédente ou fin liaison, tout archet (G) 1/3 B(un tiers d'archet), 1/4 B, 1/2B, ["fr","M","M*","Sp"] avec python transformer spicatto en moitié de la valeur de la note+moitié valeur silence, et transfromer staccto en 3/4 valeur de la note et 1/4 valeur du silence, pouvoir comparer 2 notes ou liaison(1 note et une liaison) par rapport à la longueur/vitesse/pression et avoir la logique deux l'archet entre deux notes/groupes notes


 1/2 1/4 pression longueur logique , appuyer plus, appuyer moins , 
longueur notes, valeur des notes , son plus plus fort, appuyer moins le 
son est moins fort, archet vite mais appui pas beaucoup , son est pas 
fort , on réussit à faire la durée , la durée,
durée est courte, 
La longueur de talon ou pointe ou milieu est 1/4 ou un tiers,
Pour garder même intensité son, 
Il
 y a l'intensité de son que tu imagine pour piano , forte ou nuance de 
départ et nuance d'arrivée même si c'est la même, comme l'accent 
l'intensité est courte mais d'un seul coup pour une courte durée 
Spiccato valeur moitié de la durée entière de la note
Staccato valeur des 3/4
Logique de l'archet après /avant/pendant une longue liaison
Passer de talon à pointe en decollant larchet,
 pas qui imprime des pourcents mais des indications de logique archet, 
"1ère note longue /courte, 2ème plus/moins 
longue/courte/appuyée/allongée/rapide/lente etc" , en tuilisant point de contact corde sol plus loin du chevalet, corde de mi plus près, a quel endroit précis de l'archet commence et se termine le coup d'archet, a quelle distance se trouve d'arechet du chevalet, tous les coups d'archet sont il meme ou certain devraient il etre plus proche du chevalet ? a quell vitesse coup d'archet, vitesse égale?varie t elle selon sché rapide lent, lent rapide, lent rapide lent etc. quelle est la pression de l'archet sur la corde, est elle égale, ou variable quelle tension du crin, donne la meilleure sonorité? et procure le coup d'archet plus aisé? restelle égale ou doit elle varier de plus à moins relachée? etc

programme prendre un texte musical en entrée, diviser le texte par notes /on entre une à une les notes du texte dans le formulaire avec les champs header top level markup metronome mark text mark cmajorsevensymbol textscrpt fingering notehead rest tuplet number lyric text dynamic text qui les affiche optionnellement chacun des champs (tous les champs), autre champs: début de liaison (note precedent), fin de liaison, Ensuite on propre une liste à l'user de toutes les note ou note regroupée par liaison et note seule. et de choisir 2 qui se suivent ou pas pour comparer la logique de l'archet
le programme connait les notations sevcik/lilypond:
tu peux écrire pour une note  dessous: G(tout l'archet), ou H (moitié de l'archet), uH (partie inferieure archet), oH 'moitie superieure de l'archet) 1/3B(un tiers archet) M (Milieu) Sp (pointe) M* (milieu, puis pointe puis talon)
tu peux écrire \stacatissimo ou \staccato, ou \tenuto et/ou \downbow \upbow \caesura (pour lever l'archet)
 le programme donne une liste des des notes ou groupes de notes liées ou bien de toutes les notes seule et il faut choisir 2 notes ou groupes de notes à comparer(pour comparer la logique de l'archet
en entrée l'user donne un texte simple 1 ou plusieurs mesure en lilypond
