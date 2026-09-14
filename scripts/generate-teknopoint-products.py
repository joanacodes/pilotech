#!/usr/bin/env python3
"""Génère les 12 fiches produits Teknopoint (univers « climatisation invisible ») dans _products/.
Les visuels pointent pour l'instant vers le CDN du site Squarespace pilotech.eu ;
`scripts/localize-external-images.sh` les rapatrie ensuite dans assets/img/invisible/.
"""
from pathlib import Path
import textwrap

CDN = "https://images.squarespace-cdn.com/content/v1/6795159239530112bc66aee2/"
BROCHURE_GEN = "https://www.pilotech.eu/s/CLIMATISATIONS-INVISIBLES-PILOTECH-CLIM-3.pdf"
BROCHURE_CAT = "https://www.pilotech.eu/s/1779873737-productsCAT_Les_Invisibles_Die_Unsichtbaren_FRA_DE-rllw.pdf"
IMG = {
    "elfo": CDN + "6d24c9c3-2482-4b18-8205-f5f360a9fff9/elfo+vfr+teknopont+6+pilotech.png",
    "elfo-hero": CDN + "9537c0d6-fd87-40e5-8b54-e484b42519ae/ELFO+CLIM+BGD+TRSPRT.png",
    "elfo-vrf": CDN + "45c64e8a-4600-436d-a0db-6bf34b11be3f/elfo+vfr+teknopont+6+pilotech+%281%29.png",
    "elfo-vrf-2": CDN + "251dce26-b999-48d2-bcce-a582e40ce630/elfo+vfr+teknopont+6+pilotech.png",
    "idra-next": CDN + "7721bf2c-e508-4407-b803-b03747809329/IDRA+teknopont+6+pilotech.png",
    "idra-eco": CDN + "f31bd7ab-39f6-434b-87f2-5afdb2dce904/IDRA+teknopont+6+pilotech+%281%29.png",
    "idra-ring": CDN + "446c0d17-1949-4594-b207-e0d2a4750941/IDRA+teknopont+6+pilotech+%282%29.png",
    "moka": CDN + "c8f70c48-7ada-46a8-969f-c6dc6239b267/MOKA+PILOTECH.png",
    "moka-2": CDN + "978e90bd-51e9-4b04-a7f6-041e81bb1dca/MOKA+PILOTECH+2.png",
    "moka-salon": CDN + "eb202a90-610b-4758-819e-ec46f3cddb71/MOKA+LIVING+ROOM.png",
    "unites": CDN + "57f61d93-11e0-4c99-b5aa-382cacd21c59/elfo+vfr+teknopont+6+pilotech+%282%29.png",
    "duct-plus": CDN + "cc97fe4c-7a8b-437c-9075-69b9242ee032/DUCT+PLUS+TEKNOPOINT+PILOTECH.jpg",
    "gainable": CDN + "57fb2cee-7ef4-430a-b87b-e7776dcd5181/UNITE+GENERALE+TEKNOPOINT+PILOTECH.jpg",
    "skiv": CDN + "39222ca9-df84-4ad1-9533-bcc9d2b2704b/SKIV+TEKNOPOINT+PILOTECH.jpg",
    "cask": CDN + "55f2fa34-51e7-4222-b125-a0ea7bc6a0d9/CASK+TEKNOPOINT+PILOTECH.jpg",
    "console": CDN + "52e41d6a-34ca-49e4-947f-5638bcf7427f/CONSOLE+INT.jpg",
    "schema": CDN + "b69aed57-d5b2-40c5-a0d7-c57e269e3b97/Schema+Teknopoint+Pillotehc.png",
    "dc-inverter": CDN + "26894eea-bf18-42b7-8b55-35529c810cfd/DC+INVERTER+EFLO+MULTISPLIT+PILOTECH.jpg",
    "eau": CDN + "0fc23afe-3e20-4b3b-9f08-d7b033e2dd0d/1568022342-accessoriesRisparmio-Idrico.jpg",
    "silence": CDN + "f63c5cc1-a7ae-44a4-beb1-15608d60423b/1568023602-accessoriesUltra+silenzioso.jpg",
    "a3": CDN + "1fbb314d-8614-48b6-a116-be0c08c487ea/1584543418-accessoriesthinkstockphotos-578584200.jpg",
    "app": CDN + "d9b81eba-e41c-488e-9ce5-0e540cc9bcab/pilotech+moka+app.jpg",
    "piccolo": "/assets/img/invisible/piccolo.png",      # visuel à fournir (placeholder généré)
    "cave": "/assets/img/invisible/cave-a-vin.png",      # visuel à fournir (placeholder généré)
}

