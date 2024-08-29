
# Simulador de Máquina de Turing Não-Determinística

Este projeto implementa uma simulação de uma Máquina de Turing (MT) não-determinística usando uma única fita. O programa recebe a especificação de uma MT em formato JSON e uma palavra de entrada, e verifica se a palavra pertence à linguagem descrita pela máquina.

## Autores

- **Ana Clara Cunha Lopes**
- **Thiago Ribeiro Corrêa**

## Estrutura do Código

### Importações e Funções Auxiliares

```python
import json
import sys
from collections import deque
```

- **json**: Carrega a especificação da Máquina de Turing a partir de um arquivo JSON.
- **sys**: Lê argumentos da linha de comando.
- **deque**: Implementa uma fila de execução de maneira eficiente, usada na exploração das transições.

### Função `load_tm`

```python
def load_tm(filename):
    with open(filename, 'r') as file:
        data = json.load(file)['mt']
        tm = {
            'states': set(data[0]),
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
```

- **Objetivo**: Carregar a especificação da Máquina de Turing a partir de um arquivo JSON.
- **Estrutura da Máquina de Turing**: A máquina é armazenada no dicionário `tm` com estados, alfabetos, transições, estado inicial e estados finais.
- **Processamento das Transições**: Cada transição é armazenada em um dicionário de forma que, para cada combinação de estado e símbolo lido, há uma lista de possíveis transições.

### Função `tm_simulation`

```python
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
```

- **Objetivo**: Determinar se a palavra fornecida é aceita pela Máquina de Turing.
- **Construção da Fita Inicial**: A fita inicial contém o marcador de início, a palavra de entrada, e um grande número de símbolos em branco.
- **Configuração Inicial**: Representa o estado inicial, posição do cabeçote e um dicionário de mudanças na fita.
- **Exploração com BFS**: Usa uma fila (`queue`) para explorar todas as configurações possíveis.
- **Transições**: Para cada transição válida, cria-se uma nova configuração e a adiciona à fila para processamento.
- **Retorno**: Retorna `True` se a palavra for aceita, ou `False` se todas as configurações possíveis forem exploradas sem atingir um estado final.

### Função `main`

```python
def main():
    # Verifica se foi utilizado o formato certo de entrada
    if len(sys.argv) != 3:
        print("Usar: ./mt [MT] [Palavra]")
        return

    tm_filename = sys.argv[1]
    word = sys.argv[2]

    # Prints de teste
    # print("Palavra de entrada: ", word)
    # print("Arquivo .json de entrada: ", tm_filename)

    tm = load_tm(tm_filename)
    
    if tm_simulation(tm, word):
        print("Sim")
    else:
        print("Não")

if __name__ == "__main__":
    main()
```

- **Objetivo**: Função principal que lê os argumentos da linha de comando, carrega a Máquina de Turing e verifica se a palavra é aceita.
- **Validação de Argumentos**: Garante que o número correto de argumentos seja passado.
- **Carregamento da Máquina de Turing**: Chama `load_tm` para carregar a máquina de Turing a partir do arquivo JSON.
- **Verificação da Palavra**: Usa `tm_simulation` para verificar se a palavra é aceita e imprime "Sim" ou "Não" conforme o resultado.

## Compilação e Execução

Este programa é escrito em Python, portanto, não é necessário compilar o código. Para executar o programa, basta seguir os passos abaixo:

1. Certifique-se de que o Python está instalado.
2. Prepare um arquivo JSON contendo a especificação da Máquina de Turing.
3. Execute o programa com:

```bash
$ python3 mt.py mt.json "palavra"
```

Onde `mt.json` é o arquivo JSON com a especificação da máquina e `"palavra"` é a palavra a ser verificada.

## Exemplo de Uso

```bash
$ python3 mt.py mt.json "bbabbbb"
Sim

$ python3 mt.py mt.json ""
Não
```

## Observações

- O programa utiliza uma abordagem busca em largua (BFS) para explorar todas as transições possíveis, garantindo que todas as configurações válidas sejam consideradas.
- A fita é implementada como uma lista, permitindo simular uma fita virtualmente infinita.


