"""🕸️ Soluciones — Dividir trabajo (hilos)"""
import math


def dividir(items, n):
    k, m = divmod(len(items), n)
    return [items[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def tamano_chunk(total, n):
    return math.ceil(total / n)


def cuantos_hilos(total, por_hilo):
    return math.ceil(total / por_hilo)


def aplanar(chunks):
    return [x for bloque in chunks for x in bloque]


def cuantos_chunks(items, tam):
    return (len(items) + tam - 1) // tam


def chunk_n(items, tam, i):
    return items[i * tam:(i + 1) * tam]


def tamanos_chunks(items, tam):
    return [len(items[i:i + tam]) for i in range(0, len(items), tam)]


def ultimo_chunk(items, tam):
    chunks = [items[i:i + tam] for i in range(0, len(items), tam)]
    return chunks[-1] if chunks else []


def tamano_por_hilo(total, hilos):
    return (total + hilos - 1) // hilos


def chunk_mas_grande(chunks):
    return max(chunks, key=len)


def total_items(chunks):
    return sum(len(c) for c in chunks)


def balanceado(chunks):
    tams = [len(c) for c in chunks]
    return max(tams) - min(tams) <= 1


def dividir_en_n(items, n):
    k, m = divmod(len(items), n)
    out = []
    inicio = 0
    for i in range(n):
        t = k + (1 if i < m else 0)
        out.append(items[inicio:inicio + t])
        inicio += t
    return out


def promedio_tamano(chunks):
    return total_items(chunks) / len(chunks)


def chunks_no_vacios(chunks):
    return [c for c in chunks if c]


def indice_de_chunk(items, tam, pos):
    return pos // tam


def cabe_en_chunks(total, tam, max_chunks):
    return (total + tam - 1) // tam <= max_chunks


def asignar_round_robin(items, hilos):
    out = {i: [] for i in range(hilos)}
    for i, x in enumerate(items):
        out[i % hilos].append(x)
    return out


def primer_chunk(items, tam):
    return items[:tam]


def chunk_mas_chico(chunks):
    return min(chunks, key=len)
