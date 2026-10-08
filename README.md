# Dolce Residences by Wyndham — Al Marjan Island

Site éditorial statique en **EN / FR / ES / NL / DE / PT**. Domaine canonique : `https://dolce-residences-almarjan.com`.

## Aperçu local

Depuis ce dossier, avec Python 3.9 ou plus récent :

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory docs
```

Ouvrir **http://127.0.0.1:4173/fr/**. Aucun paquet à installer pour générer, tester ou prévisualiser. Les fichiers `docs/` peuvent aussi être servis tels quels.

## Publication

Le dépôt public est `JeremyPalmDubai/dolce-residences-almarjan`.
GitHub Pages : publier la branche **main**, dossier **/docs**.
Adresse attendue après publication : `https://jeremypalmdubai.github.io/dolce-residences-almarjan/fr/`.
Les liens et ressources sont relatifs pour fonctionner à la racine d'un domaine, dans GitHub Pages et en local.

Pour un hébergement statique externe, transférer le **contenu** de `docs/` dans le dossier public. Il ne faut pas lancer de serveur Node en production.

## Domaine et SEO

Les 42 pages localisées possèdent un H1, une description, une canonique, six hreflang réciproques et x-default. Accueil anglais également disponible à la racine avec canonique `/en/`. Données structurées WebPage et BreadcrumbList. `sitemap.xml`, `sitemap-images.xml`, `robots.txt` et favicon inclus.

Le domaine canonique est préparé dans le code. La connexion DNS, la validation HTTPS et les redirections HTTP / www doivent être configurées chez l'hébergeur retenu. Aucun CNAME GitHub n'est activé par le code tant que le domaine ne pointe pas vers cet hébergement, afin de conserver un aperçu fonctionnel. Les sitemaps ne doivent être soumis à Google Search Console qu'après la mise en ligne du domaine. Aucune première place Google ni indexation n'est garantie.

## Contenu et prudence commerciale

- Prix d'appel **global** : 1 400 000 AED, soit environ 381 212 USD. Source : brief utilisateur.
- Réservation **30 %** : 420 000 AED ; remise des clés **70 %** : 980 000 AED sur cet exemple. Aucun paiement après remise des clés, aucun calendrier mensuel inventé. Frais en supplément, non chiffrés.
- Conversion indicative : 1 USD = 3,6725 AED, arrondie au dollar. Référence : [Banque centrale des EAU](https://centralbank.ae/umbraco/Surface/Exchange/GetExchangeRateAllCurrency).
- Studios, 1BR, 2BR, 3BR : aucune surface, aucun prix individuel ni disponibilité ferme inventés. La brochure n'offre pas de plans d'appartement approuvés ; le plan de parcelle est identifié comme tel.
- 93 résidences et T4 2028 : données **prévisionnelles** de la brochure conceptuelle, pages 5 et 16.
- Golden Visa : conditionnel, sans promesse. Le prix d'appel seul est inférieur au seuil de 2 M AED présenté par [l'ICP](https://icp.gov.ae/en/services-details/?serviceid=68e34eea5ae59b00117383d5).

## Images

Le hero utilise le rendu fourni explicitement par l'utilisateur le 8 octobre 2026. Les rendus du projet sont extraits de la brochure fournie. Les planches d'ambiance intérieure (pages 12–13, Courtesy Wyndham) sont distinguées des rendus Dolce. Deux illustrations d'Al Marjan sont présentées dans la section destination, sans promesse de vue.

L'image `/mnt/data/image.png` de l'ancienne conversation n'était pas accessible sur ce poste. `MarjanIsland2030.png`, présent dans les téléchargements locaux, sert de remplacement explicite. Le second visuel fourni, `Image Codex 24 sept. 2026, 15_45_24.png`, a été retrouvé. Provenance détaillée dans `content/assets.json`. WebP avec variantes 800 px, dimensions explicites et chargement différé hors hero. Filigrane d'affichage uniquement.

## Tally et confidentialité

L'embed **kdVP5j** est présent sur toutes les pages avec le script officiel et un lien de secours. Aucun faux prospect n'est envoyé pour tester. Le formulaire externe conserve les libellés configurés dans Tally ; ils sont actuellement en anglais, indépendamment de la langue du site. Les paramètres `page_language` et UTM sont transmis dans l'URL mais leur réception comme champs cachés ne peut pas être garantie sans vérifier la configuration du formulaire.

La page de confidentialité décrit les services utilisés. L'identité juridique du responsable du formulaire, son contact, ses durées de conservation et ses éventuels consentements marketing restent à compléter avec ses informations exactes. Aucun identifiant, document personnel ni secret n'est inclus dans ce dépôt. Les images et marques restent la propriété de leurs ayants droit ; la publication du code ne leur attribue pas une licence libre.

## Modifier et régénérer

- `content/project.json` : données commerciales et domaine.
- `content/locales.json` : six traductions complètes du site (hors formulaire externe).
- `content/assets.json` : sources et dimensions des images.
- `public/assets/` : styles, interactions et images optimisées.
- `scripts/build.py` : générateur unique des pages et sitemaps.
- `scripts/validate.py` : contrôles des liens, ancres, ressources, SEO, langues et calculs.
- `docs/` : résultat publié. Après chaque modification, régénérer et inclure ce dossier dans le commit.

Le projet de référence esthétique n'a pas été modifié ni republié.
