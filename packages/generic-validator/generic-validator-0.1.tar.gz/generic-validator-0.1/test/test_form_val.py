import unittest
from validateur_generique.form_val import FormValidator
import os
import sys


# Add the path to the sys.path for the validateur_generique module
sys.path.append(os.path.join(os.path.dirname(r'C:\Users\Acer\Desktop\validateur_generique\form_val'), 'validateur_generique'))

class TestFormValidator(unittest.TestCase):
    def test_valid_form(self):
        # Creation du schema
        schema = {
            'nom': r'^[A-Za-z0-9_]{3,20}$',
            'mot_de_passe': r'^.{8,}$',
            'confirmation_de_mot_de_passe': r'^.{8,}$',
            'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'daten': r'^\d{2}-\d{2}-\d{4}$'
        }
        validator = FormValidator(schema)

        # Saisie de données pour le schema (for testing purposes)
        test_data = {
            'nom': 'ValidName123',
            'mot_de_passe': 'SecurePwd123',
            'confirmation_de_mot_de_passe': 'SecurePwd123',
            'email': 'test@example.com',
            'daten': '01-01-2000',
        }

        # Verifie si aucune erreur n'a ete detectee lors de la validation.
        errors = validator.validate(test_data)
        self.assertIsNone(errors)

    def test_invalid_form(self):
        # Another schema for the invalid form test
        schema = {
            'nom': r'^[A-Za-z0-9_]{3,20}$',
            'mot_de_passe': r'^.{8,}$',
            'confirmation_de_mot_de_passe': r'^.{8,}$',
            'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'daten': r'^\d{2}-\d{2}-\d{4}$'
        }
        validator = FormValidator(schema)

        # Enter invalid form data (for testing purposes)
        test_data = {
            'nom': 'InvalidName@123',  # Invalid nom
            'mot_de_passe': 'WeakPwd',  # Invalid mot_de_passe
            'confirmation_de_mot_de_passe': 'DifferentPwd',  # Invalid confirmation_de_mot_de_passe
            'email': 'invalidemail',  # Invalid email
            'daten': '2000-01-01',  # Invalid daten
        }

        errors = validator.validate(test_data)
        expected_errors = {
            'nom': 'Invalid nom',
            'mot_de_passe': 'Invalid mot_de_passe',
            'confirmation_de_mot_de_passe': 'Invalid confirmation_de_mot_de_passe',
            'email': 'Invalid email',
            'daten': 'Invalid daten',
        }
        self.assertEqual(errors, expected_errors)
