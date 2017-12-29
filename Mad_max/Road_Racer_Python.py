# ##############################################################
# "Moteur" de Jeu 2D developpé par Olivier CHAUMETTE,
# professeur d'ISN au lycee JP Sartre - 69 BRON,
# dans un but d'appropriation par des eleves de l'enseignement ICN en 2nde
# ##############################################################
# les élèves ont à modifier tout l'environnement graphique, choisir un gameplay
# (bonus, vitesse, nbre de vies, santé...)
# Les plus avancés pourront créer et gérer un nouveau groupe de SPRITES
# ##############################################################"

# code indispensable pour gerer l'UTF-8 en python 2.7 (inutile en Python 3)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import time
import pygame #importation de pygame
import traceback #module pour recuperer des infos sur les erreurs
from pygame.locals import * #on importe les constantes de pygame
import sys
import random
import math

pygame.init() #on lance pygame
pygame.mixer.init() # initialisation des sons

# ###############################"
# Couleurs utilisées
# ##############################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# #################################################
# FONCTIONS
# #################################################
def Affiche_Texte(surface, texte, taille, x, y, couleur):
    # Affichage d'un texte sur la surface voulue à la taille choisie
    # RQ: cette méthode évite les bug du à la non fermeture du module font de pygame
    """ on définit ci-dessous la police avec
    pygame.font.match_font('nom de la police', bold=True ou False, italic= True ou False) """
    font_name = pygame.font.match_font('arial', bold=True)
    font = pygame.font.Font(font_name, taille)
    text_surface = font.render(texte, True, couleur)       # True pour l'anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# #################################################
# OBJETS du JEU: ils sont de type SPRITE
# #################################################
# objet Player:   Mon_joueur= Player(abscisse, ordonnée)
# --------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, x,y):
        # définition de l'objet "Player": on le créé avec x et y comme argument et a comme propriétés: image, rect et Health
        pygame.sprite.Sprite.__init__(self)         # c'est un SPRITE
        self.image = pygame.image.load("images\Joueur.png").convert_alpha()         # image du joueur
        self.rect =self.image.get_rect()    # rectangle de l'image: bien l'appeler "rect" pour que le module SPRITE le reconnaisse
        self.Health = 100                   # "santé" du joueur à 100 au départ
        self.rect.left=x                    # place place la gauche du rectangle à l'abscisse X
        self.rect.top=y                     # place place le haut du rectangle à l'ordonnée Y
        self.hors_piste = 0
    def move(self, DeplacementX,DeplacementY):
        # méthode que l'on peut appliquer à l'objet de type "Player": bouger de valeurs "DeplacementX" et "DeplacementY"
        # par exemple:    Mon_Joueur.move(5,0)   déplace le joueur à droite de 5 pixels

        self.rect = self.rect.move(DeplacementX,DeplacementY)   # on déplace le rectangle
        if self.rect.right > 400:                          # tests pour que le joueur
            self.rect.right = 400                          # ne sorte pas de l'écran

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top<0:
            self.rect.top=0

        if self.rect.bottom>600:
            self.rect.bottom=600

    def update(self):
        """ Mettre ici  éventuellement des conditions sur la sortie de route
        qui entraine une baisse de la santé: variable Joueur.Health """
        global danger
        if self.rect.right > 300:
            if self.hors_piste>5:
                self.Health -= 1
                self.hors_piste = 0
            danger = 1

        elif self.rect.left < 100 :
            if self.hors_piste>5:
                self.Health -= 1
                self.hors_piste = 0
            danger = 1
        else:
            danger = 0
        self.hors_piste += 1
