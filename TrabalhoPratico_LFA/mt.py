#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
from collections import deque

def load_tm(filename):
    with open(filename, 'r') as file:
        data = json.load(file)['mt']
        tm = {
            'states': data[0],
            'input_alphabet': set(data[1]),
            'tape_alphabet': set(data[2]),
            'start_marker': data[3],
            'blank_symbol': data[4],
            'transitions': {},
            'initial_state': data[6],
            'final_states': set(data[7])
        }
        for trans in data[5]:
            state, read, next_state, write, move = trans
            if (state, read) not in tm['transitions']:
                tm['transitions'][(state, read)] = []
            tm['transitions'][(state, read)].append((next_state, write, move))
            
        # Prints de teste
        # print("Conjunto de estados: ", tm['states'])
        # print("Alfabeto de entrada: ", tm['input_alphabet'])
        # print("Alfabeto da fita: ", tm['tape_alphabet'])
        # print("Simbolo marcador de inicio da fita: ", tm['start_marker'])
        # print("Simbolo de celulas vazias da fita: ", tm['blank_symbol'])
        # print("Funcao de transicao", tm['transitions'], "; Número de funcoes: ", len(tm['transitions']))
        # print("Estado inicial: ", tm['initial_state'])
        # print("Conjunto de estados finais: ", tm['final_states'])
        
    return tm

def tm_accepts(tm, word):
    # Constrói a fita inicial com a palavra de entrada
    tape = list(tm['start_marker'] + word + tm['blank_symbol'] * 1000)
    # print(tape)  
    
    initial_config = (tm['initial_state'], 1, {})  # (estado, posição do cabeçote, mudanças na fita)
    
    # Utilizando BFS para explorar todas as transições possíveis
    queue = deque([initial_config])
    
    while queue:
        state, head_pos, tape_changes = queue.popleft()

        # Aplica as mudanças na fita atual
        for pos, symbol in tape_changes.items():
            tape[pos] = symbol

        if state in tm['final_states']:
            return True
        
        current_symbol = tape[head_pos]

        for next_state, write_symbol, move_direction in tm['transitions'].get((state, current_symbol), []):
            # Cria um novo dicionário de mudanças
            new_tape_changes = tape_changes.copy()
            new_tape_changes[head_pos] = write_symbol

            # Calcula a nova posição do cabeçote
            new_head_pos = head_pos + (1 if move_direction == '>' else -1)
            
            # Expande a fita, se necessário
            if new_head_pos < 0:
                tape.insert(0, tm['blank_symbol'])
                new_tape_changes = {k + 1: v for k, v in new_tape_changes.items()}
                new_head_pos = 0
            elif new_head_pos >= len(tape):
                tape.append(tm['blank_symbol'])

            # Adiciona a nova configuração na fila
            queue.append((next_state, new_head_pos, new_tape_changes))
    
    return False

def main():
    if len(sys.argv) != 3:
        print("Usar: ./mt [MT] [Palavra]")
        return

    tm_filename = sys.argv[1]
    word = sys.argv[2]
    
    # Prints de teste
    # print("Palavra de entrada: ", word)
    # print("Arquivo .json de entrada: ", tm_filename)

    tm = load_tm(tm_filename)
    
    if tm_accepts(tm, word):
        print("Sim")
    else:
        print("Não")

if __name__ == "__main__":
    main()