IDRA_FEATURES_COMMON = [
    "Aucune unité extérieure ni grille visible depuis la rue : l'appareil est refroidi à l'eau.",
    "Se loge dans un placard, sous un évier, dans une salle de bains ou un petit local technique.",
    "Technologie Full DC Inverter : puissance modulée selon le besoin réel, consommation et bruit réduits.",
    "Compresseurs Panasonic et Mitsubishi DC Inverter, électronique dédiée.",
    "Consommation d'eau la plus basse de sa catégorie grâce à la gestion électronique DC Inverter.",
    "Caisson insonorisé : 41 dB(A), le niveau d'un réfrigérateur domestique.",
    "Jusqu'à 70 m entre la centrale et les unités intérieures : installation discrète même en centre historique.",
    "Compatible avec les unités intérieures Duct Plus, gainable, SKIV, CASK et Console Int.",
    "Fluide R32, pilotage Wi-Fi.",
]
IDRA_SPECS_BASE = [
    ("Type", "Climatiseur à eau, sans unité extérieure"),
    ("Technologie", "Full DC Inverter"),
    ("Compresseurs", "Panasonic / Mitsubishi DC Inverter"),
    ("Niveau sonore", "41 dB(A)"),
    ("Distance centrale / unités", "Jusqu'à 70 m"),
    ("Fluide", "R32"),
]
IDRA_CONTROLS = [
    ("Économie d'eau grâce au DC Inverter", IMG["eau"]),
    ("Caisson insonorisé, 41 dB(A)", IMG["silence"]),
    ("Compresseur DC Inverter", IMG["dc-inverter"]),
]
ELFO_FEATURES_COMMON = [
    "Groupe de condensation Full DC Inverter intégré à l'intérieur du bâtiment.",
    "À l'extérieur, seules deux grilles de 20 cm de diamètre restent visibles.",
    "Ventilateurs centrifuges qui aspirent l'air extérieur nécessaire au fonctionnement.",
    "Rafraîchit, chauffe et déshumidifie : c'est une pompe à chaleur.",
    "Se raccorde à des unités intérieures murales, consoles, cassettes ou gainables.",
    "Moteurs de ventilation BLDC à haut rendement et faible niveau sonore.",
    "Conçu pour les bâtiments classés, les centres historiques et les copropriétés qui interdisent tout groupe en façade.",
]

P = []

P.append(dict(slug="elfo-monosplit", order=18, name="ELFO Monosplit",
    title="ELFO Monosplit : climatisation sans unité extérieure | Pilotech",
    description="Le climatiseur ELFO chauffe, rafraîchit et déshumidifie une pièce sans groupe en façade : seules deux grilles de 20 cm sont visibles. 3,5 ou 5,2 kW. Posé par Pilotech à Paris.",
    category="Climatisation sans unité extérieure", type_label="Sans unité extérieure, une pièce",
    tagline="Une pièce, deux grilles de 20 cm en façade", image=IMG["elfo"], image_alt="Climatiseur Teknopoint ELFO sans unité extérieure",
    lead="L'ELFO regroupe à l'intérieur du bâtiment ce qu'une climatisation classique met en façade : son groupe de condensation Full DC Inverter est intégré, et l'air extérieur dont il a besoin passe par deux grilles de 20 cm de diamètre. La pièce est chauffée, rafraîchie et déshumidifiée sans rien poser dehors.",
    facts=[("2 grilles", "De 20 cm en façade"), ("3,5 ou 5,2 kW", "Deux puissances (ELFO-12, ELFO-18)"), ("Réversible", "Chauffage, froid, déshumidification", "warm"), ("DC Inverter", "Groupe de condensation intégré"), ("4 types", "D'unités intérieures compatibles"), ("Teknopoint", "Fabricant italien, 30 ans d'expérience")],
    highlight=("Pensé pour les façades que l'on n'a pas le droit de toucher", "Immeuble classé, secteur sauvegardé, règlement de copropriété strict : l'ELFO répond à ces situations avec une installation entièrement intérieure. Il se combine avec une unité murale, une console, une cassette ou un gainable selon la pièce."),
    features=ELFO_FEATURES_COMMON + ["Deux puissances en monosplit : ELFO-12 (3,5 kW) et ELFO-18 (5,2 kW)."],
    specs=[("Type", "Climatiseur sans unité extérieure, air-air"), ("Puissances", "ELFO-12 : 3,5 kW ; ELFO-18 : 5,2 kW"), ("Grilles extérieures", "2 × 20 cm de diamètre"), ("Technologie", "Full DC Inverter, ventilateurs BLDC"), ("Fonctions", "Rafraîchissement, chauffage, déshumidification"), ("Unités intérieures", "Murale, console, cassette, gainable")],
    controls=[("Compresseur DC Inverter", IMG["dc-inverter"]), ("Principe d'installation Teknopoint", IMG["schema"])],
    gallery=[(IMG["elfo"], "Climatiseur ELFO"), (IMG["elfo-hero"], "Unité ELFO, vue de face"), (IMG["schema"], "Principe d'installation sans unité extérieure")],
    body="""## Quand le mur est la seule issue

Le cas typique est l'appartement parisien dont la copropriété refuse toute machine en façade, ou l'immeuble en secteur protégé où l'architecte des Bâtiments de France a son mot à dire. L'ELFO ne demande que deux percements de 20 cm et une place à l'intérieur pour la centrale, souvent un placard ou un faux plafond. La visite technique sert à repérer le mur extérieur le plus discret et à mesurer la place disponible.

## Comment nous l'installons

Pilotech est partenaire Teknopoint pour l'Île-de-France : nous dimensionnons l'appareil, réalisons les carottages avec finition des grilles côté rue, posons l'unité intérieure choisie et mettons en service. Comptez une journée pour un monosplit, davantage si un gainable est retenu."""))

