"""
--- Análise do impacto da seleção de pivot (N=500) ---

Ordenado crescente:
    Simples escolhe arr[right] = maior elemento como pivot. Todas as n-1
    comparações sao verdadeiras e o pivot cai sempre em right gerando
    um particionamento desbalanceado. Complexidade O(n²).
    Median-of-three escolhe a mediana real do subarray
    ordenado, gerando partições balanceadas. Complexidade O(n log n).

Ordenado decrescente:
    Simples escolhe arr[right] = menor elemento. Nenhum elemento vai para
    a esquerda, pivot cai sempre em left, também gera um particionamento desbalanceado.
    Complexidade O(n²).
    Median-of-three encontra o centro e particiona de forma balanceada.
    Complexidade O(n log n)

Aleatório:
    Ambas as versões possuem complexidade assintótica idêntica em média O(n log n).
    A diferença no número de comparações, trocas e recursões existe pois
    median-of-three evita ocasionalmente escolhas ruins, mas o impacto
    é modesto.

Quase ordenado:
    Simples sofre quase tanto quanto no caso totalmente ordenado: os 20
    elementos fora de lugar raramente sao escolhidos como pivot, então
    o pivot continua sendo o maior/menor do subarray na maioria das chamadas.
    Median-of-three mantém O(n log n) mesmo neste cenário.

--- Conclusão ---

Median-of-three é amplamente superior ao pivot simples em todos os cenários
parcialmente ordenados, reduzindo muito o número de comparações. Em arrays aleatórios
a vantagem existe mas é modesta.
"""
import random

def make_partition_simple():
    stats = {'comparisons': 0, 'swaps': 0, 'partitions': 0}

    def partition(arr: list, left: int, right: int) -> int:
        stats['partitions'] += 1
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

def median_of_three(arr: list, left: int, right: int) -> int:
    mid = (left + right) // 2
    a, b, c = arr[left], arr[mid], arr[right]
    if (a <= b <= c) or (c <= b <= a):
        return mid
    if (b <= a <= c) or (c <= a <= b):
        return left
    return right

def make_partition_median_of_three():
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

def quicksort(arr: list, partition_fn) -> list:
    arr = arr[:]

    def qs(left: int, right: int) -> None:
        if left < right:
            pi = partition_fn(arr, left, right)
            qs(left, pi - 1)
            qs(pi + 1, right)

    qs(0, len(arr) - 1)
    return arr

N = 500
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
    p_s, s_s = make_partition_simple()
    p_m, s_m = make_partition_median_of_three()
    quicksort(arr, p_s)
    quicksort(arr, p_m)
    results[scenario] = (s_s, s_m)

header = f"{'Cenário':<22} {'Métrica':<14} {'Simple':>10} {'Median3':>10} {'Diff%':>8}"
print(header)
print('-' * len(header))
for scenario, (ss, sm) in results.items():
    for m in metricas:
        vs, vm = ss[m], sm[m]
        diff = (vm - vs) / vs * 100 if vs else 0
        sinal = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"
        print(f"{scenario:<22} {m:<14} {vs:>10} {vm:>10} {diff:>8.1f}")
    print()
