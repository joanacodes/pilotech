# Pilotech — site unifié

Site vitrine qui regroupe les trois sites de Pilotech :

- **Climatisation & chauffage Toshiba** (10 gammes), repris de `joanacodes/toshiba-pilotech`
- **Climatisation sans unité extérieure Teknopoint** (12 solutions), repris du site Squarespace `pilotech.eu`
- **Ventilation par insufflation VMI** (7 centrales), repris de `joanacodes/pilotech-vmi`

Le blog n'est pas encore intégré (voir « Blog » plus bas).

Jekyll, compatible GitHub Pages sans étape de build serveur : le CSS Tailwind est précompilé,
les polices sont auto-hébergées, aucun CDN ni script tiers (hors vidéos YouTube, chargées à la demande).

## Structure

```
_config.yml            Coordonnées, navigation, univers, collections — une seule source de vérité
_data/
  reviews.yml          Avis Google (citations clients)
  faq.yml              Questions fréquentes, par univers
  logements.yml        Sélecteur « par type de logement » de l'accueil
_products/*.md         29 fiches produits : toute la donnée est dans l'en-tête YAML, le texte long dans le corps
_layouts/
  default.html         Squelette de page (head, header, breadcrumb, footer)
  product.html         Gabarit unique des 17 fiches produits
  service.html         Gabarit des pages services (sections déclarées en YAML)
_includes/
  seo.html             <title>, description, canonical, Open Graph, données structurées (schema.org)
  header.html          En-tête avec les deux menus déroulants (gammes)
  footer.html, breadcrumb.html, product-card.html, form-devis.html, cta.html, reviews.html
  universe-index.html  Page catalogue d'un univers (groupes, tableau comparatif, FAQ)
  icons.html           Icônes SVG inline
index.html             Accueil
climatisation/         Catalogue Toshiba      climatisation-invisible/  Catalogue Teknopoint
ventilation/           Catalogue VMI          services/                 Hub + 5 pages
a-propos.html, contact.html, merci.html, mentions-legales.html, 404.html
assets/
  css/site.css         CSS compilé (ne pas éditer à la main, voir src/input.css)
  js/site.js           Menus, tiroir mobile, galerie, onglets, frise, formulaires
  fonts/               IBM Plex Sans + Plex Sans Condensed (woff2)
  img/climatisation/   Visuels Toshiba (identiques au site satellite)
  img/ventilation/     Visuels VMI            img/invisible/  Visuels Teknopoint (après localisation)
  brochures/           PDF constructeurs
src/input.css          Source Tailwind        tailwind.config.js  Palette et typographie
scripts/preview.py     Aperçu local sans Ruby
scripts/localize-external-images.sh   Rapatrie les visuels et PDF encore hébergés à l'extérieur
scripts/generate-teknopoint-products.py   Régénère les 12 fiches Teknopoint (données dans le script)
sitemap.xml, robots.txt
```

## Modifier le contenu

**Coordonnées, horaires, note Google, réseaux sociaux** : `_config.yml`, bloc `company`. Utilisées partout.

**Une fiche produit** : ouvrir `_products/<slug>.md`. Champs principaux :

| Champ | Rôle |
|---|---|
| `name`, `brand`, `universe`, `order` | Identité et position dans les listes |
| `title`, `description` | `<title>` (≤ 60 caractères) et meta description (≤ 155) |
| `type_label`, `tagline` | Chip et accroche des cartes |
| `image`, `image_alt`, `gallery` | Visuel principal (Open Graph) et galerie |
| `lead` | Paragraphe d'introduction |
| `facts` | Chiffres clés (`tone: warm` = chauffage, `tone: cool` = rafraîchissement) |
| `energy` | Classes énergétiques (pastilles) |
| `highlight` | Encart « point fort » |
| `features`, `features_note` | Liste des caractéristiques |
| `specs` | Fiche technique (tableau) |
| `supplied`, `schemas`, `controls`, `video_id`, `brochure`, `docs` | Sections optionnelles |

Le corps Markdown sous l'en-tête devient la section « texte long ».

**Ajouter un produit** : dupliquer une fiche, changer `slug`, `permalink`, `order`, ajouter les visuels dans `assets/img/…`.
Le produit apparaît automatiquement dans les menus, le footer, les catalogues, le sitemap et les données structurées.
Pour l'afficher dans le sélecteur de l'accueil ou les tableaux comparatifs, ajouter son `slug` dans `_data/logements.yml`
et dans le bloc `compare` de `climatisation/index.html` ou `ventilation/index.html`.

**Formulaires** : envoyés par FormSubmit à l'adresse `forms.destinataire` de `_config.yml`. Au tout premier envoi,
FormSubmit demande de confirmer l'adresse par e-mail (une seule fois). Les réponses arrivent dans la boîte mail, la page
`/merci/` est affichée au visiteur.

## Construire

```bash
npm install            # Tailwind + polices (une fois)
npm run css            # recompile assets/css/site.css après toute modification de gabarit ou de src/input.css
npm run preview        # aperçu local sans Ruby : construit _site/ (python3 + pip install python-liquid pyyaml markdown)
bundle exec jekyll serve   # aperçu avec le vrai Jekyll, si Ruby est installé
```

Le fichier `assets/css/site.css` doit être commité : GitHub Pages ne lance pas Tailwind.

## Déployer

1. Créer le dépôt GitHub, pousser la branche `main`.
2. Settings → Pages → Deploy from branch `main`, dossier `/ (root)`.
3. Ajouter un fichier `CNAME` à la racine contenant le nom de domaine, et renseigner le même domaine dans `url:`
   de `_config.yml` (actuellement `https://pilotech.eu`, à confirmer).
4. Lancer une fois `sh scripts/localize-external-images.sh` pour rapatrier les visuels Toshiba (bucket externe) et
   Teknopoint (CDN Squarespace) ainsi que les deux brochures PDF Teknopoint (voir `CONTENT-REVIEW.md`).
   Fournir ensuite `assets/img/invisible/piccolo.png` et `assets/img/invisible/cave-a-vin.png` (placeholders pour l'instant).
5. Déclarer `https://<domaine>/sitemap.xml` dans la Search Console.

## Choix techniques

- **Une seule source de vérité** : les fiches produits sont de la donnée (YAML) rendue par un gabarit unique, pas 17 pages HTML dupliquées.
- **SEO** : canonical, Open Graph, Twitter, et un graphe schema.org par type de page (HVACBusiness, WebSite,
  BreadcrumbList, Product + VideoObject, CollectionPage/ItemList, Service, FAQPage).
- **Contenu distinct des sites satellites** : toutes les descriptions ont été réécrites avec les mêmes faits ; seuls
  les avis clients (citations) sont repris tels quels.

## Blog

Le blog est volontairement absent de cette version. Les trois sites satellites publient 21 + 7 articles ; pour les
intégrer sans cannibaliser le référencement des satellites, chaque article devra être **réécrit** (mêmes sujets, mots
différents), avec sa propre image et sans `canonical_url` vers l'original. Le gabarit d'article et l'index pourront
être réintroduits à ce moment-là (`_layouts/post.html`, `blog/index.html`, `_posts/`).
- **Performance et RGPD** : polices auto-hébergées, aucun appel à Google Fonts ni CDN, icônes SVG inline,
  images en `loading="lazy"`, vidéos via `youtube-nocookie.com`.
- **Accessibilité** : navigation clavier des menus, onglets et galerie, `prefers-reduced-motion` respecté,
  focus visible, lien d'évitement.