P.append(dict(slug="elfo-multisplit", order=19, name="ELFO Multisplit",
    title="ELFO Multisplit : jusqu'à trois pièces sans unité extérieure | Pilotech",
    description="Bi-split 4,1 ou 5,2 kW, tri-split 7 kW : ELFO Multisplit climatise, chauffe et déshumidifie jusqu'à trois pièces depuis une seule centrale intérieure, avec deux grilles en façade. Pose Pilotech IDF.",
    category="Climatisation sans unité extérieure", type_label="Sans unité extérieure, deux ou trois pièces",
    tagline="Deux ou trois pièces, une seule centrale intérieure", image=IMG["elfo-hero"], image_alt="Climatiseur Teknopoint ELFO Multisplit",
    lead="Même principe que l'ELFO Monosplit, avec une centrale capable d'alimenter deux ou trois unités intérieures. Une seule installation, deux grilles de 20 cm dehors, et des pièces réglées séparément : c'est la configuration des appartements de plusieurs chambres et des petits bureaux.",
    facts=[("3 pièces", "Au maximum, en tri-split"), ("4,1 à 7 kW", "Trois modèles"), ("2 grilles", "De 20 cm en façade"), ("Réversible", "Chauffage, froid, déshumidification", "warm"), ("DC Inverter", "Groupe de condensation intégré"), ("Teknopoint", "Fabricant italien")],
    highlight=("Plusieurs pièces, un seul point de passage", "Un bi-split ou un tri-split évite de multiplier les percements : la centrale intérieure dessert chaque unité, et chaque pièce garde sa propre consigne. Unités murales, consoles, cassettes ou gainables se combinent librement."),
    features=ELFO_FEATURES_COMMON + ["Trois modèles : ELFO2-12 (4,1 kW, bi-split), ELFO2-18 (5,2 kW, bi-split), ELFO3-24 (7 kW, tri-split).", "Chaque pièce dispose de son propre réglage."],
    specs=[("Type", "Climatiseur sans unité extérieure, air-air, multisplit"), ("Bi-split", "ELFO2-12 : 4,1 kW ; ELFO2-18 : 5,2 kW"), ("Tri-split", "ELFO3-24 : 7 kW"), ("Grilles extérieures", "2 × 20 cm de diamètre"), ("Technologie", "Full DC Inverter, ventilateurs BLDC"), ("Unités intérieures", "Murale, console, cassette, gainable")],
    controls=[("Compresseur DC Inverter", IMG["dc-inverter"]), ("Principe d'installation Teknopoint", IMG["schema"])],
    gallery=[(IMG["elfo-hero"], "Climatiseur ELFO Multisplit"), (IMG["elfo"], "Gamme ELFO"), (IMG["schema"], "Principe d'installation sans unité extérieure")],
    body="""## Pour quels lieux

Un appartement de deux ou trois chambres, un cabinet avec salle d'attente et bureau, une boutique avec réserve : dès qu'il faut traiter plusieurs volumes sans droit de façade, le multisplit s'impose. Le tri-split ELFO3-24 couvre 7 kW, ce qui correspond à un logement d'une centaine de mètres carrés bien isolé.

## Ce que nous vérifions avant de chiffrer

L'emplacement de la centrale, le mur extérieur qui recevra les deux grilles, le cheminement des liaisons vers chaque pièce et le type d'unité intérieure adapté à chacune. Ces choix conditionnent la discrétion du résultat, c'est pourquoi le devis n'est établi qu'après la visite."""))

P.append(dict(slug="elfo-vrf", order=20, name="ELFO VRF",
    title="ELFO VRF : jusqu'à 9 unités intérieures sans unité extérieure | Pilotech",
    description="ELFO VRF climatise les commerces et bureaux où aucun condenseur extérieur n'est autorisé : centrale centrifuge dissimulée, jusqu'à neuf unités intérieures, compresseur Toshiba GMCC. Pose Pilotech en IDF.",
    category="Climatisation sans unité extérieure haute puissance", type_label="VRF sans unité extérieure",
    tagline="Jusqu'à neuf unités intérieures, rien dehors", image=IMG["elfo-vrf"], image_alt="Centrale Teknopoint ELFO VRF sans unité extérieure",
    lead="L'ELFO VRF transpose le principe des Invisibles aux surfaces professionnelles : une unité de condensation centrifuge dissimulée à l'intérieur alimente jusqu'à neuf unités intérieures, en cassette, gainable, murale ou plafond-plancher. La puissance d'un VRF, sans le moindre condenseur en toiture ou en façade.",
    facts=[("9 unités", "Intérieures au maximum"), ("4 types", "Cassette, gainable, murale, plafond-plancher"), ("Toshiba GMCC", "Compresseur"), ("Centrifuge", "Condensation dissimulée"), ("Réversible", "Chauffage et rafraîchissement", "warm"), ("Teknopoint", "Fabricant italien")],
    highlight=("Puissance maximale, impact visuel nul", "Les panneaux de la centrale sont interchangeables : la direction de l'air entrant et sortant se modifie à la pose, et le moteur se règle pour garder le rendement dans n'importe quelle configuration. De quoi loger la machine dans un local technique aux contraintes réelles."),
    features=["Unité de condensation centrifuge entièrement dissimulée à l'intérieur du bâtiment.", "Jusqu'à neuf unités intérieures gérées par une même centrale.", "Unités intérieures au choix : cassette, gainable, murale ou plafond-plancher.", "Compresseur Toshiba GMCC : fiabilité, rendement et niveau sonore contenu.", "Panneaux interchangeables pour orienter l'air entrant et sortant selon le local.", "Moteur ajustable pour conserver les performances quelle que soit la configuration.", "Destiné aux environnements commerciaux où les condenseurs extérieurs sont interdits."],
    specs=[("Type", "VRF sans unité extérieure"), ("Unités intérieures", "Jusqu'à 9"), ("Types d'unités", "Cassette, gainable, murale, plafond-plancher"), ("Compresseur", "Toshiba GMCC"), ("Condensation", "Centrifuge, dissimulée"), ("Panneaux", "Interchangeables (direction de l'air)")],
    controls=[("Centrale ELFO VRF", IMG["elfo-vrf-2"]), ("Principe d'installation Teknopoint", IMG["schema"])],
    gallery=[(IMG["elfo-vrf"], "Centrale ELFO VRF"), (IMG["elfo-vrf-2"], "ELFO VRF, autre vue"), (IMG["schema"], "Principe d'installation sans unité extérieure")],
    body="""## Le tertiaire sans droit de façade

Restaurant en rez-de-chaussée d'un immeuble haussmannien, boutique sous arcades, plateau de bureaux dans un bâtiment protégé : ces lieux ont des charges thermiques importantes et aucune possibilité de poser un condenseur dehors. L'ELFO VRF y répond avec une centrale unique, dissimulée, et une unité intérieure par zone.

## Une étude de charge avant tout

Surface, occupation, vitrages, équipements, horaires : le dimensionnement d'un VRF se calcule. Nous réalisons l'étude, proposons l'emplacement de la centrale et le type d'unité par zone, puis planifions le chantier autour de votre activité, y compris en dehors des heures d'ouverture."""))

