import random
from django.utils import timezone
from faker import Faker
from django.contrib.auth.models import User
from .models import Client, CategorieSocio, Produit, Category, Commande, CommandeArticle, AddressChipping


fake = Faker()

# créer des clients fictifs
for i in range(10):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    name = fake.name()
    nb_enfants = random.randint(0, 5)
    categ = CategorieSocio.objects.create(
        nom_categ=fake.word(),
        description=fake.text(max_nb_chars=150)
    )
    user = User.objects.create_user(username=username, email=email, password=password)
    client = Client.objects.create(
        user=user,
        name=name,
        email=email,
        nb_enfants=nb_enfants,
        CategorieSocio=categ
    )

# créer des catégories de produits
for i in range(5):
    Category.objects.create(
        name=fake.word(),
        description=fake.text(max_nb_chars=150)
    )

# créer des produits
for i in range(20):
    category = random.choice(Category.objects.all())
    Produit.objects.create(
        Category=category,
        name=fake.word(),
        price=random.uniform(10.0, 100.0),
        digital=random.choice([True, False]),
        image=None,
        date_ajout=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
    )

# créer des commandes fictives
for i in range(10):
    client = random.choice(Client.objects.all())
    status = random.choice(['En cours de traitement', 'En attente de paiement', 'Paiement effectué', 'Commande terminée'])
    transaction_id = fake.uuid4()
    total_trans = sum(random.uniform(10.0, 100.0) for i in range(3))
    commande = Commande.objects.create(
        client=client,
        complete=random.choice([True, False]),
        transaction_id=transaction_id,
        status=status,
        total_trans=total_trans
    )
    
    # ajouter des articles de commande
    produits = Produit.objects.all()
    for j in range(random.randint(1, 5)):
        produit = random.choice(produits)
        quantite = random.randint(1, 10)
        CommandeArticle.objects.create(
            produit=produit,
            commande=commande,
            quantite=quantite,
            date_added=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
        )

    # ajouter des adresses de livraison
    addresse = fake.address()
    ville = fake.city()
    zipcode = fake.zipcode()
    AddressChipping.objects.create(
        client=client,
        commande=commande,
        addresse=addresse,
        ville=ville,
        zipcode=zipcode,
        date_ajout=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
    )