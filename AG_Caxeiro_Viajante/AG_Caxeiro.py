# Allgorito Genetico
import csv
import tkinter

import numpy as np
from random import random
import math
import random
import matplotlib.pyplot as plt
from tkinter import *
from functools import partial
import statistics
from pathlib import Path


def Programa(tamanho_populacao, max_gen, taxa_de_mutacao, taxa_de_cruzamento):
    arq_FIT_min = []
    arq_IND_min = []
    interacao = 0

    tamanho_populacao = int(tamanho_populacao.get())
    max_gen = int(max_gen.get())
    taxa_mutacao = float(taxa_de_mutacao.get()) / 100
    taxa_cruzamento = float(taxa_de_cruzamento.get()) / 100

    if taxa_mutacao > 1:
        taxa_mutacao = 1
    if taxa_mutacao < 0:
        taxa_mutacao = 0
    if taxa_cruzamento > 1:
        taxa_cruzamento = 1
    if taxa_cruzamento < 0:
        taxa_cruzamento = 0

    matriz_distancia = np.loadtxt('Database/lau15_dist.txt', dtype='int')
    num_city = len(matriz_distancia)

    file_AG = open('AG_Final.csv', 'a+', newline='', encoding='utf-8')
    w_final = csv.writer(file_AG)

    if Path('AG_Final.csv').stat().st_size == 0:
        w_final.writerow(['Ordem_Cidades', 'Melhor FIT', 'Pior FIT', 'Media', 'Desvio_Padrao'])
    w_final.writerow(['Populacao : {}'.format(tamanho_populacao), 'Geracoes : {}'.format(max_gen), '#########',
                      'Taxa_Mutacao : {}'.format(taxa_mutacao), 'Taxa_Cruzamento : {}'.format(taxa_cruzamento)])


    while interacao < 10:
        min_fit = []
        populacao = []
        individuo_fit = []
        populacao_intermediaria = []
        min_ind = []
        numero_de_geracoes = 1

        populacao_inicial(populacao, num_city, tamanho_populacao)

        while numero_de_geracoes <= max_gen:
            for i in populacao:
                funcao_objetivo(len(matriz_distancia), i, matriz_distancia, individuo_fit)

            selecao(populacao, tamanho_populacao, populacao_intermediaria, individuo_fit, num_city, taxa_cruzamento)
            mutacao(tamanho_populacao, taxa_mutacao, num_city, populacao_intermediaria)
            elitismo(populacao, populacao_intermediaria, individuo_fit)

            populacao = populacao_intermediaria[:]  # nao retire o 2 pontos
            min_fit.append(individuo_fit[0])
            min_ind.append(populacao_intermediaria[0])

            individuo_fit = []
            populacao_intermediaria = []
            numero_de_geracoes += 1
        arq_FIT_min.append(min(min_fit))
        arq_IND_min.append(min_ind[min_fit.index(min(min_fit))])
        interacao += 1

    media = statistics.mean(arq_FIT_min)
    desvio = np.std(arq_FIT_min)
    melhor_fit = min(arq_FIT_min)
    pior_fit = max(arq_FIT_min)

    w_final.writerow([arq_IND_min[arq_FIT_min.index(melhor_fit)], melhor_fit, pior_fit, media, desvio])
    file_AG.close()
    # Plot(max_gen, fit_gen_graph)


def populacao_inicial(populacao, num_city, tamanho_populacao):
    for i in range(tamanho_populacao):
        populacao.append([])  # alocando cada individuo
        populacao[i] = random.sample(range(0, num_city), num_city)


def funcao_objetivo(n, permutacao, rho, individuo_fit):
    distancia = 0
    for c, p in enumerate(permutacao):
        if c < n - 1:
            distancia += rho[permutacao[c]][permutacao[c + 1]]
    distancia += rho[permutacao[n - 1]][permutacao[0]]
    individuo_fit.append(distancia)


# def selecaoRoleta(populacao, individuo_fit, populacao_intermediaria, tamanho_populacao,
#                   taxa_cruzamento,num_city):
#     aux_fitness = []
#     roleta = []
#     cont = 0
#
#     for ind in individuo_fit:
#         aux_fitness.append(1 / ind)
#
#     pfitness = sum(aux_fitness)
#
#     for ind in aux_fitness:
#         roleta.append(ind / pfitness)
#
#     while (len(populacao_intermediaria) < tamanho_populacao):
#
#         auxroleta = 0
#         pai1 = 0
#         pai2 = 0
#         sort1 = random.uniform(0,pfitness)
#         sort2 = random.uniform(0,pfitness)
#
#         for i in roleta:
#             if auxroleta < sort1:
#                 auxroleta += i
#                 pai1 = roleta.index(i)
#
#         auxroleta = 0
#
#         for i in roleta:
#             if auxroleta < sort2:
#                 auxroleta += i
#                 pai2 = roleta.index(i)
#
#         if (pai1 != pai2):
#             prob_sort = random.random()
#             if (taxa_cruzamento >= prob_sort):
#                  Cruzamento(populacao, populacao_intermediaria, pai1, pai2, num_city)


