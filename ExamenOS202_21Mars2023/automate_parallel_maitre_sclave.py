import numpy as np
import time
import matplotlib.pyplot as plt
import sys
from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp = globCom.size
rank = globCom.rank


print(f'processus {rank} a commencé')

#tags
TERMINATE = 'T'

status = MPI.Status()

nombre_cas   : int = 256
nb_cellules  : int = 360  # Cellules fantomes
nb_iterations: int = 360

compute_time = 0.
display_time = 0.

def save_as_md(cells, symbols='⬜⬛'):
    res = np.empty(shape=cells.shape, dtype='<U')
    res[cells==0] = symbols[0]
    res[cells==1] = symbols[1]
    np.savetxt(f'resultat_{num_config:03d}.md', res, fmt='%s', delimiter='', header=f'Config #{num_config}', encoding='utf-8')

def save_as_png(cells):
    fig = plt.figure(figsize=(nb_iterations/10., nb_cellules/10.))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(cells[:, 1:-1], interpolation='none', cmap='RdPu')
    plt.savefig(f"resultat_{num_config:03d}.png", dpi=100, bbox_inches='tight')
    plt.close()


for num_config in range(nombre_cas): # save une image for each case -> On peut paralléliser cela
    
    t1 = time.time()
    #créé la grille (360,362)
    cells = np.zeros((nb_iterations, nb_cellules+2), dtype=np.int16) # on laisse les 2 dernieres, une à gauche et autre à droite toujours éteintes 
    cells[0, (nb_cellules+2)//2] = 1

    # print(cells.shape)

    # print(f'processus {rank} chegou aqui')

    #processus maitre
    if(rank==0): 
        
        # envio inicial -> envia 1 pack de mesmo tamanho para cada processo
        count_packs = 1
        for i in range(1,nbp):
            globCom.send(count_packs,dest=i,tag=0) #envia um index de uma linha por vez
            count_packs+=1
        
        #espera mensagem do slave pedindo o proximo pack
        while(count_packs<nb_iterations):
            #verifica mensagem do slave
                message_recv = globCom.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)

                cells[status.Get_tag(),:] = message_recv
                #envia proximo pack com index da linha
                globCom.send(count_packs,dest=status.Get_source(),tag=0)
                count_packs+=1
        
        # recebe as ultimas mensagens -> sai do loop for antes de receber as nbp ultimas 
        for j in range(1,nbp):
            message_recv = globCom.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)
            cells[status.Get_tag(),:] = message_recv
            globCom.send(TERMINATE,dest=status.Get_source(),tag=0)
        
        t2 = time.time()
        compute_time += t2 - t1

        t1 = time.time()
        save_as_md(cells)
        # save_as_png(cells)
        t2 = time.time()
        display_time += t2 - t1

        # processus sclave   
    else:
        # result_calcul =np.zeros((1,nb_cellules+2),dtype=np.double)

        while(True):
            line_iter = globCom.recv(source=0,tag=0)
            if(line_iter==TERMINATE):
                break
            # fait le calcul
            vals = np.left_shift(1, 4*cells[line_iter-1, 0:-2] 
                                + 2*cells[line_iter-1, 1:-1]
                                + cells[line_iter-1, 2:])
            cells[line_iter, 1:-1] = np.logical_and(np.bitwise_and(vals, num_config), 1)       

            # print(cells[line_iter].shape)
            
            globCom.send(cells[line_iter],dest=0,tag=line_iter)
       
print(f"Temps calcul des generations de cellules : {compute_time:.6g}")
print(f"Temps d'affichage des resultats : {display_time:.6g}")

globCom.Disconnect()
