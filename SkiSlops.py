
## Importation des librairies
import json
import math
import networkx as nx
import heapq

## Fonctions annexe
def heures_en_minutes(heures):
    minutes = math.ceil(heures * 60) 
    return minutes
    #ceil retourne le plus petit entier supérieur 
    # ou égal à la valeur donnée en argument. 

## Le skieur entre son niveau 
niveaux = ["débutant","expérimenté"]
type_skieur = input("Quel type de skieur êtes-vous? ")
while type_skieur not in niveaux:
    print("ERREUR: êtes vous débutant ou expérimenté? ")
    type_skieur = input("Quel type de skieur êtes-vous? ")

## Récupération du fichier contenant la data en fonction du niveau du skieur
if type_skieur == "débutant":
    with open('debutant.json') as fic:
        data = json.load(fic)
elif type_skieur == "expérimenté":
    with open('experimente.json') as fic:
        data = json.load(fic)

## Le skieur chosit son sommet de départ et son sommet d'arrivée
depart = input("entrer le sommet de départ ")
arrivee = input("entrer le sommet d'arrivée ")

## Création du graphe
graphe = nx.Graph()
for node, edges in data.items():
    graphe.add_node(node)
    for neighbor, properties in edges.items():
        for piste in properties:
            nom_piste = piste["Piste"]
            duree_piste = heures_en_minutes(piste["duree"])
            graphe.add_edge(node, neighbor, nom = nom_piste,duree = duree_piste)

## Fonction qui calcul le plus court chemin
def dijkstra(graphe, depart, arrivee):
    # Initialisation de la distance de tous les sommets à l'infini
    distances = {sommet: float('infinity') for sommet in graphe}
    # La distance de départ à elle-même est de 0
    distances[depart] = 0
    # Initialisation de la file de priorité
    pq = [(0, depart)]
    # Initialisation du dictionnaire des pistes empruntées pour atteindre chaque sommet
    chemin = {depart: []}
    while len(pq) > 0:
        # On récupère le sommet avec la plus petite distance
        (dist, sommet_courant) = heapq.heappop(pq)
        # Si on a atteint le sommet de destination, on retourne la distance et le chemin
        if sommet_courant == arrivee:
            return (distances[sommet_courant], chemin[sommet_courant])
        # Sinon, on explore les sommets adjacents
        for voisin, piste in graphe[sommet_courant].items():
            temps = piste['duree']
            distance = distances[sommet_courant] + temps
            # Si on a trouvé un chemin plus court, on met à jour la distance et le chemin
            if distance < distances[voisin]:
                distances[voisin] = distance
                chemin[voisin] = chemin[sommet_courant] + [(piste['nom'], piste['duree'])]
                heapq.heappush(pq, (distance, voisin))
    # Si on n'a pas trouvé de chemin, on retourne None
    return None

## Fonction qui affiche le chemin
def affichage_chemin(path, depart, arrivee):
    []
    print("Vous vous trouvez à", depart)
    for piste in path[1]:
        if "Piste" in piste[0]:
            print("Descendre la", piste[0], "pendant environ", piste[1],"min")
        elif "Télécabine" in piste[0]:
            print("Prenez la", piste[0], "pendant environ", piste[1],"min")
        else:
            print("Prenez le", piste[0], "pendant environ", piste[1],"min")
    print("Vous arrivez à ", arrivee) 
    print(f'Le trajet devrait vous prendre environ {path[0]} min')


## Lancement du programme
way = dijkstra(graphe, depart, arrivee)
affichage_chemin(way, depart,arrivee)