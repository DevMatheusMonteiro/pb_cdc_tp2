"""
Demonstração: event loop bloqueado vs com asyncio.to_thread()

Cenário A - chamada síncrona direta:
  O event loop fica bloqueado durante os 3s de time.sleep(),
  impedindo qualquer outra tarefa de rodar no meio-tempo.

Cenário B - chamada via asyncio.to_thread():
  A função pesada roda em uma thread separada.
  O event loop continua livre para executar outras coroutines em paralelo.
"""
import asyncio
import time

def tarefa_pesada(nome: str) -> int:
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] tarefa_pesada '{nome}' iniciando (3s)")
    time.sleep(3)
    resultado = sum(range(1_000_000))
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] tarefa_pesada '{nome}' concluída (resultado={resultado})")

async def coroutine(label: str):
    await asyncio.sleep(1)
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] coroutine '{label}' executou")

async def cenario_a():
    print("--- CENÁRIO A: chamada síncrona direta ---")
    asyncio.create_task(coroutine("A"))
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] chamando tarefa_pesada diretamente")
    tarefa_pesada("A")
    await asyncio.sleep(2)
    print("coroutine só executou depois que tarefa_pesada terminou")

async def cenario_b():
    print("--- CENÁRIO B: via asyncio.to_thread() ---")
    asyncio.create_task(coroutine("B"))
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] delegando tarefa_pesada para thread com asyncio.to_thread()")
    await asyncio.to_thread(tarefa_pesada, "B")
    print("coroutine executou durante a tarefa_pesada")

async def main():
    await cenario_a()
    print("\n" + "="*50 + "\n")
    await cenario_b()

asyncio.run(main())
