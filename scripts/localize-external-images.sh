#!/usr/bin/env sh
# Rapatrie dans assets/ tous les visuels et PDF encore hébergés à l'extérieur, puis met à jour
# les références dans _products/ et les pages. À lancer une fois, depuis la racine du dépôt :
#     sh scripts/localize-external-images.sh
# (Squarespace limite le nombre de requêtes : le script marque une pause entre chaque téléchargement.)
set -e
cd "$(dirname "$0")/.."

fetch() { # url  chemin_local
  if [ -f "$2" ]; then echo "déjà présent : $2"; else
    echo "→ $2"; mkdir -p "$(dirname "$2")"; curl -fsSL "$1" -o "$2"; sleep 2
  fi
  # remplace l'URL dans les fiches produits et les pages (guillemets ou non)
  grep -rl --include=*.md --include=*.html -F "$1" _products _includes . 2>/dev/null | grep -v node_modules | grep -v _site | xargs -r sed -i "s|$1|/$2|g"
}

# ---- Toshiba : six visuels sur un bucket UXPilot ----
U="https://storage.googleapis.com/uxpilot-auth.appspot.com/AwYCQYRWfMc2W3Qky94kDOsPiu42%2F"
D="assets/img/climatisation"
fetch "${U}5ae0e6fe-eae7-4333-a418-e5f70a6a5ef9.png" "$D/haori-main.png"
fetch "${U}f7d06d9f-4bd7-4ee5-b156-2c985616e217.png" "$D/daiseikai-10-main.png"
fetch "${U}310809a0-21c0-4a6e-9d57-e53bcae628cb.png" "$D/super-heating-main.png"
fetch "${U}9ca5345f-fcbc-4961-81e8-c981bd399c73.png" "$D/gainable-standard-main.png"
fetch "${U}176959d9-fab6-4395-b31c-8d905d815014.png" "$D/yukai-main.png"
fetch "${U}30966fb0-863e-430b-8d72-ad57830708c1.png" "$D/naka-main.png"

# ---- Teknopoint : visuels du site Squarespace pilotech.eu ----
S="https://images.squarespace-cdn.com/content/v1/6795159239530112bc66aee2/"
D="assets/img/invisible"
fetch "${S}6d24c9c3-2482-4b18-8205-f5f360a9fff9/elfo+vfr+teknopont+6+pilotech.png" "$D/elfo.png"
fetch "${S}9537c0d6-fd87-40e5-8b54-e484b42519ae/ELFO+CLIM+BGD+TRSPRT.png" "$D/elfo-hero.png"
fetch "${S}45c64e8a-4600-436d-a0db-6bf34b11be3f/elfo+vfr+teknopont+6+pilotech+%281%29.png" "$D/elfo-vrf.png"
fetch "${S}251dce26-b999-48d2-bcce-a582e40ce630/elfo+vfr+teknopont+6+pilotech.png" "$D/elfo-vrf-2.png"
fetch "${S}7721bf2c-e508-4407-b803-b03747809329/IDRA+teknopont+6+pilotech.png" "$D/idra-next.png"
fetch "${S}f31bd7ab-39f6-434b-87f2-5afdb2dce904/IDRA+teknopont+6+pilotech+%281%29.png" "$D/idra-eco.png"
fetch "${S}446c0d17-1949-4594-b207-e0d2a4750941/IDRA+teknopont+6+pilotech+%282%29.png" "$D/idra-ring.png"
fetch "${S}c8f70c48-7ada-46a8-969f-c6dc6239b267/MOKA+PILOTECH.png" "$D/moka.png"
fetch "${S}978e90bd-51e9-4b04-a7f6-041e81bb1dca/MOKA+PILOTECH+2.png" "$D/moka-2.png"
fetch "${S}eb202a90-610b-4758-819e-ec46f3cddb71/MOKA+LIVING+ROOM.png" "$D/moka-salon.png"
fetch "${S}57f61d93-11e0-4c99-b5aa-382cacd21c59/elfo+vfr+teknopont+6+pilotech+%282%29.png" "$D/unites-interieures.png"
fetch "${S}cc97fe4c-7a8b-437c-9075-69b9242ee032/DUCT+PLUS+TEKNOPOINT+PILOTECH.jpg" "$D/duct-plus.jpg"
fetch "${S}57fb2cee-7ef4-430a-b87b-e7776dcd5181/UNITE+GENERALE+TEKNOPOINT+PILOTECH.jpg" "$D/gainable.jpg"
fetch "${S}39222ca9-df84-4ad1-9533-bcc9d2b2704b/SKIV+TEKNOPOINT+PILOTECH.jpg" "$D/skiv.jpg"
fetch "${S}55f2fa34-51e7-4222-b125-a0ea7bc6a0d9/CASK+TEKNOPOINT+PILOTECH.jpg" "$D/cask.jpg"
fetch "${S}52e41d6a-34ca-49e4-947f-5638bcf7427f/CONSOLE+INT.jpg" "$D/console-int.jpg"
fetch "${S}b69aed57-d5b2-40c5-a0d7-c57e269e3b97/Schema+Teknopoint+Pillotehc.png" "$D/schema-teknopoint.png"
fetch "${S}26894eea-bf18-42b7-8b55-35529c810cfd/DC+INVERTER+EFLO+MULTISPLIT+PILOTECH.jpg" "$D/dc-inverter.jpg"
fetch "${S}0fc23afe-3e20-4b3b-9f08-d7b033e2dd0d/1568022342-accessoriesRisparmio-Idrico.jpg" "$D/economie-eau.jpg"
fetch "${S}f63c5cc1-a7ae-44a4-beb1-15608d60423b/1568023602-accessoriesUltra+silenzioso.jpg" "$D/silence.jpg"
fetch "${S}1fbb314d-8614-48b6-a116-be0c08c487ea/1584543418-accessoriesthinkstockphotos-578584200.jpg" "$D/classe-a3.jpg"
fetch "${S}d9b81eba-e41c-488e-9ce5-0e540cc9bcab/pilotech+moka+app.jpg" "$D/moka-app.jpg"
fetch "${S}9b49b921-8c11-4c01-b6b7-a9e5d954fc2f/Class+A+teknopoint+pilotech.jpg" "$D/moka-classe-a.jpg"

# ---- Teknopoint : brochures PDF ----
D="assets/brochures/invisible"
fetch "https://www.pilotech.eu/s/CLIMATISATIONS-INVISIBLES-PILOTECH-CLIM-3.pdf" "$D/climatisations-invisibles-pilotech.pdf"
fetch "https://www.pilotech.eu/s/1779873737-productsCAT_Les_Invisibles_Die_Unsichtbaren_FRA_DE-rllw.pdf" "$D/catalogue-teknopoint-les-invisibles.pdf"

echo
echo "Terminé. Restent à fournir manuellement : assets/img/invisible/piccolo.png et assets/img/invisible/cave-a-vin.png"
echo "Vérification : grep -rn 'squarespace-cdn\|storage.googleapis\|pilotech.eu/s/' _products climatisation-invisible  (ne doit rien retourner)"
