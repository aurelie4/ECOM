import sys    
sys.path.append("..")     
from shop.models import Client, Commande, AddressChipping
from django.test import TestCase
from django.contrib.auth.models import User



class CommandeTestCase(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        user = User.objects.create_user(username='testuser', password='testpassword')
        # Créer un client de test
        client = Client.objects.create(user=user, name='John Doe', email='john.doe@example.com')
        # Créer une commande de test
        Commande.objects.create(client=client, total_trans=100.00)

    def test_commande_str(self):
        # Vérifier la représentation en chaîne de la commande
        commande = Commande.objects.get(total_trans=100.00)
        self.assertEqual(str(commande), str(commande.id))

    def test_commande_produit_physique(self):
        # Vérifier si la commande contient un produit physique
        commande = Commande.objects.get(total_trans=100.00)
        self.assertFalse(commande.produit_physique)

    #def test_commande_get_panier_total(self):
        # Vérifier le calcul du prix total du panier
    #    commande = Commande.objects.get(total_trans=100.00)
    #    self.assertEqual(commande.get_panier_total, 100.00)

    def test_commande_get_panier_article(self):
        # Vérifier le calcul du nombre d'articles dans le panier
        commande = Commande.objects.get(total_trans=100.00)
        self.assertEqual(commande.get_panier_article, 0)

class AddressChippingTestCase(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        user = User.objects.create_user(username='testuser', password='testpassword')
        # Créer un client de test
        client = Client.objects.create(user=user, name='John Doe', email='john.doe@example.com')
        # Créer une commande de test
        commande = Commande.objects.create(client=client, total_trans=100.00)
        # Créer une adresse de livraison de test
        AddressChipping.objects.create(client=client, commande=commande, addresse='123 Rue du Test', ville='Testville', zipcode='12345')

    def test_addresschipping_str(self):
        # Vérifier la représentation en chaîne de l'adresse de livraison
        address = AddressChipping.objects.get(addresse='123 Rue du Test')
        self.assertEqual(str(address), address.addresse)








    