for slug, order, name, powers_txt, powers_spec, kind, extra in [
    ("idra-next-monosplit", 21, "IDRA Next Monosplit", "quatre puissances, de 3,5 à 10 kW", "3,5 / 5,2 / 7 / 10 kW", "mono",
     "Conçu pour chauffer et rafraîchir une seule pièce, il convient aux commerces et bureaux de taille réduite comme aux appartements."),
    ("idra-next-multisplit", 22, "IDRA Next Multisplit", "trois puissances, de 5,2 à 8,2 kW", "5,2 / 7 / 8,2 kW", "multi",
     "Une centrale pour plusieurs pièces, en bi-split, tri-split ou quadri-split : la configuration des bureaux et commerces de plusieurs zones."),
]:
    P.append(dict(slug=slug, order=order, name=name,
        title=f"{name} : climatiseur à eau sans unité extérieure | Pilotech",
        description=f"{name} : refroidi à l'eau, aucune grille ni groupe visible, Full DC Inverter, 41 dB(A), {powers_txt}. Se loge dans un placard ou un local technique. Pose Pilotech à Paris et en IDF."[:155],
        category="Climatisation à eau sans unité extérieure", type_label="Climatiseur à eau, " + ("une pièce" if kind == "mono" else "plusieurs pièces"),
        tagline=("Rien en façade, pas même une grille" if kind == "mono" else "Bi, tri ou quadri-split à eau, rien en façade"),
        image=IMG["idra-next"], image_alt=f"Climatiseur à eau Teknopoint {name}",
        lead=f"L'IDRA Next est un climatiseur refroidi à l'eau : ni groupe extérieur, ni grille en façade, la totalité de l'appareil tient dans un placard, sous un évier ou dans un petit local technique. {extra} Full DC Inverter, compresseurs Panasonic et Mitsubishi, et un caisson insonorisé à 41 dB(A).",
        facts=[("0 grille", "Rien de visible à l'extérieur"), (powers_spec.split(" / ")[0] + " à " + powers_spec.split(" / ")[-1], "Puissances disponibles"), ("41 dB(A)", "Caisson insonorisé"), ("70 m", "Entre centrale et unités"), ("Réversible", "Chauffage et rafraîchissement", "warm"), ("R32", "Fluide, Wi-Fi")],
        highlight=("Le plus discret de tous : refroidi à l'eau", "Là où les gammes à air ont besoin de deux grilles, l'IDRA Next se contente d'un raccordement hydraulique. C'est la solution des bâtiments où même une grille est refusée, et des locaux sans mur extérieur accessible."),
        features=IDRA_FEATURES_COMMON + ([f"Quatre puissances : 3,5, 5,2, 7 et 10 kW (12 000 à 36 000 BTU/h)."] if kind == "mono" else ["Trois puissances : 5,2, 7 et 8,2 kW.", "Versions bi-split, tri-split et quadri-split."]) + ["Déclinaisons de la gamme : CED pour les salles informatiques, RING pour les boucles d'eau, ECO pour une consommation encore réduite."],
        specs=[("Puissances", powers_spec)] + IDRA_SPECS_BASE + ([("Configuration", "Monosplit")] if kind == "mono" else [("Configurations", "Bi-split, tri-split, quadri-split")]),
        controls=IDRA_CONTROLS,
        gallery=[(IMG["idra-next"], f"{name}"), (IMG["schema"], "Principe d'installation sans unité extérieure")],
        body="""## Un climatiseur raccordé à l'eau

Le principe : la chaleur extraite de la pièce est évacuée par un circuit d'eau plutôt que par un échangeur en façade. L'appareil se raccorde au réseau, et sa gestion électronique DC Inverter limite la consommation d'eau au minimum de sa catégorie. Pour les immeubles équipés d'une boucle d'eau, la version RING est prévue ; pour les salles serveurs, la version CED.

## Où le placer

Le silence du caisson (41 dB(A)) autorise une pose dans un placard de couloir, sous un plan de travail ou dans une salle de bains. La visite technique vérifie l'arrivée et l'évacuation d'eau, l'alimentation électrique et le cheminement vers les unités intérieures, jusqu'à 70 m."""))

