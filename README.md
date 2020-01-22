# pyDES

Implémentation python du chiffrement et déchiffrement DES.

Lancer avec `python3 des.py`.

**Aides**

[Constantes du DES sur Wikipedia](https://fr.wikipedia.org/wiki/Constantes_du_DES)

[Algo chiffrement DES](https://www.commentcamarche.net/contents/204-introduction-au-chiffrement-avec-des)

[Truc sur yield parce qu'on adore](https://www.geeksforgeeks.org/use-yield-keyword-instead-return-keyword-python/)

[Percipio : vidéo sur l'algo DES](https://reseau-ges.percipio.com/courses/8e8d3e93-0d9c-11e7-b6c3-0242c0a80802/videos/8e8d3ea2-0d9c-11e7-b6c3-0242c0a80802)

[Percipio : bouquin chouette, algo XOR et autres trucs](https://reseau-ges.percipio.com/books/4bc44c80-f383-11e6-ad5d-0242c0a80607)


**Workflow git**

1 - Toujours commencer par pull master, avec un repo propre (= pas de modifs en cours)

`git checkout master`

`git pull`

2.a - Se placer sur une nouvelle branche

`git co -b nom_de_ma_nouvelle_branche`
 
2.b **ou bien** se placer sur une branche déjà existante

`git co nom_de_ma_branche`

et se mettre à jour avec master 

`git rebase master`

3 . Dev des trucs 🤓

4 . Vérifier les fichiers qui ont changé

`git status`

`git diff`

5 . Les préparer à être envoyés
 
`git add .`

*`.` signifie "tous les fichiers modifiés" mais il est possible de spécifier uniquement certains noms de fichiers*

En général je refais un `git status` ici pour vérifier qu'ils sont bien tout verts. 

6 . Commiter les fichiers

`git commit -m "Description rapide de ce que j'ai fait"`

*`-m` signifie "message"*

7 . Pousser les fichiers commités sur la branche distante

`git push`

8 . Aller sur le repo github. Normalement il y a un bandeau jaune avec un bouton vert "Create pull request"

9 . Descript° feature & valider

10 . Attendre retours & approvals **avant** de merger 