# objet "Ennemy":   Mon_Ennemi= Ennemy()
# --------------------------------------
class Ennemy(pygame.sprite.Sprite):
    def __init__(self):
        # création de l'objet Ennemy qui sera un SPRITE. On définit ses propriétés: (image, rect, speed)
        pygame.sprite.Sprite.__init__(self)          # on dit que Ennemy est un SPRITE (classe spéciale de pygame)
        global Liste_images_Ennemis                          # liste qui contient les noms des fichiers images
        global vitesse_scrolling                        # on aura besoin de la vitese du scrolling
        liste_positions_possible=[100,133,166,200,233,266]  # liste des abscisses possibles pour les ennemis (pour ne pas avoir 2 ennemis qui se chevauchent)
        self.image = random.choice(Liste_images_Ennemis)   # on prend un nom d'image au hasard dans la liste des images d'ennemis
        self.rect =self.image.get_rect()                # rectangle de l'image de l'objet: bien l'appeler "rect" pour que le module SPRITE reconnaisse la propriété
        self.speed = vitesse_scrolling + Temps/10           # vitesse de déplacemnt de l'ennemi allignée sur le scrolling
        self.rect.left =random.choice(liste_positions_possible)       # coordonnées prises au hasard
        self.rect.top=-80

    def move(self):
        # méthode qui s'applique sur l'objet ennemy: déplace vers le bas de la valeur "speed" associée à l'objet
        # par exemple:  Mon_Ennemi.move()
        global vitesse_scrolling
        self.speed = vitesse_scrolling+ 3 +  Temps/10
        self.rect = self.rect.move(0, self.speed)

    def update(self):
        # méthode qui sera appelée chaque fois qu'on mettra à jour les sprites de l'écran
        self.move()                            # à chaque appel de mise à jour Tous_les_sprites.update, on bouge l'énnemi
        if self.rect.top > 600:                # si le mouvement de l'ennemi l'ammène hors de l'écran
            self.kill()                        # on détruit l'objet pour qu'il ne s'affiche plus

""" On peut créer ici une classe "Bonus", comme les ennemis.
Sur le même principe, les bonus auront une méthode MOVE
et dans UPDATE, ils seront "killé" dès qu'ils auront quitté l'écran
"""
class Element_Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global Liste_image_Bonus
        global vitesse_scrolling
        liste_positions_possibles=[100,133,166,200,233,266]
        self.image = random.choice(Liste_image_Bonus)
        self.rect = self.image.get_rect()
        self.speed = vitesse_scrolling
        self.rect.left =random.choice(liste_positions_possibles)
        self.rect.bottom=-10
    def move(self):
        # méthode qui s'applique sur l'objet ennemy: déplace vers le bas de la valeur "speed" associée à l'objet
        # par exemple:  Mon_Ennemi.move()
        global vitesse_scrolling
        self.speed = vitesse_scrolling
        self.rect = self.rect.move(0, self.speed)

    def update(self):
        self.move()
        if self.rect.top > 600:
            self.kill()

# objet "Element de décor":   Mon_Decor = Element_Decor ("G")  ou ("D") suivant l'endroit où il doit être placé
# --------------------------------------
class Element_Decor(pygame.sprite.Sprite):
    def __init__(self,direction):
        # création de l'objet Element de décor qui sera un SPRITE. On définit ses propriétés: (image, rect, speed)
        pygame.sprite.Sprite.__init__(self)          # on dit que Element de decor est un SPRITE
        global Liste_images_Decor                            # liste qui contient les noms des fichiers images
        global vitesse_scrolling                    # on aura besoin de la vitesse du scrolling
        self.image = random.choice(Liste_images_Decor)           # on prend un nom d'image au hasard dans la liste des images décor
        """ les éléments de décor sont des blocs de 100x100 pixels """
        self.rect = self.image.get_rect()                # rectangle de l'image de l'objet
        self.speed = vitesse_scrolling             # le décor doit aller à la vitesse du scrolling
        if direction=="G":                          # si le décor est à gauche
            self.rect.left =0       # coordonnées à gauche
        else:
            self.rect.left =300    # coordonnées à droite
        self.rect.top=-100

    def update(self):
        # méthode qui sera appelée chaque fois qu'on mettra à jour les sprites de l'écran
        global vitesse_scrolling
        self.speed = vitesse_scrolling
        self.rect = self.rect.move(0, self.speed)           # à chaque appel de mise à jour Tous_les_sprites.update, on bouge le décor
        if self.rect.top > 600:                # si hors de l'écran
            self.kill()                        # on détruit l'objet pour qu'il ne s'affiche plus