P.append(dict(slug="idra-next-ring", order=23, name="IDRA Next Ring",
    title="IDRA Next Ring : climatiseur sur boucle d'eau, sans unité extérieure | Pilotech",
    description="IDRA Next Ring se raccorde à la boucle d'eau d'un immeuble : aucune unité extérieure ni grille, Full DC Inverter, 41 dB(A), chauffage et rafraîchissement. Installation Pilotech à Paris et en IDF.",
    category="Climatisation à eau sans unité extérieure", type_label="Climatiseur sur boucle d'eau",
    tagline="Pour les immeubles équipés d'une boucle d'eau", image=IMG["idra-ring"], image_alt="Climatiseur Teknopoint IDRA Next Ring",
    lead="Version de l'IDRA Next prévue pour les bâtiments qui disposent d'une boucle d'eau : l'appareil s'y raccorde et rejette la chaleur dans le circuit, sans grille ni groupe extérieur. Même plateforme Full DC Inverter, mêmes compresseurs Panasonic et Mitsubishi, même caisson insonorisé.",
    facts=[("Boucle d'eau", "Raccordement au circuit de l'immeuble"), ("0 grille", "Rien de visible à l'extérieur"), ("41 dB(A)", "Caisson insonorisé"), ("Réversible", "Chauffage et rafraîchissement", "warm"), ("Mono / multi", "Versions disponibles"), ("R32", "Fluide, Wi-Fi")],
    highlight=("La solution des immeubles tertiaires récents", "De nombreux immeubles de bureaux et résidences de standing disposent déjà d'une boucle d'eau. L'IDRA Next Ring l'utilise comme source d'échange : l'installation se réduit à un raccordement hydraulique et au placement de l'unité intérieure."),
    features=IDRA_FEATURES_COMMON + ["Prévu pour les systèmes raccordés à une boucle d'eau.", "Disponible en monosplit et en multisplit."],
    specs=[("Type", "Climatiseur sur boucle d'eau, sans unité extérieure"), ("Configurations", "Monosplit, multisplit")] + IDRA_SPECS_BASE,
    controls=IDRA_CONTROLS,
    gallery=[(IMG["idra-ring"], "IDRA Next Ring"), (IMG["schema"], "Principe d'installation sans unité extérieure")],
    body="""## Quand la boucle d'eau existe déjà

Dans un immeuble équipé d'une boucle d'eau, chaque occupant peut se raccorder pour son chauffage et son rafraîchissement. L'IDRA Next Ring est la déclinaison de la gamme prévue pour ce cas : elle s'y branche directement, sans percement ni équipement extérieur, et se place dans un local technique, un placard ou un faux plafond.

## Notre rôle

Vérification de la compatibilité avec la boucle (température, débit disponible, points de raccordement), dimensionnement, pose et mise en service, puis entretien annuel."""))

for slug, order, name, powers_spec, kind in [
    ("idra-eco-monosplit", 24, "IDRA Eco Monosplit", "3,5 / 5,2 / 7 / 10 kW", "mono"),
    ("idra-eco-multisplit", 25, "IDRA Eco Multisplit", "Trois puissances (bi, tri, quadri-split)", "multi"),
]:
    P.append(dict(slug=slug, order=order, name=name,
        title=f"{name} : classe A+++ sans unité extérieure | Pilotech",
        description=f"{name} : la version économe de l'IDRA Next, classée A+++, refroidie à l'eau, sans grille ni groupe extérieur, 41 dB(A). Pour bureaux, commerces et appartements. Pose Pilotech en IDF."[:155],
        category="Climatisation à eau sans unité extérieure", type_label="Climatiseur à eau, classe A+++",
        tagline=("A+++, une pièce, rien en façade" if kind == "mono" else "A+++, plusieurs pièces, rien en façade"),
        image=IMG["idra-eco"], image_alt=f"Climatiseur Teknopoint {name}",
        lead=f"L'IDRA Eco reprend la plateforme de l'IDRA Next, refroidie à l'eau et sans aucun élément en façade, avec une électronique orientée vers la consommation minimale : classe énergétique A+++, soit un rendement supérieur de 48 % à celui d'un appareil A++. {'Une pièce, quatre puissances.' if kind == 'mono' else 'Plusieurs pièces, en bi-split, tri-split ou quadri-split.'}",
        facts=[("A+++", "Classe énergétique", "cool"), ("+48 %", "De rendement par rapport à un A++"), ("0 grille", "Rien de visible à l'extérieur"), ("41 dB(A)", "Caisson insonorisé"), ("Réversible", "Chauffage et rafraîchissement", "warm"), ("R32", "Fluide, Wi-Fi")],
        highlight=("Le même invisible, avec la consommation en moins", "Un appareil A+++ consomme sensiblement moins qu'un A++ pour le même confort. Sur un commerce ouvert toute la journée ou un bureau occupé en continu, la différence se lit sur la facture dès la première saison."),
        features=IDRA_FEATURES_COMMON + ["Classe énergétique A+++ : 48 % d'efficacité en plus qu'un appareil A++."] + ([f"Quatre puissances : 3,5, 5,2, 7 et 10 kW."] if kind == "mono" else ["Trois puissances, en bi-split, tri-split ou quadri-split."]),
        specs=[("Classe énergétique", "A+++"), ("Puissances", powers_spec)] + IDRA_SPECS_BASE,
        controls=[("Classe énergétique A+++", IMG["a3"])] + IDRA_CONTROLS,
        gallery=[(IMG["idra-eco"], f"{name}"), (IMG["schema"], "Principe d'installation sans unité extérieure")],
        body="""## Pour qui

Les locaux qui tournent longtemps : commerces, cabinets, bureaux, mais aussi les appartements où la climatisation sert de chauffage d'appoint une bonne partie de l'année. Le surcoût par rapport à l'IDRA Next se compense par la consommation, et l'installation est identique : un raccordement d'eau, une place dans un placard ou un local technique, aucune trace dehors.

## L'installation

Comme pour toute la gamme IDRA, la visite technique porte sur l'arrivée et l'évacuation d'eau, l'alimentation électrique, l'emplacement de la centrale et le cheminement vers les unités intérieures. Nous assurons ensuite la mise en service et l'entretien."""))