def selecao(populacao, tamanho_populacao, populacao_intermediaria, individuo_fit, num_city, taxa_cruzamento):
    # Basicamente vou pegar 4 individuos aleatorios a cada interação e sellecionar pais
    # Que irão gerar minha proxima Geraçao a partir de um Cruzamento.

    while (len(populacao_intermediaria) < tamanho_populacao):
        r = random.sample(range(0, tamanho_populacao), 4)
        pai1 = r[0]
        if (individuo_fit[r[0]] > individuo_fit[r[1]]):
            pai1 = r[1]
        pai2 = r[2]
        if (individuo_fit[r[2]] > individuo_fit[r[3]]):
            pai2 = r[3]

        if (pai1 != pai2):
            prob_sort = random.random()
            if (taxa_cruzamento >= prob_sort):
                Cruzamento(populacao, populacao_intermediaria, pai1, pai2, num_city)
            else:
                populacao_intermediaria.append(populacao[pai1])


def Cruzamento(populacao, populacao_intermediaria, pai1, pai2, num_city):
    alelo1 = random.randrange(2, num_city - 1)
    alelo2 = random.randrange(2, num_city - 1)
    parte1 = []
    parte2 = []
    filho = []

    while (alelo1 == alelo2):
        alelo1 = random.randrange(2, num_city - 1)
        alelo2 = random.randrange(2, num_city - 1)

    if alelo1 < alelo2:
        filho = populacao[pai1][alelo1:alelo2]
        cont_cromossomo = alelo2
        i = alelo2
        while cont_cromossomo < num_city:
            if i < len(populacao[pai2]):
                if populacao[pai2][i] not in filho:
                    parte1.append(populacao[pai2][i])
                    cont_cromossomo += 1
                i += 1
            else:
                i = 0
        filho.extend(parte1)
        cont_cromossomo = 0
        while cont_cromossomo < alelo1:
            if i < len(populacao[pai2]):
                if populacao[pai2][i] not in filho:
                    parte2.append(populacao[pai2][i])
                    cont_cromossomo += 1
                i += 1
            else:
                i = 0

        parte2.extend(filho)
        filho = parte2

    if alelo1 > alelo2:
        filho = populacao[pai1][alelo2:alelo1]
        cont_cromossomo = alelo1
        i = alelo1
        while cont_cromossomo < num_city:
            if i < len(populacao[pai2]):
                if populacao[pai2][i] not in filho:
                    parte1.append(populacao[pai2][i])
                    cont_cromossomo += 1
                i += 1
            else:
                i = 0
        filho.extend(parte1)
        cont_cromossomo = 0
        while cont_cromossomo < alelo2:
            if i < len(populacao[pai2]):
                if populacao[pai2][i] not in filho:
                    parte2.append(populacao[pai2][i])
                    cont_cromossomo += 1
                i += 1
            else:
                i = 0

        parte2.extend(filho)
        filho = parte2

    populacao_intermediaria.append(filho)


def mutacao(tamanho_populacao, taxa_mutacao, num_city, populacao_intermediaria):
    # para realizar a mutacao precisamos percorrer por toda a populacao_intermediaria
    for i in range(tamanho_populacao):
        mutacao = random.random()
        # sorteio uma taxa de mutação
        if mutacao <= taxa_mutacao:  # sematriz_distancia minha taxa for igual ou menor que minha taxa de mutação
            mutacao1 = random.randrange(0, num_city)
            for j in range(mutacao1):
                troca1 = random.randrange(0, num_city)
                troca2 = random.randrange(0, num_city)

                while troca1 == troca2:
                    troca1 = random.randrange(0, num_city)
                    troca2 = random.randrange(0, num_city)

                if troca1 != troca2:
                    aux = populacao_intermediaria[i][troca1]
                    populacao_intermediaria[i][troca1] = populacao_intermediaria[i][troca2]
                    populacao_intermediaria[i][troca2] = aux


