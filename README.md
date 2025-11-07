Ce travail correspond à un projet de Cryptographie du M1 MIC de l'université Paris Cité.

# Codes-Polaires
Ce projet contient un document pdf ainsi que 2 programmes python:

- `Codes_Polaires-1.pdf` : Introduction aux codes polaires, on y trouve des définitions, théorèmes, schémas et exemples conçernant les codes polaires.
- `polarize.py` : simule l'encodage et le décodage d’un message sur un canal BEC.
- `visualize.py` : permet de visualiser la polarisation des canaux en fonction de leur fiabilité.

---

**Auteurs :** Dos Santos Jonas et Nathan Fauvelle-Aymar.

## 1. `polarize.py`

### Description

Ce script permet de simuler un codage canal à l'aide de **codes polaires** sur un **canal à effacement binaire (BEC)**.

### Paramètres

- `N` : nombre total de canaux utilisés (**puissance de 2**).
- `K` : nombre de bits utiles à transmettre.
- `epsilon` : taux d'effacement du canal BEC (valeur entre 0 et 1).

### Commande

python3 polarize.py N K epsilon

Cette commande affiche dans le terminal :
- les étapes intermédiaires de l'encodage et du décodage,
- un booléen de réussite du décodage,
- le nombre de bits ayant pu causer des erreurs,
- la fiabilité du pire canal utilisé selon les paramètres `N` et `K`.

### Exemples recommandés

python3 polarize.py 8 3 0.5  
python3 polarize.py 32 11 0.5  
python3 polarize.py 256 90 0.5  
python3 polarize.py 4096 1750 0.5

> Pour des grandes valeurs de `N`, vous pouvez choisir `K` approchant  `N × (1 - epsilon)` pour observer l’évolution de la fiabilité et du taux d’erreur.

---

## 2. `visualize.py`

### Description

Ce script permet de **visualiser la polarisation** de `N` canaux en fonction d’un taux d’effacement `epsilon`.

- Une fiabilité proche de **0** indique un canal **très performant**.
- Une fiabilité proche de **1** indique un canal **très défaillant**.

### Paramètres

- `N` : nombre de canaux (puissance de 2).
- `epsilon` : taux d’effacement.
- `-s` : (optionnel) trie les canaux par fiabilité croissante avant l'affichage.

### Commandes

# Sans tri  
python3 visualize.py 8 0.5  
python3 visualize.py 32 0.5  
python3 visualize.py 256 0.5  
python3 visualize.py 4096 0.5

# Avec tri  
python3 visualize.py 8 0.5 -s  
python3 visualize.py 32 0.5 -s  
python3 visualize.py 256 0.5 -s  
python3 visualize.py 4096 0.5 -s

---

## Remarques

- `N` doit être une **puissance de 2**.
- `epsilon` est un taux d’effacement typiquement compris entre 0.1 et 0.9.
- Pour des analyses avancées, n'hésitez pas à tester différentes combinaisons de `N`, `K` et `epsilon`.

---

## 3. Sources pour les programmes

Voici les différentes sources consultées et utilisées dans le cadre des recherches sur l'encodage et le décodage.
Certaines de ces sources ont pu servir à la compréhension d'algorithmes qui seront mentionnés lors de la soutenance, et dont nous ne proposons pas forcément d'implémentation (CA-SCL et Fast SSC Decoding)

- Emre Telatar | ISIT 2017 | The Flesh of Polar Codes | 2017-06-29
> https://www.youtube.com/watch?v=VhyoZSB9g0w&list=LL&index=6&t=3164s&ab_channel=ISIT2017

- E. Arikan, “Channel polarization: A method for constructing capacity-achieving codes for symmetric binary-input memoryless channels,” IEEE Trans. on Inf. Theory, vol. 55, no. 7, pp.3051–3073, 2009.

- Alexios Balatsoukas-Stimming's full lecture at the 2020 European School of Information Theory Stuttgart, Germany
> https://www.itsoc.org/video/efficient-decoding-polar-codes-algorithms-and-implementations

- Malek ELLOUZE, Camille LEROUX, Romain TAJAN, Charly POULLIAT, Christophe JEGO | 2022 | "Décodage SC par listes optimisées de codes polaires" | Université de Bordeaux, Bordeaux INP, Laboratoire IMS, UMR CNRS 5218, France et Université de Toulouse, INPT-ENSEEIHT, Laboratoire IRIT , UMR CNRS 5505, France

