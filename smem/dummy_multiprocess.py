import concurrent.futures
import time
import itertools
import sys

def process_batch(gquery, graphs):
    # lógica do graph matcher
    results = []
    for i in range(len(graphs)):
        graph = graphs[i]
        if graph == gquery: results.append(i)
    
    # espera ocupada para perceber que existem vários processos em execucao
    for i in range(int(1e9)): continue

    return results

def main():
    # nworkers (deve ser um parametro)
    nworkers = int(sys.argv[1])

    # resultados finais
    results = []
        
    # consulta
    gquery = 6
    

    # grafos organizados em batches (lotes)
    batch1 = [1, 2, 5, 6, 8]
    batch2 = [1, 2, 5, 6, 8]
    batch3 = [1, 2, 5, 3, 8]
    batch4 = [1, 6, 8, 7, 9]
    batch5 = [1, 6, 8, 7, 9]
    batch6 = [1, 6, 8, 7, 9]
    batch7 = [1, 6, 8, 7, 9]
    batch8 = [1, 6, 8, 7, 9]
    batch9 = [1, 6, 8, 7, 9]
    batch10 = [1, 6, 8, 6, 9]
    graphbatches = [batch1, batch2, batch3, batch4, batch5, batch6, batch7,
                    batch8, batch9, batch10]
    
    # muito importante que o executor seja PROCESS, para garantir multiplos
    # processos python e não cair na armadilha do GIL (Global Interpreter Lock)
    with concurrent.futures.ProcessPoolExecutor(nworkers) as executor:
        # submissao de tarefas de forma assíncrona
        futures = [executor.submit(process_batch, gquery, graphs) for graphs in graphbatches]
    
        # parent data
        batchs = list(range(100000000))

        # Observacao: você verá vários processos (child) gerados e com a memória
        # residente igual a do processo pai (parent), entretanto, geralmente
        # páginas de memória são compartilhadas até que o processo filho escreva
        # em alguma delas (nesse ponto, ele ganharia uma cópia daquela página e
        # a mesma ocuparia e incrementaria a RAM). Portanto, desde que você se
        # limite a apenas LER informações passadas aos processos filhos, estamos
        # OK. Este exemplo tenta simular esse comportamento.

        # coletar resultados à medida em que eles são produzidos
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    results = itertools.chain(*results)
    print(list(results)) # evitar chamar list ao iterar, nao e necessario

if __name__ == "__main__":
    main()

