from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from datetime import datetime
from .utile import commandeAnonyme, data_cookie, panier_cookie
from .models import Category
from django.views.decorators.csrf import csrf_exempt
import random
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from .models import CategorieSocio, Client, Category, Produit, Commande, CommandeArticle, AddressChipping
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from decimal import Decimal

from django.http import HttpResponse
from django.db.models import Sum, Avg, Count, DecimalField, ExpressionWrapper, F

import matplotlib.pyplot as plt
import numpy as np

@login_required
def statistiques(request):
    # Récupérer les dépenses par catégorie en fonction de la catégorie socioprofessionnelle
    categories = CategorieSocio.objects.all()
    depenses_par_categorie = []
    depense_panier_moyen = []

    for categorie in categories:
        # Calculez les dépenses pour chaque catégorie socioprofessionnelle
        depenses = Commande.objects.filter(client__CategorieSocio=categorie).values_list('total_trans', flat=True)
        depenses_par_categorie.append(sum(depenses))

        # Calculez la dépense moyenne du panier pour chaque catégorie socioprofessionnelle
        nb_commandes = Commande.objects.filter(client__CategorieSocio=categorie).count()
        if nb_commandes > 0:
            depense_moyenne = sum(depenses) / nb_commandes
        else:
            depense_moyenne = 0
        depense_panier_moyen.append(depense_moyenne)

    # Convertir les valeurs Decimal en float
    depenses_par_categorie = [float(d) for d in depenses_par_categorie]
    depense_panier_moyen = [float(d) for d in depense_panier_moyen]

    context = {
        'depenses_par_categorie': depenses_par_categorie,
        'depense_panier_moyen': depense_panier_moyen,
        'categories_labels': [categorie.nom_categ for categorie in categories]
    }

    return render(request, 'shop/statistiques.html', context)

def filtre_produit(request):
    selected_category_id = request.GET.get('category_id')  # Utilisation de 'category_id' pour le champ de clé primaire
    if selected_category_id:
        selected_category = Category.objects.get(id=selected_category_id)
        produits = Produit.objects.filter(Category=selected_category)
    else:
        produits = Produit.objects.all()

    context = {
        'selected_category': selected_category_id,  # Utilisation de 'selected_category_id' au lieu de 'selected_category'
        'produits': produits,
    }
    return render(request, 'shop/filtre_produit.html', context)


def shop(request, *args, **kwargs):
    """ vue principale """

    produits = Produit.objects.all()
    data = data_cookie(request)
    nombre_article = data['nombre_article']

    context = {
        'produits':produits,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):
    """ panier """
    
    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles':articles,
        'commande':commande,
        'nombre_article':nombre_article
    }

    return render(request, 'shop/panier.html', context)


def commande(request, *args, **kwargs):
    """ Commande """

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles':articles,
        'commande':commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/commande.html', context)    


@csrf_exempt
def update_article(request, *args, **kwargs):

    data = json.loads(request.body)

    produit_id = data['produit_id']

    action = data['action']

    client = request.user.client

    produit = Produit.objects.get(id=produit_id)

    commande, created = Commande.objects.get_or_create(client=client, complete=False)

    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    if action == 'add':

        commande_article.quantite += 1

    if action == 'remove':

        commande_article.quantite -= 1

    commande_article.save()

    if  commande_article.quantite <= 0:

        commande_article.delete()        

    return JsonResponse("Article ajouté", safe=False)


def traitementCommande(request, *args, **kwargs):
   
    transaction_id = datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)
    else:
        client, commande = commandeAnonyme(request, data)

    total = float(data['form']['total'])

    commande.transaction_id = transaction_id


    if commande.get_panier_total == total:

        commande.complete = True
    commande.save()       

    if commande.produit_physique:

        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse = data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse("Votre paiement a été effectué avec succès, votre commande est en cours de préparation !", safe=False)



#définir des données aléatoires
fake = Faker()

@staff_member_required  # Décorateur pour restreindre l'accès aux administrateurs uniquement
@login_required  # Décorateur pour restreindre l'accès aux utilisateurs connectés uniquement
def generer_donnees_aleatoires(request):
    if request.method == 'POST':
        # Supprimer toutes les données existantes (si nécessaire)
        AddressChipping.objects.all().delete()
        CommandeArticle.objects.all().delete()
        Commande.objects.all().delete()
        Produit.objects.all().delete()
        Category.objects.all().delete()
        Client.objects.all().delete()
        CategorieSocio.objects.all().delete()
        User.objects.all().delete()

    # Générer les catégories socio-professionnelles
    categories = ['Cadre', 'Retraité', 'Artisan','Employé']
    for categorie in categories:
        CategorieSocio.objects.create(
            nom_categ=categorie,
            description=fake.text()
        )

    # Générer les clients
    for _ in range(10):  # Générer 10 clients par exemple
        username = fake.user_name()
        email = fake.email()
        name = fake.name()
        nb_enfants = random.randint(0, 5)
        categorie_socio = random.choice(CategorieSocio.objects.all())


        Client.objects.create(
            name=name,
            email=email,
            nb_enfants=nb_enfants,
            CategorieSocio=categorie_socio
        )

    # Générer les catégories
    categories = ['Vêtements', 'Alimentaire', 'Jardinage', 'Multimédia']
    for categorie in categories:
        Category.objects.create(
            name=categorie,
            description=fake.text()
        )

    # Générer les produits
    for _ in range(20):  # Générer 20 produits par exemple
        category = random.choice(Category.objects.all())
        name = fake.word()
        price = random.uniform(1, 100)
        digital = random.choice([True, False])
        image = fake.image_url()
        date_ajout = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=timezone.utc)

        Produit.objects.create(
            Category=category,
            name=name,
            price=price,
            digital=digital,
            image=image,
            date_ajout=date_ajout
        )

    # Générer les commandes
    for _ in range(5):  # Générer 5 commandes par exemple
        client = random.choice(Client.objects.all())
        date_commande = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=timezone.utc)
        complete = random.choice([True, False])
        transaction_id = fake.uuid4()
        status = random.choice(['ACCEPTED', 'COMPLETED', 'SUCCESS'])
        total_trans = random.uniform(10, 100)

        commande = Commande.objects.create(
            client=client,
            date_commande=date_commande,
            complete=complete,
            transaction_id=transaction_id,
            status=status,
            total_trans=total_trans
        )

        # Générer les articles de commande
        produits = random.sample(list(Produit.objects.all()), k=random.randint(1, 5))

        for produit in produits:
            quantite = random.randint(1, 10)
            date_added = fake.date_time_between_dates(datetime_start=date_commande, datetime_end=timezone.now(), tzinfo=timezone.utc)

            commande_article = CommandeArticle.objects.create(
                produit=produit,
                commande=commande,
                quantite=quantite,
                date_added=date_added
            )

        # Générer les adresses de livraison
        if complete and commande.produit_physique:
            addresse = fake.street_address()
            ville = fake.city()
            zipcode = fake.zipcode()
            date_ajout = fake.date_time_between_dates(datetime_start=date_commande, datetime_end=timezone.now(), tzinfo=timezone.utc)

            AddressChipping.objects.create(
                client=client,
                commande=commande,
                addresse=addresse,
                ville=ville,
                zipcode=zipcode,
                date_ajout=date_ajout
            )
        return redirect('accueil')  # Rediriger vers la page d'accueil ou une autre page appropriée
    else:
        return render(request, 'generer_donnees_aleatoires.html')  # Afficher le formulaire ou le bouton de génération
