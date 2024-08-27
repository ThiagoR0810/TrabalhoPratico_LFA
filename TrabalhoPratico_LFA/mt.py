#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from collections import deque

def carregar_maquina_turing():
    # Lê o arquivo .json e atribui ele a variável "mt_data". Essa variável se torna um dicionário.
    with open(sys.argv[1]) as file:
        mt_data = json.load(file)
        return mt_data["mt"]

def interpretar_maquina_turing(mt, palavra_entrada):
    # Separa o dicionário nas partes que queremos.
    conj_estados = mt[0]
    alfabeto_entrada = mt[1]
    alfabeto_fita = mt[2]
    simbolo_inicio_fita = mt[3]
    simbolo_celula_vazia = mt[4]
    conj_transicoes = mt[5]
    estado_inicial = mt[6]
    conj_estados_finais = mt[7]

    # Inicializa a fita
    fita = list(simbolo_inicio_fita + palavra_entrada + simbolo_celula_vazia * (len(palavra_entrada) + 1))
    
    # Prints de teste
    # print("Palavra de entrada: ", palavra_entrada, "; Tamanho da palavra de entrada: ", len(palavra_entrada), "; Primeira letra: ", palavra_entrada[0])
    # print("Conjunto de estados: ", conj_estados)
    # print("Alfabeto de entrada: ", alfabeto_entrada)
    # print("Alfabeto da fita: ", alfabeto_fita)
    # print("Simbolo marcador de inicio da fita: ", simbolo_inicio_fita)
    # print("Simbolo de celulas vazias da fita: ", simbolo_celula_vazia)
    # print("Funcao de transicao", conj_transicoes, "; Número de funcoes: ", len(conj_transicoes))
    # print("Estado inicial: ", estado_inicial)
    # print("Conjunto de estados finais: ", conj_estados_finais)
    # print(fita)
    
    return simular_maquina_turing(estado_inicial, fita, 1, conj_transicoes, conj_estados_finais, simbolo_celula_vazia)

def simular_maquina_turing(estado_atual, fita, posicao_cabecote, conj_transicoes, conj_estados_finais, simbolo_celula_vazia):
    if estado_atual in conj_estados_finais:
        return True
    
    for transicao in conj_transicoes:
        if estado_atual == transicao[0] and fita[posicao_cabecote] == transicao[1]:
            print("Transição: ", transicao)
            print("Posição cabeçote: ", posicao_cabecote)
            print("Célula atual: ", fita[posicao_cabecote])
            estado_novo = transicao[2]
            fita[posicao_cabecote] = transicao[3]
            if transicao[4] == ">":
                posicao_cabecote = posicao_cabecote + 1
            elif transicao[4] == "<":
                posicao_cabecote = posicao_cabecote - 1
            simular_maquina_turing(estado_novo, fita, posicao_cabecote, conj_transicoes, conj_estados_finais, simbolo_celula_vazia)

    return False

# Lê a palavra de entrada e a atribui à variável "palavra_entrada".
palavra_entrada = sys.argv[2]

mt = carregar_maquina_turing()
resultado = interpretar_maquina_turing(mt, palavra_entrada)

if resultado:
    print("Sim")
else:
    print("Não")
