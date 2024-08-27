#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from collections import deque

arquivo_entrada = sys.argv[1]

def carregar_maquina_turing():
    # Lê o arquivo .json e atribui ele a variável "arquivo_JSON". Essa variável se torna um dicionário.
    with open(sys.argv[1]) as file:
        mt_data = json.load(file)
        return mt_data["mt"]

# Lê a palavra de entrada e a atribui à variável "palavra_entrada".
palavra_entrada = sys.argv[2]


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

    # Criação das variáveis para fazer a movimentação do cabeçote na fita
    direita = ">"
    esquerda = "<"
    
    # Inicializa a fita
    fita = list(simbolo_inicio_fita + palavra_entrada + simbolo_celula_vazia * (len(palavra_entrada) + 1))
    return simular_maquina_turing(estado_inicial, fita, 1, conj_transicoes, conj_estados_finais, simbolo_celula_vazia)

def simular_maquina_turing(estado_atual, fita, posicao, transicoes, estados_finais, simbolo_vazio):
    # Fila para armazenar todas as possíveis configurações (estado, posição, fita)
    fila = deque([(estado_atual, posicao, fita)])

    while fila:
        estado_atual, posicao, fita_atual = fila.popleft()

        # Verificar se estamos em um estado final e a palavra é reconhecida
        if estado_atual in estados_finais:
            return True

        # Ler o símbolo atual na fita
        simbolo_lido = fita_atual[posicao]

        # Buscar possíveis transições
        for transicao in transicoes:
            if transicao[0] == estado_atual and transicao[1] == simbolo_lido:
                for nova_transicao in transicao[2]:
                    novo_estado, simbolo_escrito, movimento = nova_transicao

                    # Criar nova fita e aplicar a transição
                    nova_fita = fita_atual[:]
                    nova_fita[posicao] = simbolo_escrito

                    # Mover a cabeça da fita
                    if movimento == ">":
                        nova_posicao = posicao + 1
                    elif movimento == "<":
                        nova_posicao = posicao - 1
                    else:
                        raise ValueError("Movimento inválido")

                    # Adicionar nova configuração à fila
                    fila.append((novo_estado, nova_posicao, nova_fita))

    # Se todas as configurações possíveis forem exploradas e nenhuma reconheceu a palavra, retornar False
    return False

mt = carregar_maquina_turing()
resultado = interpretar_maquina_turing(mt, palavra_entrada)

if resultado:
    print(f"A Máquina de Turing reconhece a palavra '{palavra_entrada}'.")
else:
    print(f"A Máquina de Turing não reconhece a palavra '{palavra_entrada}'.")

# print("Arquivo JSON: ", arquivo_JSON)

# Prints de teste
# print("Palavra de entrada: ", palavra_entrada, "; Tamanho da palavra de entrada: ", len(palavra_entrada), "; Primeira letra: ", palavra_entrada[0])
# print("Conjunto de estados: ", conj_estados)
# print("Alfabeto de entrada: ", alfabeto_entrada)
# print("Alfabeto da fita: ", alfabeto_fita)
# print("Simbolo marcador de inicio da fita: ", simbolo_inicio_fita)
# print("Simbolo de celulas vazias da fita: ", simbolo_celula_vazia)
# print("Funcao de transicao", funcao_transicao, "; Número de funcoes: ", len(funcao_transicao))
# print("Estado inicial: ", estado_inicial)
# print("Conjunto de estados finais: ", conj_estados_finais)

# print(len(arquivo_JSON["mt"][0]))

    