# objet "Explosion":   Mon_Explosion= Explosion(x,y) - avec animation à partir de 4 images
# --------------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        # création de l'objet Explosion qui sera un SPRITE. On définit ses propriétés: (image, rect, index, animation_frame)
        pygame.sprite.Sprite.__init__(self)
        global images_explosions
        self.index=0                            # index: propriété qui donne l'image utilisée dans la liste. Au début, la n°0
        self.image=images_explosions[self.index]       # L'image de l'explosion en cours est la première de la liste des images d'explosion
        self.rect=self.image.get_rect()                     # on définit le REctangle autour de l'image
        self.rect.top=y+20                                  # Les coordonnées du rectangle (récupérée depuis les arguments)
        self.rect.left=x
        # Pour gérer l'animation de l'explosion
        self.animation_frames = 4           # toutes les 6 rafraichissements d'écran (ou bien tours de la boucle "continuer"), on change l'image de l'explosion
        self.current_frame = 0              # le refraichissement courant (qui va être modifié)

    def update(self):
        # méthode qui sera appelée chaque fois qu'on mettra à jour les sprites de l'écran
        global images_explosions
        if self.index < 8:                   # boucle qui a lieu tant que l'index n'a pas atteint la dernière image d'explosion
            # ces instructions permettent d'avoir une "pause" de 6 (animation_frames) frames entre deux images de l'explosion
            self.current_frame += 1         # on ugmente de 1 la frame encours
            if self.current_frame >= self.animation_frames:             # si elle dépasse les 6 frames
                self.current_frame = 0                                  # elle revient à 0
                self.index = (self.index + 1) % len(images_explosions)     # on change l'index de l'image de l'explosion utilisée
                self.image = images_explosions[self.index]                 # et on change l'image de l'explosion
        else:                                   # si on a dépassé la dernière image de l'explosion
            self.kill()                         # on détruit l'explosion pour qu'il ne s'affiche plus

# ########################################################
# initialisation des variables
# #########################################################
continuer=1                     # si = 0 le jeu d'arrete
score=0                         # valeur du score au début
vitesse_scrolling=5             # la vitesse du scrolling
compteur_affichage_element_decor=0      # compteur nécessaire pour afficher les élements de décor au bout d'un certain nombre de frames
compteur_affiche_ennemi=0               # compteur nécessaire pour afficher les ennemis au bout d'un certain nombre de frames
compteur_affiche_bonus=0
Difficulte= 3                           # difficulté du niveau: au moment du scrolling, il y a 1 chance sur 5 pour qu'un ennemi apparaisse.
                                        # descendre cette valeur en fonction du nombre de point (jusqu'au maxi: 1)
pygame.time.Clock().tick(30)
Temps = time.time()
couleur_chrono = RED

"""
def c(jx, jy, x,y, matrice, direction):
    if 0 <= x < n and 0 <= y < n:
        if cache[y][x] != " ":
            return cache[y][x]

        if x == jx and y == jy:
            total = matrice[jy][jx]
        else:
            if x > jx:
                tt1 = c(x-1,y)
            else:
                tt1 = 0
            if y > jy:
                tt2 = c(x,y-1)
            else:
                tt2 = 0
            total = max(tt1,tt2) + matrice[y][x]
        cache[y][x] = total
        return total

def pathfind():
    cache = [ [" " for i in range(8)] for i in range(6) ]    
    c(x-1,y-1)
    a = cache
    y,x = jy, jx
    for i in range(14):
        if x < 9:
            droite = a[y][x+1]
        else:
            droite = 0
        if y < 9:
            bas = a[y+1][x]
        else:
            bas = 0

        if droite > bas:
            a[y][x+1] = -1
            x += 1
        else:
            a[y+1][x] = -1
            y += 1
 """   

def matrice():
    matrice_map = [ [ 60, 100, 100, 100, 100, 100, 100, 60] for i in range(6) ]
    en=Groupe_Sprites_Ennemis
    for i in en:
        y = (i.rect.top) // 100
        if y < 0:
            y = 0
        if y > 5:
            y = 5

        x = (i.rect.right-100) // 33
        matrice_map[y][x] -= 10
        
        if x > 0:
            matrice_map[y][x-1] -= 5
        if x < 7:
            matrice_map[y][x+1] -= 5
        if y > 0 :
            matrice_map[y-1][x] -= 5
        if y < 5:
            matrice_map[y+1][x] -= 5

    note = 0
    for i in range(6):
        for a in range(8):
            if matrice_map[i][a] >= note:
                note = matrice_map[i][a]
                x,y = a,i
    if  Joueur.rect.left < 100:
        jx = 0
    if Joeur.rect.left > 300:
        jx = 7
    jy = Joueur.rect.top//100,
    jx = Joueur.rect.left-100//33
    if jx < x: #Joueur a gauche
        if jy > y : #Joueur en bas
            c(jx,jy,x,y,matrice_map, "DH")
        else:
            c(jx,jy,x,y,matrice_map, "DB")
    else:
        if jy > y:
            c(jx,jy,x,y,matrice_map, "GH")
        else:
            c(jx,jy,x,y,matrice_map, "GB")
    
    coord_possibles = [100,133,166,200,233,266]

    
