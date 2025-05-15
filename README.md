# Projet IA QUARTO

## Nom des membres du binome : 
- Aberkane Ayoub – Matricule : 23218
- El Kadi Manar  – Matricule : 23346

## Objectif
Le but ici est de crééer une ia pour jouer au jeu Quarto qui choisit les bons coups.

## Bibliothèques utilisées
- Python :  
- Random : choisir une position ou une pièce au pif quand l’IA ne peut pas gagner directement ou ne sait pas quelle pièce donner.
- Socket : Permet de communiquer avec le serveur du tournoi a l'aide des connexions réseau (envoyer/recevoir).
- Json : Utilisé pour encoder et décoder les messages échangés avec le serveur, car ils sont envoyés au format JSON.
- Threading : Sert à lancer le serveur local en parallèle pour qu’il puisse écouter sans bloquer le reste du programme.

## Stratégie (à compléter)
À chaque tour de jeu, notre IA commence par vérifier si elle peut poser la pièce reçue à un endroit qui lui permet de gagner directement. Si une position qui permet de gagner est détectée, elle joue ce coup. De même, à chaque tour l'IA fait en sorte de ne pas donner une pièce gagnante à l'adversaire en détéctant d'abord les positions gagnantes et les pièces disponibles.

## Lancement
L'IA est appelée par le gestionnaire de tournoi grace au fichier `client.py`.
