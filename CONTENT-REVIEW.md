# Points à vérifier avant la mise en ligne

Les trois sites satellites contenaient des données contradictoires ou des restes de gabarit. Voici comment elles ont
été tranchées dans le site unifié, et ce qu'il faut confirmer avec le client ou les fiches constructeur.

## Données produits

| Produit | Conflit dans les sources | Retenu ici | À vérifier |
|---|---|---|---|
| Daiseikai 10 | Bandeau technique « SCOP max 4,6 » et « 7 kW / 15 kW » (copié de la fiche Yukai) contre la liste des caractéristiques « SCOP 5,3, SEER 10,7, 2,5–5 kW froid / 3,2–6 kW chaud » | La liste des caractéristiques | Confirmer le SCOP |
| Naka | Pictogrammes « A++ chaud / A++ froid » contre la caractéristique « A++ en refroidissement et A+ en chauffage » | A++ froid, A+ chaud | Confirmer les classes |
| Naka | L'introduction parlait du Yukai (copier-coller) | Réécrite pour le Naka | — |
| Yukai | Bandeau « 7 kW / 15 kW » (coquille pour 1,5 kW) | 1,5 à 6,5 kW froid, 2 à 7 kW chaud | — |
| Super Heating | Pictogrammes « A++ chaud / A++ froid » contre le texte « A+++ en chauffage » ; introduction copiée de la console double-flux ; « 3 tailles : 2,5 / 3,5 kW » (deux valeurs) | A+++ chaud, A++ froid ; introduction réécrite ; « puissances de 2,5 à 3,5 kW » | Confirmer les classes et le nombre de tailles |
| Shorai Curve | Introduction et encart parlaient du Shorai Edge | Réécrits pour le Curve | — |
| Console double-flux | Bandeau « 8 kW / 2,5 kW » et encart copié du Shorai Edge ; schémas d'installation empruntés au Naka | 2,5–5 kW froid, 3,2–6 kW chaud ; encart réécrit ; schémas Naka conservés faute d'autres visuels | Fournir des schémas propres à la console si disponibles |
| Gainable compact | « 2,0–7,0 kW froid » dans les caractéristiques, « 7,1 kW » dans le bandeau | 2 à 7 kW | — |
| Gainable standard | Fluide « R32 » et « R410A » tous deux affichés | « R32 ou R410A selon modèle » | Confirmer par référence |
| Yukai, Naka | Visuels de carte : le site satellite utilisait pour le Yukai une photo d'ambiance (`yukai-scaled.jpg`) | Même visuel conservé | Une photo produit sur fond neutre serait plus lisible en carte |
| Purevent, Wally | Aucune valeur chiffrée (débit, niveau sonore, dimensions) sur le site satellite | Fiches sans ces chiffres | Les ajouter depuis les brochures VMI si souhaité |
| Toutes les fiches VMI | Formule « conçu, assemblé et certifié en France par Pilotech-VMI » | Remplacée par « fabriqué en France par VMI » (Pilotech est l'installateur, VMI le fabricant) | — |
| Piccolo (Teknopoint) | La page pilotech.eu parle de « climatisation et chauffage » ; la fiche du fabricant indique « froid seulement » (3,6 et 5,3 kW) | Froid seul, comme le fabricant | Confirmer |
| Moka | Le bloc « compresseur twin-rotary 8–26 kW / scroll 28–33,5 kW » de la page est un texte générique VRF sans rapport avec un monobloc de 2,3 à 3,5 kW | Non repris | — |
| IDRA Next multisplit | « 5,2 / 7 / 8,2 kW » dans le texte, « 12 000 / 18 000 / 28 000 BTU/h » dans le bandeau | Les kW du texte | Confirmer |
| IDRA Eco multisplit | « trois puissances » sans valeurs sur la page | Aucune valeur affichée | Compléter |
| Cave à vin | La page pilotech.eu n'a pas pu être lue (limite de requêtes Squarespace) ; fiche rédigée d'après la documentation Teknopoint du Wine ELFO | À relire | Confirmer le modèle réellement proposé (Wine ELFO, Wine Split, Wine M03/M05) |
| Unités intérieures | Cinq noms (Duct Plus, gainable, SKIV, CASK, Console Int) sans description sur les pages lues | Présentées par type générique (murale, console, cassette, gainable) sans attribuer un type précis à chaque nom | Compléter les caractéristiques |

## Visuels

- **Teknopoint** : les visuels des 12 fiches pointent vers le CDN Squarespace du site pilotech.eu (`images.squarespace-cdn.com`)
  et les deux brochures vers `pilotech.eu/s/…`. Cela fonctionne tant que le site Squarespace existe. Lancer
  `sh scripts/localize-external-images.sh` pour tout rapatrier dans `assets/` avant de fermer Squarespace.
  Deux visuels n'ont pas pu être identifiés et sont des placeholders à remplacer : `assets/img/invisible/piccolo.png`
  et `assets/img/invisible/cave-a-vin.png`.
- Le site pilotech.eu contient une vingtaine de **photos de chantiers réels** (section « Nos travaux » et galerie de
  l'accueil). Elles ne sont pas reprises ici faute de pouvoir les télécharger ; elles feraient une bonne page
  « Réalisations ».

- **Six visuels Toshiba** (Haori, Daiseikai 10, Super Heating, Gainable standard, et une vue du Yukai et du Naka) sont
  encore hébergés sur un bucket externe (`storage.googleapis.com/uxpilot-auth…`) hérité de l'outil de maquettage.
  Ils fonctionnent aujourd'hui mais peuvent disparaître à tout moment. Lancer `sh scripts/localize-external-images.sh`
  pour les rapatrier (les URL sont remplacées automatiquement dans `_products/`).
- Les photos « à propos », « réalisations » et illustrations génériques du site VMI provenaient d'Unsplash
  (photos de banque, pas des chantiers Pilotech) : elles n'ont pas été reprises. Des photos de chantiers réels
  seraient un vrai plus pour une section « Réalisations ».
- Le logo utilisé est celui du site Toshiba (« Pilotech Climatisation — Installateur agréé Toshiba »). Sur les pages
  ventilation, la mention Toshiba est un peu incongrue : une variante « Pilotech » seule, sans sous-titre, serait
  préférable. Le fichier source du logo (vectoriel) n'était pas dans les dépôts.

## Coordonnées

- **Adresse** : le site VMI affichait « 123 Avenue de la République, 75011 Paris » — un texte de gabarit, pas une
  adresse réelle. Non reprise. Le schema.org indique seulement « Paris, Île-de-France » ; ajouter l'adresse du siège
  dans `_includes/seo.html` (bloc `address`) et sur `/mentions-legales/` si le client le souhaite.
- **Horaires** : le site Toshiba (données structurées) indiquait lundi–vendredi 9 h–18 h ; le site VMI
  lundi–vendredi 8 h–18 h et samedi 9 h–13 h. Retenu : 9 h–18 h en semaine (`_config.yml`, `hours_label`, et
  `openingHoursSpecification` dans `seo.html`). À confirmer.
- **E-mail** : `info.pilotech@gmail.com` partout ; le site VMI mentionnait aussi `info@pilotech.eu` dans un en-tête.
  À confirmer, et à mettre à jour dans `_config.yml` (`company.email` et `forms.destinataire`).
- **Domaine** : `url: https://pilotech.eu` dans `_config.yml`. C'est aujourd'hui l'adresse du site Squarespace
  (Teknopoint). Si le site unifié doit le remplacer, c'est correct : basculer le DNS vers GitHub Pages et créer le
  fichier `CNAME`. Sinon, choisir un autre domaine et le renseigner dans `url:`. Le site Squarespace a de toute façon
  vocation à disparaître ou à rester en satellite : dans le premier cas, prévoir les redirections 301 de ses URL
  (`/moka` → `/climatisation-invisible/moka/`, `/idra-next-monosplit-…` → `/climatisation-invisible/idra-next-monosplit/`, etc.).
- **Localité** : le site pilotech.eu et la fiche Google Business situent l'entreprise à **Sucy-en-Brie (94)**.
  Les données structurées utilisent désormais Sucy-en-Brie / 94370 (`_config.yml`, `company.city`). Ajouter l'adresse
  complète si le client le souhaite (cohérence avec la fiche Google Business, utile en référencement local).
- **Mentions légales** : forme juridique, SIREN, TVA, adresse du siège et directeur de publication sont à compléter
  dans `mentions-legales.html`.

## Contenu repris tel quel

- Les **avis Google** (19, dont quatre issus du site pilotech.eu) sont des citations de clients : conservés à l'identique.
- Le **blog** n'est pas repris. Les articles des satellites (21 sur pilotech-vmi.fr, 7 sur pilotech.eu, 1 gabarit
  générique sur pilotech-toshiba.com) devront être réécrits avec des mots différents avant d'être publiés ici,
  pour ne pas cannibaliser le référencement des sites d'origine.

## Sites satellites

Les sites existants restent en ligne et sont référencés dans le footer et dans `sameAs` des données structurées.
Pour éviter toute cannibalisation, garder le site unifié comme référence de marque (nom, adresse, avis) et laisser
les satellites sur leurs mots-clés respectifs ; si un jour ils sont fermés, prévoir des redirections 301 vers les
fiches correspondantes du site unifié (`/gammes/shorai-edge/` → `/climatisation/shorai-edge/`, `/wally.html` →
`/ventilation/wally/`, etc.).
