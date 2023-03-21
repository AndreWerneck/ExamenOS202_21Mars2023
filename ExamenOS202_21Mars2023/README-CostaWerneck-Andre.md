INTRODUCTION 

![image](https://user-images.githubusercontent.com/40474628/226589205-298b30c2-8bd1-4ab0-b3f2-a9f1c7401fd0.png)

![image](https://user-images.githubusercontent.com/40474628/226589356-011704aa-307e-4ca0-810e-6137f7a19d48.png)

D'après les images, on peut voire que le nombre de coeurs physiques de mon ordinateur est de 2 unités et le nombre de coeurs logiques est de 4 unités.

La quantité de mémoire cache de ma machine est de 128 KB pour les caches L1 ensembles, 512 KB pour le cache L2 et 3 MB pour le cache L3.

QUESTION 1

Pour la première question, 2 stratégies de parallélisation étaient étudiés: une statique, en donnent une quantité presque égal de tâches pour chaque processus et une dynamique, en faisant un algoritme maître-sclave pour chaque ligne à chaque tâche.

Pour la paralélisation statique, on a parallélisé le premier boucle et pour la parallélisation dynamique, on a parallélisé le deuxième boucle. Vous pouvez regarder dans le code source comme cela a été fait. Comme je croyait déjà, la parallélisation statique a donnée un speed-up positif. En revanche, la parallélisation dynamique de la façon faite, nous a donnée un speed-up negatif. La courbe pour la parallélisation statique est le suivante. Comme le speed-up était négatif pour la dynamique, on va pas montrer la courbe.

![image](https://user-images.githubusercontent.com/40474628/226589015-6ce0c78e-abc9-465d-93f2-13c6d794584d.png)

On peut remarquer qu'on a obtenu un speed-up avec le parallélisation statique.

Statique						
nbp	1	2	3	4	8	16


temps calcul	1,4565	0,851063	0,740989	0,875835	0,869799	0,947672


temps affichage	15,9	8,628	7,6929	8,5447	7,8361	7,6704


SpeedUp calcul	1	1,711389169	1,965616224	1,662984466	1,674524804	1,536924168


SpeedUp affichage	1	1,842762521	2,066830107	1,860802603	2,029060226	2,072917142

lignes de commande:

mpiexec -n 4 --oversubscribe python3 -m mpi4py automate_parallel_statique.py


mpiexec -n 4 --oversubscribe python3 -m mpi4py automate_parallel_maitre_sclave.py 

QUESTION 2

Pour la premiere partie de cetet question. L'idée était de faire une parallélisation statique du programme. Pour la deuxieme partie de l'algo, l'idée était échanger les données modulo 2 (si modulo = 0 -> processus suivante, sinon processus contraire) et après faire un recv et un send à chaque 2 processus, pour tout rejoindre et aussi pour tout envoyer à l'autre processus. Et, à la fin, il fallait refaire l'algo pour les données mélangées.

lignes de commande:


mpiexec -n 4 --oversubscribe python3 -m mpi4py enveloppe_parallel.py 


