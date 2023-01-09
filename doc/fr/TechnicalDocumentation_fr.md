# Auto Pong
## Documentation Technique
---
### Description :
Ce projet est une démonstration d'un algorithme d'apprentissage par renforcement.

Le programme joue tout seul et s'améliore

---
### Algorithme d'apprentissage

#### Renforcement
Pendant la partie, à chaque intervalle de temps, un 'état' du jeu est enregistré (position et direction de la balle, position de la raquette), puis quand la balle est alignée horizontalement avec la raquette, soit la balle frappe la raquette soit elle passée à côte.

Si la balle frappe la raquette les 'états' précédents reçoivent un renforcement positif, sinon ils reçoivent un renforcement négatif, plus l'image est proche du moment ou la balle et la raquette sont alignées plus ce renforcement est fort.

#### Prise de décision
Lorsque le programme doit prendre une décision, on simule 3 états futurs du programme: déplacement vers le haut, déplacement vers le bas, et ne pas bouger, et on prend dans la liste des états passés l'état le plus proche pour ces trois cas, puis on choisit l'état futur qui a le plus gros renforcement.

