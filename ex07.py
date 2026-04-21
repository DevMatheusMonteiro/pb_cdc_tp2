"""
--- Análise do impacto do histórico (N=1000, K=500) ---

Ordenado crescente / Quase ordenado:
  median-of-three ja escolhe o pivot perfeito na primeira chamada (o elemento
  central cai exatamente na posição alvo). O histórico nao tem chance de
  contribuir
  Resultado: ambas as versões são idênticas.

Ordenado decrescente:
  O histórico reduz o número de comparações,
  mas aumenta o numero de partitions em 25%. Isso ocorre porque o primeiro
  pivot escolhido é alto, enviesa o histórico, e as partições seguintes
  ficam desbalanceadas — mais chamadas recursivas no total.
  Resultado: histórico é pior neste cenário.

Aleatório:
  O histórico reduz as chamadas de partições, mas cada partição
  varre um subarray maior, gerando um número maior de comparações e trocas.
  Além disso, choose_pivot executa um min() O(n) extra por chamada.
  Resultado: histórico é pior.

--- Conclusão ---

Não vale a pena implementar histórico nesses casos apresentados aqui.
Em nenhum cenário ele reduz simultaneamente comparações, trocas e recursões.
O overhead de choose_pivot (busca linear do elemento mais proximo)
consome mais do que o ganho obtido pela melhor escolha de pivot.
"""

import random

def median_of_three(arr: list, left: int, right: int) -> int:
    mid = (left + right) // 2
    a, b, c = arr[left], arr[mid], arr[right]
    if (a <= b <= c) or (c <= b <= a):
        return mid
    if (b <= a <= c) or (c <= a <= b):
        return left
    return right


def make_partition_classic():
    stats = {'comparisons': 0, 'swaps': 0, 'partitions': 0}

    def partition(arr: list, left: int, right: int) -> int:
        stats['partitions'] += 1
        pi = median_of_three(arr, left, right)
        arr[pi], arr[right] = arr[right], arr[pi]
        stats['swaps'] += 1
        pivot = arr[right]
        i = left - 1
        for j in range(left, right):
            stats['comparisons'] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                stats['swaps'] += 1
        arr[i + 1], arr[right] = arr[right], arr[i + 1]
        stats['swaps'] += 1
        return i + 1

    return partition, stats

def make_partition_history(k_hist: int = 3):
    stats = {'comparisons': 0, 'swaps': 0, 'partitions': 0}
    history: list = []

    def choose_pivot(arr: list, left: int, right: int) -> int:
        mid = (left + right) // 2
        candidates = [left, mid, right]
        if history:
            hist_median = sorted(history)[len(history) // 2]
            closest = min(range(left, right + 1), key=lambda i: abs(arr[i] - hist_median))
            candidates.append(closest)
        candidates.sort(key=lambda i: arr[i])
        return candidates[len(candidates) // 2]

    def partition(arr: list, left: int, right: int) -> int:
        stats['partitions'] += 1
        pi = choose_pivot(arr, left, right)
        arr[pi], arr[right] = arr[right], arr[pi]
        stats['swaps'] += 1
        pivot = arr[right]
        history.append(pivot)
        if len(history) > k_hist:
            history.pop(0)
        i = left - 1
        for j in range(left, right):
            stats['comparisons'] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                stats['swaps'] += 1
        arr[i + 1], arr[right] = arr[right], arr[i + 1]
        stats['swaps'] += 1
        return i + 1

    return partition, stats

def quickselect(arr: list, k: int, partition_fn) -> int:
    arr = arr[:]
    target = k - 1

    def qs(left: int, right: int) -> int:
        pivot_index = partition_fn(arr, left, right)
        if pivot_index == target:
            return arr[pivot_index]
        if target < pivot_index:
            return qs(left, pivot_index - 1)
        return qs(pivot_index + 1, right)

    return qs(0, len(arr) - 1)

N = 1000
K = N // 2

random.seed(42)

scenarios = {
    'Ordenado crescente': list(range(1, N + 1)),
    'Ordenado decrescente': list(range(N, 0, -1)),
    'Aleatorio': random.sample(range(1, N * 10), N),
    'Quase ordenado': list(range(1, N - 19)) + random.sample(range(N, N * 2), 20),
}

metricas = ('comparisons', 'swaps', 'partitions')
results = {}

for scenario, arr in scenarios.items():
    p_c, s_c = make_partition_classic()
    p_h, s_h = make_partition_history()
    quickselect(arr, K, p_c)
    quickselect(arr, K, p_h)
    results[scenario] = (s_c, s_h)

header = f"{'Cenário':<22} {'Métrica':<14} {'Classic':>10} {'History':>10} {'Diff%':>8}"
print(header)
print('-' * len(header))
for scenario, (sc, sh) in results.items():
    for m in metricas:
        vc, vh = sc[m], sh[m]
        diff = (vh - vc) / vc * 100
        print(f"{scenario:<22} {m:<14} {vc:>10} {vh:>10} {diff:>8.1f}%")
    print()
