import heapq
import math
from itertools import count
from collections import Counter


# Построение дерева Хаффмана
def build_huffman(freq):
    if not freq:
        raise ValueError("Пустой алфавит")

    order = count()

    heap = [
        (w, next(order), s)
        for s, w in freq.items() if w > 0
    ]

    heapq.heapify(heap)

    if not heap:
        raise ValueError("Все частоты нулевые")

    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)

        heapq.heappush(
            heap,
            (w1 + w2, next(order), (left, right))
        )

    tree = heap[0][2]
    codes = {}

    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")

    walk(tree)

    return tree, codes


# Кодирование текста
def encode(text, codes):
    return "".join(codes[s] for s in text)


# Декодирование текста
def decode(bits, tree):
    if isinstance(tree, str):
        if any(b != "0" for b in bits):
            raise ValueError("Некорректный код")
        return tree * len(bits)

    result = []
    node = tree

    for b in bits:
        if b not in "01":
            raise ValueError("Недопустимый бит")

        node = node[int(b)]

        if isinstance(node, str):
            result.append(node)
            node = tree

    if node is not tree:
        raise ValueError("Неполное кодовое слово")

    return "".join(result)


# Исходное сообщение
text = "ABCADE"

# Подсчёт частот
freq = Counter(text)

# Построение дерева и кодов
tree, codes = build_huffman(freq)

# Кодирование
bits = encode(text, codes)

# Расчёт характеристик
N = sum(freq.values())
probabilities = {s: n / N for s, n in freq.items()}

L = sum(probabilities[s] * len(codes[s]) for s in freq)

H = -sum(
    p * math.log2(p)
    for p in probabilities.values()
)

eta = H / L * 100
R = 100 - eta

# Проверка декодирования
decoded = decode(bits, tree)

print("Частоты:", freq)
print("Коды:", codes)
print("Закодированное сообщение:", bits)
print("Длина:", len(bits), "бит")
print("Энтропия:", round(H, 4))
print("Средняя длина:", round(L, 4))
print("Эффективность:", round(eta, 2), "%")
print("Избыточность:", round(R, 2), "%")
print("Декодирование:", decoded)

assert decoded == text

# Проверка одного символа
tree_one, codes_one = build_huffman({"A": 5})
print("Код одного символа:", codes_one)