# #########################################################
# On encadre toujours les programmes pygame par try et finally ce qui permet de fermer correctement la fenetre pygame en cas d'erreur
# ########################################################
try:
    # #####################################
    # création de la fenêtre de jeu
    # #####################################
    Fenetre_Jeu=pygame.display.set_mode((400,600))      #creation d'une fenetre
    pygame.display.set_caption('Mad Max')     # Nom affiché sur la fenêtre

    # ##################################################################"
    # OBJETS du jeu
    # ###########################################################################"

    # création d'un groupe de sprite contenant tous les SPRITE(=objets) du jeu
    Tous_les_sprites = pygame.sprite.Group()

    # --------- le Fond ---------

    Cache_misere = pygame.image.load("images\cache_misere.PNG")
    Decor =pygame.image.load("images\Fond.PNG").convert_alpha()
    Decor2 =pygame.image.load("images\Fond2.PNG").convert_alpha()
    Rectangle_Decor1=Decor.get_rect()                           # on créé un rectangle pour le 1er décor
    Rectangle_Decor2=Decor2.get_rect()                           # on créé un rectangle pour le 2nd décor
    Rectangle_Decor1.top=0                                      # le 1er décor démarre à y=0
    Rectangle_Decor2.top=-600                                   # le 2nd décor démarre à y=-600

    #----------Les Ajouts ----------
    RectScore =pygame.image.load("images\RectScore.PNG").convert_alpha()
    degrade = pygame.image.load("images\Degrade.PNG")
    danger= 0
    """ le fond a comme dimension 400x600
    La route commence à l'abscisse 100 et fait 200 px de large (donc finit à 300) """

    # --------- le joueur ---------
    Groupe_Sprites_Joueur= pygame.sprite.Group()    # création d'un groupe de sprite joueur (conseillé pour l'affichage)
    Joueur=Player(180,450)          # on créé un objet "joueur" à la position x=180 y=450
    Tous_les_sprites.add(Joueur)    # on met l'objet joueur dans le groupe de tous les sprites
    Groupe_Sprites_Joueur.add(Joueur) # on met l'objet joueur dans le groupe de sprites joueur

    # --------- Les voitures ennemi ---------
    Groupe_Sprites_Ennemis= pygame.sprite.Group()   # on créé un groupe de sprites contenant tous les ennemis
    Liste_Ennemis=["Voiture1","Voiture2","Voiture4"]        # liste des noms de fichiers des images des ennemis
    """ rajouter éventuellement dans cette liste des ennemis: préciser le nom du fichier
    les images des voitures font 30 pixels de large, des camions 33 pixels (et au maxi 80 px de haut """
    Liste_images_Ennemis=[]                                         # on va mettre toutes les images dans une liste
    for enmi in Liste_Ennemis:
        Liste_images_Ennemis.append(pygame.image.load("images\\"+enmi+".png").convert_alpha())

    # ---------  les explosions ---------
    Groupe_Sprites_Explosion=pygame.sprite.Group()
    images_explosions =[]              # liste dans laquelle seront stockées les 4 images de l'explosion
    for i in range(9):                      # on va charger les 4 images et les ajouter à la liste
        images_explosions.append(pygame.image.load("images\Explosion"+str(i)+".png").convert_alpha())

    # ---------  Les éléments de décor ---------
    Groupe_Sprites_Decor= pygame.sprite.Group()          # on créé un groupe de sprites contenant tous les elts de décor
    Liste_Decor=["Tile"+str(i) for i in range(1,9)]        # liste des fichiers des images des décors
    """ rajouter éventuellement dans cette liste des élements de décor: préciser le nom du fichier
    Les éléments de décor sont des blocs de 100x100 avec éventuellement un fond transparent"""
    Liste_images_Decor=[]                                         # on va mettre toutes les images dans une liste
    for d in Liste_Decor:
        Liste_images_Decor.append(pygame.image.load("images\\"+d+".png").convert_alpha())

    # ---------  ...........  ---------
    """ si l'on a besoin d'un groupe de sprite "bonus" ou "points", le créer ici """
    Groupe_Sprites_Bonus = pygame.sprite.Group()
    Liste_Bonus=["Bonus1", "Bonus2", "Bonus3"]
    Liste_image_Bonus=[]
    for bonus in Liste_Bonus:
        Liste_image_Bonus.append(pygame.image.load("images\\"+bonus+".PNG").convert_alpha())

    # ##########################################################
    # SONS du jeu
    # #########################################################
    Crash = pygame.mixer.Sound("sounds\Crash.ogg")              # son lors des impacts
    """ si sons bonus ou autres sons (perdus, santé faibles etc...) , les définir ici """
    pygame.mixer.music.load("sounds\moteur.ogg")                # son joué "comme musique de fond": le bruit du moteur

    # #################################################
    # Initialisations diverses
    # #########################################################
    pygame.key.set_repeat(10,30)            # on active la repetition des touches - Ne pas modifier ces valeurs
    start = time.time ()                    # On demarre le chronometre: définition de la date temps 0
    Horloge = pygame.time.Clock()           # pour fixer plus tard le nombre d'image par seconde affichées

    # ##################################################################
    # boucle principale qui attend les evenement du clavier, de la souris etc...
    # ##################################################################
    while continuer:                        # tant que "continuer" vaut 1

        Horloge.tick(60)                    # on fixe à 60 images/s

        pygame.mixer.music.play(-1)         # on lance la musique de fond (le bruit du moteur)

        # #################################################
        # -------- Attente des évènements ----------------
        for event in pygame.event.get():    #pygame prend le premier evenement de la file

            if event.type==QUIT:            #l'evenement QUIT correspond au clic sur la croix
                continuer=0                 #permet de quitter la boucle et donc le jeu

            """if event.type == KEYDOWN:            # si l'evenemement est l'appui sur une touche
            mettre ici les évènements et ce qu'ils déclenchent"""

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:          # si c'est la touche LEFT
                Joueur.move(-10,0)             # on déplace le joueur de -10 pixels
            if keys[K_RIGHT]:
                Joueur.move(10,0)
            if keys[K_UP]:          # si c'est la touche LEFT
                Joueur.move(0,-10)             # on déplace le joueur de -10 pixels
            if keys[K_DOWN]:
                Joueur.move(0,10)
            if keys[K_ESCAPE]:
                pygame.quit()
                break

            """ si l'on veut que la voiture soit contrôlée par la souris, mettre ici le code suivant:
            if event.type == MOUSEMOTION:       #Si l'évènement est le mouvement de souris
		          Joueur.move(event.rel[0],0)   #On déplace le joueur du nombre de pixels parcouru par la souris suivant X : rel[0]   """

        # #################################################
        # ------------- Gestion des collisions -----------
        # Collision Joueur/Ennemis:
        Liste_Collisions=pygame.sprite.spritecollide(Joueur, Groupe_Sprites_Ennemis, 1)     # on regarde les collisions entre le joueur et les groupe sprite Ennemi
        for Ennemi_touche in Liste_Collisions:                  # pour chaque les ennemis touché
            Explosion_ennemi=Explosion(Ennemi_touche.rect.left,Ennemi_touche.rect.top)      # on créé un sprite explosion à la position de l'ennemi
            Tous_les_sprites.add(Explosion_ennemi)                                          # on ajoute cette explosion au groupe de tous les sprites
            Groupe_Sprites_Explosion.add(Explosion_ennemi)                                  #  on ajoute cette explosion au groupe de sprites explosion
            Crash.play()                                            # on joue le son de l'impact
            Joueur.Health -= 10

        """ mettre ici une éventuelle collision du joueur avec des bonus ou unes vies ou autre.
        Ces bonus pourront être mis dans un groupe de sprites: "Groupe_Sprites_Bonus"
        Les collisions seront gérées comme celle avec les ennemis avec les explosions en moins... """
        Liste_collisions_bonus = pygame.sprite.spritecollide(Joueur, Groupe_Sprites_Bonus, 1)
        for Bonus_touche in Liste_collisions_bonus:

            Joueur.Health += 10

        # #################################################
        # Gestion du score, de l'état de santé etc...
        """ mettre ici l'évolution du score en fonction de vos critères
        mettre ici aussi la gestion de la santé = 0: vie en moins, fin du jeu etc...

        POUR ARRETER LE JEU si on a perdu, il faut mettre: continuer =0
        et la boucle infinie s'arrêtera..."""
        if Joueur.Health < 1:
            continuer = 0

        # #################################################
        # ---------- Création des éléments de décor ------
        compteur_affichage_element_decor+=1                             # compteur qui augmente de 1 à chaque frame
        if compteur_affichage_element_decor > (100/vitesse_scrolling):  # dès que 100 pixels ont défillé (c'est à dire la hauteur d'un bloc)
            compteur_affichage_element_decor=0                          # on remet le compteur à 0
            Nouveau_Decor=Element_Decor("G")                             # on créé un décor à gauche (pris au hasard dans les blocs)
            Tous_les_sprites.add(Nouveau_Decor)                         # on l'ajoute au groupe de SPRITE TOTAL
            Groupe_Sprites_Decor.add(Nouveau_Decor)
            Nouveau_Decor=Element_Decor("D")                            # on créé un décor à droite (pris au hasard dans les blocs)
            Tous_les_sprites.add(Nouveau_Decor)                     # on l'ajoute au groupe de SPRITE TOTAL
            Groupe_Sprites_Decor.add(Nouveau_Decor)

        # #################################################
        # --------- Création des ennemis de manière aléatoire en fonction de la difficulté
        compteur_affiche_ennemi+=1            # ce compteur permet d'attendre qu'un camion (hauteur 80) se soit entièrement déplacé avant de créer un autre ennemi
        if compteur_affiche_ennemi > (80/vitesse_scrolling):  # dès que 80 pixels ont défillé (c'est à dire la hauteur d'un camion, qui est la max des véhicules)
                                                                # on est prêt à créer aléatoirement un ennemi
            hasard=random.randrange(1,Difficulte)               # on tire un nombre entr 1 et "difficulté" (5 au début). Plus "difficulté" faible, plus c'est dur
            if hasard==1:                                       # si ce ombre au hasard vaut 1
                compteur_affiche_ennemi=0                          # on remet le compteur à 0 (car si c'est un camion, il faut attendre qu'il défile entièrement)
                Nouvel_Ennemi=Ennemy()                                  # on créé un objet ennemi
                Tous_les_sprites.add(Nouvel_Ennemi)                     # on l'ajoute au groupe de SPRITE TOTAL
                Groupe_Sprites_Ennemis.add(Nouvel_Ennemi)               # et au groupe total

        compteur_affiche_bonus += 1
        if compteur_affiche_bonus > (80/vitesse_scrolling):
            hasard=random.randrange(1,Difficulte*100)
            if hasard == 1:
                compteur_affiche_bonus=0
                Nouveau_Bonus = Element_Bonus()
                Tous_les_sprites.add(Nouveau_Bonus)
                Groupe_Sprites_Bonus.add(Nouveau_Bonus)

                

        matrice()
       # #################################################
        # --------- Création d'autres objets (bonus...)
        """ mettre ici la création programmée ou aléatoire d'autres objets (bonus,etc...) """

        # #################################################
        # ------------- Gestion du scrolling --------------
        """ ici se gère le scrolling du fond. La base du code se fait avec 2 décors.
        On peut imaginer aussi dessiner des objets au hasard sur les décors qui "scrolleront"
        avec les décors... """
        Rectangle_Decor1=Rectangle_Decor1.move(0,vitesse_scrolling)
        Rectangle_Decor2=Rectangle_Decor2.move(0,vitesse_scrolling)
        if Rectangle_Decor1.top>=600:
            Rectangle_Decor1.top=-600
        if Rectangle_Decor2.top>=600:
            Rectangle_Decor2.top=-600

        # #################################################
        # ------------ mise à jour des sprites ------------
        Tous_les_sprites.update()     # on met à jour les groupes de sprite

        # #################################################
        # -------- Affichage des images et sprites -------
        Fenetre_Jeu.blit(Cache_misere,(0,0))
        Groupe_Sprites_Decor.draw(Fenetre_Jeu)                      # on affiche tous les sprites (joueur, ennemis, bonus etc...)
        Fenetre_Jeu.blit(Decor, Rectangle_Decor1)                 # on affiche les 2 fonds
        Fenetre_Jeu.blit(Decor2, Rectangle_Decor2)

                                                                    # on pourrait tous les afficher d'un coup avec
        Groupe_Sprites_Bonus.draw(Fenetre_Jeu)
        Groupe_Sprites_Ennemis.draw(Fenetre_Jeu)                    #Tous_les_sprites.draw mais l'ordre d'affichage serait aléatoire
        Groupe_Sprites_Joueur.draw(Fenetre_Jeu)                     # Là, on affiche d'abord le décor, puis au dessus les bonus,
        Groupe_Sprites_Explosion.draw(Fenetre_Jeu)                  # puis au dessus Joueur et explosions...
        if danger:
            Fenetre_Jeu.blit(degrade,(-100,-150))
            time.sleep(0.01)

        # #################################################
        # ------------ Affichage des textes --------------
        """ Afficher ici éventuellement des textes pour la santé du joueur, le score,
        le nombre de vie ou autre...

        Pour afficher un rectangle, mettre AVANT l'affichage du texte:
        pygame.draw.rect(Fenetre_Jeu, couleur choisie, Rect(gauche, haut, largeur, hauteur))
        exple: pygame.draw.rect(Fenetre_Jeu,RED,Rect(0, 10, 100, 100))
        """
        #pygame.draw.rect(Fenetre_Jeu,BLACK,Rect(0, 10, 100, 100))
        """
        SYNTHAXE de la fonction "Affiche_Texte:"
        Affiche_Texte(Surface sur laquelle afficher,texte à afficher, taille, x, y, couleur)
        Les couleurs disponibles sont les constantes définies au début du programme en codage RVB
        exemple:
        Affiche_Texte(Fenetre_Jeu,str(Joueur.Health), 40, 350, 20, WHITE) """
        Fenetre_Jeu.blit(RectScore,(300,0))
        Affiche_Texte(Fenetre_Jeu,"Health", 25, 350, 10, YELLOW)
        Affiche_Texte(Fenetre_Jeu,str(Joueur.Health), 40, 350, 50, WHITE)       # on affiche la santé du joueur

        Fenetre_Jeu.blit(RectScore,(0,0))
        Affiche_Texte(Fenetre_Jeu,"Chrono", 25, 50, 10, YELLOW)
        Affiche_Texte(Fenetre_Jeu, str(Temps), 40, 50, 50 , couleur_chrono)

        Affiche_Texte(Fenetre_Jeu,"AZEEEEE", 12, 32, 550, BLACK)
        Affiche_Texte(Fenetre_Jeu,"AZEAZEA", 12, 25, 560, BLACK)
        Affiche_Texte(Fenetre_Jeu,"MZE", 12, 15, 570, BLACK)
        Affiche_Texte(Fenetre_Jeu,"AZEAZEAZEA", 12, 32, 580, BLACK)
        # #################################################
        #  ------------ Gestion du chronometre ------------
        """ mettre ici une éventuelle gestion de choronomètre:
        Le temps écoulé depuis le début de la boucle est: Temps=time.time()-start
        On peut le soustraire à une variable "temps autorisé" que l'on aura défini avant pour
        afficher un temps restant...        """
        Temps = int(time.time()-start)
        if Temps < 10 :
            couleur_chrono = RED
        elif Temps < 30 :
            couleur_chrono = YELLOW
        else:
            couleur_chrono = GREEN

        # #################################################
        # et pour finir...
        pygame.display.flip()                                                   # on rafraichit l'ecran
        vitesse_scrolling = Temps/10 + 5
# ######################################
# si erreur rencontree, on ecrit le type d'erreur dans la console
except:
    traceback.print_exc()
# ########################################
# Et pour finir, toujours s'il y a eu une erreur, on quitte
finally:
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()
    sys.exit()
