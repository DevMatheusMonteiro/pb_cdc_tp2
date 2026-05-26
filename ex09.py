"""
--- Análise do Quicksort de dois pivôs vs. pivot simples (N=500) ---

Funcionamento do Quicksort de dois pivôs:
    Dois pivôs p1 e p2 (com p1 <= p2) dividem o subarray em três regiões:
        [left:lt-1]: elementos < p1
        [lt:gt]: elementos entre p1 e p2 (inclusive)
        [gt+1:right]: elementos > p2
    O algoritmo usa três ponteiros: lt (less-than), k (scanner), gt (greater-than).
    Para cada arr[k]:
        - se arr[k] < p1: troca arr[k] com arr[lt], avança lt e k
        - se arr[k] > p2: troca arr[k] com arr[gt], recua gt (k não avança pois
          o elemento trocado ainda precisa ser classificado)
        - caso contrário: apenas avança k
    Ao final, p1 e p2 são posicionados em lt-1 e gt+1 respectivamente, e
    três chamadas recursivas processam as três regiões resultantes.

Vantagens do Dual-Pivot:
    - Divide o array em três partes por chamada, enquanto o pivot simples divide
      em duas. Em média, isso reduz o número de chamadas recursivas.
    - Menor número de comparações em arrays aleatórios.
    - Mais resistente a arrays com muitos elementos iguais, pois os iguais ficam
      na região central sem gerar chamadas extras.

Desvantagens do Dual-Pivot:
    - Implementação consideravelmente mais complexa: três regiões, três ponteiros,
      lógica de avanço assimétrica.
    - Em arrays já ordenados (crescente ou decrescente) com a escolha ingênua de
      arr[left] e arr[right] como pivôs, pode degradar para O(n²) pelo mesmo
      motivo do pivot simples: um dos pivôs será sempre extremo.
    - O número de trocas pode ser maior que o pivot simples em alguns cenários,
      pois cada elemento pode ser movido mais de uma vez durante o escaneamento.

Ordem crescente:
    Simples: arr[right] é o maior elemento; particionamento degenerado O(n²).
    Dual-Pivot: arr[left]=menor e arr[right]=maior como pivôs. A região central
    fica vazia, toda a recursão cai em um único lado -> O(n²).

Ordem decrescente:
    Simples: arr[right] é o menor elemento; particionamento degenerado O(n²).
    Dual-Pivot: arr[left]=maior e arr[right]=menor; os pivôs são trocados para
    garantir p1 <= p2, mas a distribuição ainda é desbalanceada -> O(n²).

Aleatório:
    Simples: O(n log n) em média.
    Dual-Pivot: O(n log n) em média com constante ligeiramente menor.

Quase ordenado:
    Simples: quase tão ruim quanto o caso totalmente ordenado.
    Dual-Pivot: idem — a escolha ingênua de pivôs sofre os mesmos problemas.

--- Conclusão ---

O Dual-Pivot supera o pivot simples em arrays aleatórios, mas não resolve o
problema do pior caso para arrays ordenados sem uma estratégia de seleção de
pivôs robusta. A complexidade
de implementação é o principal custo frente ao ganho constante obtido.
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

def make_dual_pivot_quicksort():
    stats = {'comparisons': 0, 'swaps': 0, 'partitions': 0}

    def partition(arr: list, left: int, right: int) -> tuple:
        stats['partitions'] += 1

        # Garante p1 <= p2; se não, troca os extremos
        stats['comparisons'] += 1
        if arr[left] > arr[right]:
            arr[left], arr[right] = arr[right], arr[left]
            stats['swaps'] += 1

        p1, p2 = arr[left], arr[right]
        lt = left + 1   # próxima posição da região < p1
        gt = right - 1  # próxima posição da região > p2
        k = left + 1    # scanner

        while k <= gt:
            stats['comparisons'] += 1
            if arr[k] < p1:
                arr[k], arr[lt] = arr[lt], arr[k]
                stats['swaps'] += 1
                lt += 1
                k += 1
            else:
                stats['comparisons'] += 1
                if arr[k] > p2:
                    arr[k], arr[gt] = arr[gt], arr[k]
                    stats['swaps'] += 1
                    gt -= 1
                    # k não avança: o elemento trocado ainda precisa ser avaliado
                else:
                    k += 1

        # Posiciona os pivôs nas fronteiras das três regiões
        lt -= 1
        gt += 1
        arr[left], arr[lt] = arr[lt], arr[left]
        arr[right], arr[gt] = arr[gt], arr[right]
        stats['swaps'] += 2
        return lt, gt

    def sort(arr: list, left: int, right: int) -> None:
        if left >= right:
            return
        lt, gt = partition(arr, left, right)
        sort(arr, left, lt - 1)
        sort(arr, lt + 1, gt - 1)
        sort(arr, gt + 1, right)

    return sort, stats

def quicksort_simple(arr: list, partition_fn) -> list:
    arr = arr[:]

    def qs(left: int, right: int) -> None:
        if left < right:
            pi = partition_fn(arr, left, right)
            qs(left, pi - 1)
            qs(pi + 1, right)

    qs(0, len(arr) - 1)
    return arr

def quicksort_dual(arr: list, sort_fn) -> list:
    arr = arr[:]
    sort_fn(arr, 0, len(arr) - 1)
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
    dp_sort, s_dp = make_dual_pivot_quicksort()
    quicksort_simple(arr, p_s)
    quicksort_dual(arr, dp_sort)
    results[scenario] = (s_s, s_dp)

header = f"{'Cenário':<22} {'Métrica':<14} {'Simple':>10} {'DualPivot':>10} {'Diff%':>8}"
print(header)
print('-' * len(header))
for scenario, (ss, sdp) in results.items():
    for m in metricas:
        vs, vdp = ss[m], sdp[m]
        diff = (vdp - vs) / vs * 100 if vs else 0
        print(f"{scenario:<22} {m:<14} {vs:>10} {vdp:>10} {diff:>8.1f}")
    print()
