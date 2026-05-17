import pygame
from random import randint

pygame.init()
# "initialise toutes les variables générales de pygame"

Largeur = 500
Hauteur = 500
fenetre = pygame.display.set_mode((Largeur, Hauteur))
# création de l'environnement graphique
pygame.display.set_caption("SPACE INVADERS")  # titre fenetre

imageVaisseau = pygame.image.load("Vaisseau.png")
imageVaisseau = pygame.transform.scale(imageVaisseau, (64, 64))
imageAlienVert = pygame.image.load("AlienVert.png")
imageAlienJaune = pygame.image.load("AlienJaune.png")
imageAlienRouge = pygame.image.load("AlienRouge.png")

positionVaisseau = (Largeur // 2, Hauteur - 64)

NBvaisseaux = 10
FLOTTEVert = []
for i in range(NBvaisseaux):
    FLOTTEVert.append((i * 40 + 8, 10))
FLOTTEJaune = [(i * 40 + 8, 40) for i in range(NBvaisseaux)]
FLOTTERouge = []
for i in range(NBvaisseaux, 0, -1):
    FLOTTERouge.append((-i * 25, 200))

MesTirs = []
TirsEnnemis = []


def dessiner():
    fenetre.fill((50, 50, 50))

    # pygame.draw.rect(fenetre,(255,0,0),rect1,1)

    fenetre.blit(imageVaisseau, positionVaisseau)

    for i in range(len(FLOTTEVert)):
        fenetre.blit(imageAlienVert, FLOTTEVert[i])
    for i in range(len(FLOTTEJaune)):
        fenetre.blit(imageAlienJaune, FLOTTEJaune[i])
    for i in range(len(FLOTTERouge)):
        fenetre.blit(imageAlienRouge, FLOTTERouge[i])

    for i in range(len(MesTirs)):
        pygame.draw.circle(fenetre, (0, 255, 0), MesTirs[i], 5)

    for i in range(len(TirsEnnemis)):
        pygame.draw.circle(fenetre, (255, 255, 0), TirsEnnemis[i], 3)

    pygame.display.flip()
    # Rafrachit l'écran
    return True


def gererClavierSouris():
    global Continuer, positionVaisseau, positionProjectile

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Continuer = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            MesTirs.append((positionVaisseau[0] + 32, positionVaisseau[1]))

    touchesPressees = pygame.key.get_pressed()
    # Je mets toutes les touches clavier dans un dico
    if touchesPressees[pygame.K_RIGHT] == True:
        positionVaisseau = (positionVaisseau[0] + 1, positionVaisseau[1])
    if touchesPressees[pygame.K_LEFT]:
        positionVaisseau = (positionVaisseau[0] - 1, positionVaisseau[1])
    if positionVaisseau[0] > Largeur:
        positionVaisseau = (-64, Hauteur - 64)
    if positionVaisseau[0] < -64:
        positionVaisseau = (Largeur, Hauteur - 64)

    return True


# PROGRAMME PRINCIPAL
clock = pygame.time.Clock()
# Création d'une horloge

Continuer = True
while Continuer:
    clock.tick(200)
    # Vitesse boucle: en une seconde j'ai 50 rafraichissement dessiner

    dessiner()
    gererClavierSouris()

    # CREATION et GESTION DES TIRS ENNEMIS
    for i in range(len(FLOTTEVert)):
        if (randint(0, 2000) == 0):
            TirsEnnemis.append((FLOTTEVert[i][0] + 17, FLOTTEVert[i][1] + 22))
    for i in range(len(TirsEnnemis)):
        if TirsEnnemis[i][1] > 600:
            TirsEnnemis.pop(i)
            break
        else:
            TirsEnnemis[i] = (TirsEnnemis[i][0], TirsEnnemis[i][1] + 1)

    # MOUVEMENTS DES SPRITES
    for i in range(len(MesTirs)):
        MesTirs[i] = (MesTirs[i][0], MesTirs[i][1] - 3)
    for i in range(len(FLOTTEJaune)):
        FLOTTEJaune[i] = (FLOTTEJaune[i][0], FLOTTEJaune[i][1] + 0.01)

    for i in range(len(FLOTTERouge)):
        if FLOTTERouge[i][0] > 600:
            FLOTTERouge[i] = (-30, 200)
        else:
            FLOTTERouge[i] = (FLOTTERouge[i][0] + 0.5, -0.003 * FLOTTERouge[i][0] ** 2 + 2 * FLOTTERouge[i][0] + 100)

    # LES COLLISIONS
    for Alien in FLOTTEVert:
        rect1 = pygame.Rect(Alien, (32, 28))
        for Tir in MesTirs:
            if rect1.collidepoint(Tir):
                FLOTTEVert.remove(Alien)
                MesTirs.remove(Tir)

    for Alien in FLOTTEJaune:
        rect1 = pygame.Rect(Alien, (32, 28))
        for Tir in MesTirs:
            if rect1.collidepoint(Tir):
                FLOTTEJaune.remove(Alien)
                MesTirs.remove(Tir)

    for Alien in FLOTTERouge:
        rect1 = pygame.Rect(Alien, (32, 28))
        for Tir in MesTirs:
            if rect1.collidepoint(Tir):
                FLOTTERouge.remove(Alien)
                MesTirs.remove(Tir)

pygame.quit()