def elitismo(populacao, populacao_intermediaria,
             individuo_fit):  # Para a Fuunção de Elitismo vamos procurar o menor valor do individuo fit
    min_fit = individuo_fit[0]  # Defino o min_fit como o primeiro individuo e verifico entre eles qual o menor
    min_pos = 0
    for i in individuo_fit:
        if i < min_fit:
            min_fit = i
            min_pos = individuo_fit.index(min_fit)  # salvo a posicao do inviduo fit
    populacao_intermediaria[0] = populacao[min_pos][:]


def Arquivo():
    janela = Tk()  # criamos a janela
    j1 = janela.geometry('1080x720')
    center(janela)
    janela.title('AG_Real')
    E = Text(janela, height=1080, width=720)  # criamos o widget Text
    arquivo = open('AG_Final.csv')  # função de abertura para ler
    z = arquivo.read()  # função ler, read
    E.insert(0.0, z)  # aqui inserimos o texto dentro do widget Text.
    E.pack()  # empacotanos o widget Text
    janela.mainloop()  # fazemos o loop da janela.


def Arquivo_Delete():
    arquivo = open('AG_Final.csv', 'w')  # função de abertura para ler
    arquivo.close()


def center(win):
    win.update_idletasks()  # Update "requested size" from geometry manager
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width

    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2

    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    win.deiconify()


def Interface():
    back = '#6C6C94'
    back_label = '#5fb3fc'
    fore = '#001582'
    fonte = ("Aller", 14, "italic", "bold")
    fontTitle = ("Aller", 18, "italic", "bold")
    window = Tk()
    window.title('AG_Caxeiro_Viajante')
    window.geometry('1080x720')
    window.minsize(1080, 720)
    window.maxsize(1080, 720)
    image = tkinter.PhotoImage(file="back.png")
    image = image.subsample(1, 1)
    labelimage = Label(image=image)
    labelimage.place(x=0, y=0, relwidth=1.0, relheight=1.0)
    center(window)
    # window.configure(background=back)
    textoIni = Label(window, text='Algoritmo Genetico', background=back_label, foreground=fore)
    textoIni.configure(font=fontTitle)
    textoIni.place(x=430, y=10, width=300, height=50)

    tp = Label(window, text='Tamanho_População  : ', background=back_label, foreground=fore)
    tp.configure(font=fonte)
    tp.place(x=10, y=80, width=250, height=40)

    tamanho_populacao = Entry(window)
    tamanho_populacao.configure(font=fonte, foreground=fore)
    tamanho_populacao.place(x=280, y=80, width=250, height=40)
    #
    ng = Label(window, text='Numero_Gerações  :  ', background=back_label, foreground=fore)
    ng.configure(font=fonte)
    ng.place(x=10, y=150, width=250, height=40)

    max_gen = Entry(window)
    max_gen.configure(font=fonte, foreground=fore)
    max_gen.place(x=280, y=150, width=250, height=40)
    #
    tm = Label(window, text='Taxa de mutação  : ', background=back_label, foreground=fore)
    tm.configure(font=fonte)
    tm.place(x=10, y=220, width=250, height=40)

    taxa_de_mutacao = Entry(window)
    taxa_de_mutacao.configure(font=fonte, foreground=fore)
    taxa_de_mutacao.place(x=280, y=220, width=250, height=40)
    #
    tc = Label(window, text='Taxa de Cruzamento  : ', background=back_label, foreground=fore)
    tc.configure(font=fonte)
    tc.place(x=10, y=290, width=250, height=40)

    taxa_de_cruzamento = Entry(window)
    taxa_de_cruzamento.configure(font=fonte, foreground=fore)
    taxa_de_cruzamento.place(x=280, y=290, width=250, height=40)
    #
    bt = Button(window, text='Compilar',
                command=partial(Programa, tamanho_populacao, max_gen, taxa_de_mutacao, taxa_de_cruzamento),
                background=back_label, foreground=fore, borderwidth=5)
    bt.configure(font=fonte)
    bt.place(x=150, y=550, width=200, height=50)

    bt = Button(window, text='Ver Arquivo.csv', command=partial(Arquivo), background=back_label, foreground=fore)
    bt.configure(font=fonte, borderwidth=5)
    bt.place(x=450, y=550, width=200, height=50)

    bt = Button(window, text='Resetar CSV', command=partial(Arquivo_Delete), background=back_label,
                foreground=fore, borderwidth=5)
    bt.configure(font=fonte)
    bt.place(x=750, y=550, width=200, height=50)
    window.mainloop()


Interface()
