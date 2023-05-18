
# GoldenLine
GoldenLine-ecom app

# Présentation du site e-commerce

GoldenLine est une entreprise spécialisée dans les vêtements grande surface mais propose également d'autres types de produits tels que des articles multimédia, de jardinage ou des aliments. Elle est implantée partout en France avec une estimation de 3 millions de clients. 
Son site e-commerce présentent tous les produits présents en magasin.

Les clients peuvent commander des produits sans se connecter, la connexion est seulement pour les collaborateurs marketing de GoldenLine. Les collaborateurs connectés auront accès aux statistiques des données de l'application.

```
git clone https://github.com/aurelie4/ECOM.git
```

# Explication du code

Vous trouverez dans le dossier ECOM : 

- ECOM : les fichiers importants dans un projet Django qui contribuent au bon fonctionnement et à la configuration de l'application (wsgi.py, settings.py ...)
- shop : le fichier models.py contient les définitions des modèles de données de l'application.
         le fichier views.py contient les fonctions ou les classes de vue de l'application.
         le fichier utile.py contient le code utilisé plusieurs fois dans les vues, évite d'avoir des redondances de codes.
         le fichier urls contient les configurations des URL de l'application.
- static : 3 dossiers css, images (stokage des images du site) et js (code javascript)
- templates : base.html contient le code qui sera présent sur toutes les pages du site
              shop : contient les différents code html
-tests : contient le code des tests unitaires