P.append(dict(slug="moka", order=26, name="Moka",
    title="Moka : climatiseur monobloc sans unité extérieure | Pilotech Paris",
    description="Le Moka réunit tout le circuit dans une unité intérieure compacte : monobloc air-air à double circuit, 8 000 à 12 000 BTU/h, classe A, application Smart Life. Installé par Pilotech à Paris et en IDF.",
    category="Climatisation monobloc sans unité extérieure", type_label="Monobloc, une pièce",
    tagline="Tout-en-un compact, 2,3 à 3,5 kW", image=IMG["moka"], image_alt="Climatiseur monobloc Teknopoint Moka",
    lead="Le Moka est un monobloc : l'ensemble du circuit frigorifique tient dans une seule unité intérieure, à double circuit air-air, sans groupe dehors. Compact et sobre, il équipe un logement, un bureau ou une structure d'accueil quand la façade ne peut recevoir aucune machine.",
    facts=[("Monobloc", "Un seul appareil, à l'intérieur"), ("2,3 à 3,5 kW", "8 000 à 12 000 BTU/h"), ("Classe A", "Efficacité énergétique"), ("Réversible", "Dès 10 000 BTU/h", "warm"), ("Smart Life", "Application Wi-Fi"), ("Teknopoint", "Fabricant italien")],
    highlight=("La climatisation sans contrainte de pose", "Ni liaisons frigorifiques, ni groupe extérieur : un monobloc se pose vite et convient aux bâtiments soumis à des règles architecturales, de copropriété ou d'esthétique. Trois puissances couvrent une chambre comme un séjour."),
    features=["Technologie monobloc air-air à double circuit, sans unité extérieure.", "Trois versions : 8 000 BTU/h (2,3 kW), 10 000 BTU/h (2,9 kW, réversible) et 12 000 BTU/h (3,5 kW, réversible).", "Classe énergétique A.", "Compresseur DC Inverter à haut rendement, faible niveau sonore et faibles vibrations.", "Pilotage à distance par l'application Smart Life (iOS et Android) via le Wi-Fi domestique.", "Dessin épuré et installation simplifiée.", "Adapté aux logements, bureaux et structures d'accueil."],
    specs=[("Type", "Monobloc air-air à double circuit, sans unité extérieure"), ("Versions", "8 000 BTU/h (2,3 kW) ; 10 000 BTU/h (2,9 kW) ; 12 000 BTU/h (3,5 kW)"), ("Réversible", "Versions 10 000 et 12 000 BTU/h"), ("Classe énergétique", "A"), ("Compresseur", "DC Inverter"), ("Pilotage", "Application Smart Life, Wi-Fi")],
    controls=[("Application Smart Life", IMG["app"]), ("Classe énergétique A", CDN + "9b49b921-8c11-4c01-b6b7-a9e5d954fc2f/Class+A+teknopoint+pilotech.jpg")],
    brochure=BROCHURE_CAT,
    docs=[("Catalogue Teknopoint « Les Invisibles »", BROCHURE_CAT), ("Brochure climatisations invisibles Pilotech", BROCHURE_GEN)],
    gallery=[(IMG["moka"], "Climatiseur Moka"), (IMG["moka-2"], "Moka, autre vue"), (IMG["moka-salon"], "Moka installé dans un salon")],
    body="""## Le plus simple des Invisibles

Le Moka s'adresse à ceux qui veulent une seule pièce traitée, vite et sans travaux lourds : pas de liaison frigorifique à tirer, pas de groupe à fixer, l'appareil se pose contre un mur extérieur et rejette la chaleur par ses grilles. Les versions 10 000 et 12 000 BTU/h chauffent aussi.

## Ce que nous faisons

Choix de la puissance selon la pièce, percements avec finition côté façade, pose, raccordement électrique et paramétrage de l'application Smart Life. Une demi-journée à une journée selon le mur."""))

P.append(dict(slug="piccolo", order=27, name="Piccolo",
    title="Piccolo : le climatiseur sans unité extérieure le plus compact | Pilotech",
    description="Piccolo, 405 × 235 × 432 mm : le plus petit climatiseur sans bloc extérieur du marché, 3,6 ou 5,3 kW en froid seul, Full DC Inverter. Se cache dans un meuble ou sous un évier. Pose Pilotech à Paris.",
    category="Climatisation sans unité extérieure compacte", type_label="Sans unité extérieure, ultra-compact",
    tagline="405 × 235 × 432 mm, se cache dans un meuble", image=IMG["piccolo"], image_alt="Climatiseur Teknopoint Piccolo",
    lead="Le Piccolo est le modèle le plus compact de la famille des Invisibles : 405 × 235 × 432 mm, de quoi le loger dans un meuble, sous un évier, dans une salle de bains ou n'importe quel volume inutilisé. Deux puissances en rafraîchissement, une technologie Full DC Inverter et un niveau sonore réduit.",
    facts=[("405 × 235 × 432", "Millimètres, le plus compact du marché"), ("3,6 ou 5,3 kW", "Deux puissances"), ("Froid seul", "Rafraîchissement", "cool"), ("0 unité", "Extérieure"), ("DC Inverter", "Consommation réduite"), ("Teknopoint", "Fabricant italien")],
    highlight=("Là où rien d'autre ne rentre", "Une bijouterie, une réserve, un studio sous les toits : le Piccolo se glisse dans un placard bas ou un meuble de cuisine et libère la façade comme les murs. Son installation rapide en fait une alternative aux systèmes traditionnels quand la place manque."),
    features=["Le plus compact de la gamme : 405 × 235 × 432 mm.", "Deux puissances, 3,6 kW et 5,3 kW, en rafraîchissement seul.", "Aucune unité extérieure visible.", "Full DC Inverter : puissance modulée, consommation réduite, niveau sonore contenu.", "S'installe dans un meuble, sous un évier, dans une salle de bains ou un espace inutilisé.", "Installation simple et rapide."],
    specs=[("Type", "Climatiseur sans unité extérieure, monosplit"), ("Dimensions", "405 × 235 × 432 mm"), ("Puissances", "3,6 kW ; 5,3 kW"), ("Mode", "Rafraîchissement seul"), ("Technologie", "Full DC Inverter")],
    brochure=BROCHURE_GEN, docs=[("Brochure climatisations invisibles Pilotech", BROCHURE_GEN)],
    gallery=[(IMG["piccolo"], "Climatiseur Piccolo")],
    body="""## Une réponse aux petits volumes contraints

Le Piccolo a été retenu par nos clients commerçants, notamment une bijouterie où l'installation devait rester invisible et où chaque centimètre comptait. Il rafraîchit une pièce de taille modeste depuis un emplacement que l'on ne soupçonne pas.

## À savoir avant de choisir

Il ne chauffe pas : pour une pièce qui doit aussi être chauffée sans groupe extérieur, l'ELFO Monosplit ou le Moka réversible sont les alternatives. Nous en parlons lors de la visite."""))

P.append(dict(slug="cave-a-vin", order=28, name="Climatisation de cave à vin",
    title="Climatisation de cave à vin sans unité extérieure | Pilotech Paris",
    description="Wine ELFO : climatiseur basse température pour cave à vin, jusqu'à 10 °C, sans groupe extérieur, humidificateur intégré, classe A, DC Inverter, Wi-Fi. Étude et pose par Pilotech à Paris et en IDF.",
    category="Climatisation basse température pour cave à vin", type_label="Cave à vin, sans unité extérieure",
    tagline="Jusqu'à 10 °C, hygrométrie maîtrisée, rien en façade", image=IMG["cave"], image_alt="Climatisation de cave à vin Teknopoint Wine",
    lead="Une cave à vin demande une température basse et stable, et une hygrométrie tenue. Le climatiseur basse température Wine ELFO de Teknopoint descend jusqu'à 10 °C, régule l'humidité grâce à son humidificateur intégré et se passe de tout groupe extérieur : il s'installe dans un sous-sol parisien comme dans une maison.",
    facts=[("10 °C", "Température intérieure minimale", "cool"), ("Humidificateur", "Intégré"), ("0 unité", "Extérieure"), ("Classe A", "Efficacité énergétique"), ("DC Inverter", "Puissance modulée"), ("Wi-Fi", "Alexa et Google Home")],
    highlight=("Le climat d'une cave enterrée, reconstitué", "Autrefois, les caves fraîches et humides faisaient le travail. Le Wine ELFO le reproduit : froid régulé au degré près, humidité nébulisée pour maintenir les bouchons, et un appareil qui n'a aucun impact sur la façade de l'immeuble."),
    features=["Climatiseur basse température, conçu pour la conservation et le vieillissement du vin.", "Température intérieure jusqu'à 10 °C.", "Humidificateur intégré qui nébulise de l'eau pour maintenir l'hygrométrie dans les bonnes valeurs.", "Aucune unité de condensation extérieure : aucun impact sur la façade.", "Classe énergétique A, technologie DC Inverter, ventilateurs BLDC silencieux.", "Wi-Fi, compatible Alexa et Google Home.", "Convient aussi à la conservation de médicaments, de cosmétiques, de fleurs ou aux musées."],
    specs=[("Type", "Climatiseur basse température, sans unité extérieure"), ("Température minimale", "10 °C"), ("Humidité", "Humidificateur intégré"), ("Classe énergétique", "A"), ("Technologie", "DC Inverter, ventilateurs BLDC"), ("Pilotage", "Wi-Fi, Alexa, Google Home")],
    brochure=BROCHURE_GEN, docs=[("Brochure climatisations invisibles Pilotech", BROCHURE_GEN)],
    gallery=[(IMG["cave"], "Climatisation de cave à vin")],
    body="""## Une cave à vin en appartement ou en sous-sol

Les caves parisiennes ne sont pas toujours fraîches, et une pièce dédiée au vin dans un appartement ne l'est jamais. Le Wine ELFO recrée les conditions d'une bonne cave : une température basse et constante, une humidité suffisante pour que les bouchons ne sèchent pas, sans bruit ni vibrations excessives.

## Ce que nous étudions

Le volume à traiter, son isolation, la présence d'un mur extérieur pour les grilles ou l'alternative à eau, l'évacuation des condensats et l'alimentation en eau de l'humidificateur. Nous dimensionnons, posons et assurons l'entretien annuel."""))

P.append(dict(slug="unites-interieures", order=29, name="Unités intérieures",
    title="Unités intérieures Teknopoint : Duct Plus, SKIV, CASK, Console | Pilotech",
    description="Les unités intérieures compatibles avec les centrales ELFO et IDRA Next : Duct Plus et gainable pour une diffusion par gaines, SKIV, CASK et Console Int. Choisies pièce par pièce par Pilotech en IDF.",
    category="Unités intérieures pour climatisation sans unité extérieure", type_label="Unités intérieures ELFO et IDRA",
    tagline="Murale, console, cassette ou gainable, au choix", image=IMG["unites"], image_alt="Unités intérieures Teknopoint compatibles ELFO et IDRA Next",
    lead="Les centrales ELFO et IDRA Next ne diffusent pas l'air elles-mêmes : elles alimentent une ou plusieurs unités intérieures, choisies pièce par pièce. Teknopoint en propose cinq, murales, consoles, cassettes ou gainables, pour que le résultat reste aussi discret que la centrale.",
    facts=[("5 unités", "Duct Plus, gainable, SKIV, CASK, Console Int"), ("4 types", "Murale, console, cassette, gainable"), ("ELFO", "Compatibles"), ("IDRA Next", "Compatibles"), ("Pièce par pièce", "Choix selon l'usage"), ("Teknopoint", "Fabricant italien")],
    highlight=("La centrale se cache, l'unité intérieure se choisit", "Un gainable dans un faux plafond pour ne rien voir, une cassette dans un bureau, une console basse sous une fenêtre, une murale dans une chambre : chaque pièce a sa réponse, et toutes se raccordent à la même centrale."),
    features=["Duct Plus et unité gainable : diffusion par gaines et bouches, l'unité disparaît dans le faux plafond.", "SKIV, CASK et Console Int : unités apparentes, choisies selon la pièce et le style de l'intérieur.", "Compatibles avec les centrales ELFO (monosplit, multisplit, VRF) et IDRA Next (toutes versions).", "Combinaison libre de plusieurs types d'unités sur une même centrale multisplit.", "Sélection faite lors de la visite technique, en fonction du volume, du mobilier et des passages possibles."],
    specs=[("Unités disponibles", "Duct Plus, unité gainable, SKIV, CASK, Console Int"), ("Types", "Murale, console, cassette, gainable"), ("Compatibilité", "ELFO, IDRA Next, IDRA Eco, IDRA Next Ring")],
    controls=[("Duct Plus", IMG["duct-plus"]), ("Unité intérieure gainable", IMG["gainable"]), ("SKIV", IMG["skiv"]), ("CASK", IMG["cask"]), ("Console Int", IMG["console"])],
    brochure=BROCHURE_GEN, docs=[("Brochure climatisations invisibles Pilotech", BROCHURE_GEN)],
    gallery=[(IMG["unites"], "Unités intérieures Teknopoint"), (IMG["duct-plus"], "Duct Plus"), (IMG["gainable"], "Unité intérieure gainable"), (IMG["skiv"], "SKIV"), (IMG["cask"], "CASK"), (IMG["console"], "Console Int")],
    body="""## Comment nous choisissons

Le gainable est notre premier choix quand un faux plafond existe ou peut être créé : plus rien n'est visible à part les grilles. Sans faux plafond, la cassette convient aux bureaux et aux commerces, la console aux pièces basses de plafond ou en remplacement d'un radiateur, la murale aux chambres. Sur un multisplit, ces types se combinent.

## Une seule centrale, plusieurs pièces

Avec un ELFO Multisplit ou un IDRA Next multisplit, chaque unité garde son réglage. Le dimensionnement se fait pièce par pièce lors de la visite, en tenant compte de l'exposition, des vitrages et de l'usage."""))


def q(s):
    return '"' + s.replace('"', '\\"') + '"'


def write(p):
    lines = ["---", f"name: {q(p['name'])}", f"slug: {q(p['slug'])}", "universe: invisible", "brand: Teknopoint", f"order: {p['order']}",
             f"permalink: /climatisation-invisible/{p['slug']}/", f"title: {q(p['title'])}", f"description: {q(p['description'])}",
             f"category: {q(p['category'])}", f"type_label: {q(p['type_label'])}", f"tagline: {q(p['tagline'])}", f"image: {q(p['image'])}",
             f"image_alt: {q(p['image_alt'])}", f"lead: {q(p['lead'])}", "facts:"]
    for f in p["facts"]:
        tone = f", tone: {f[2]}" if len(f) > 2 else ""
        lines.append(f"  - {{ value: {q(f[0])}, label: {q(f[1])}{tone} }}")
    lines += ["highlight:", f"  title: {q(p['highlight'][0])}", f"  text: {q(p['highlight'][1])}", "features:"]
    lines += [f"  - {q(x)}" for x in p["features"]]
    lines.append("specs:")
    lines += [f"  - {{ label: {q(a)}, value: {q(b)} }}" for a, b in p["specs"]]
    if p.get("controls"):
        lines.append("controls:")
        lines += [f"  - {{ label: {q(a)}, img: {q(b)} }}" for a, b in p["controls"]]
    lines.append(f"brochure: {q(p.get('brochure', BROCHURE_GEN))}")
    docs = p.get("docs", [("Brochure climatisations invisibles Pilotech", BROCHURE_GEN)])
    lines.append("docs:")
    lines += [f"  - {{ title: {q(a)}, href: {q(b)} }}" for a, b in docs]
    lines.append("gallery:")
    lines += [f"  - {{ src: {q(a)}, alt: {q(b)} }}" for a, b in p["gallery"]]
    lines.append("---")
    out = "\n".join(lines) + "\n" + textwrap.dedent(p["body"]).strip() + "\n"
    Path(__file__).resolve().parent.parent.joinpath("_products", p["slug"] + ".md").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    for p in P:
        write(p)
    print(f"{len(P)} fiches écrites dans _products/")
