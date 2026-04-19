import asyncio
import random

async def coletar_dados(fonte: str, latencia: float) -> dict:
    await asyncio.sleep(latencia)
    valor = random.randint(100, 999)
    return {"fonte": fonte, "dados": valor}

async def main():
    fontes = [
        ("Coleta 1", 2.1),
        ("Coleta 2", 1.5),
        ("Coleta 3", 3.0),
        ("Coleta 4", 1.8),
        ("Coleta 5", 1.2)
    ]
    print("Iniciando coleta de dados...\n")
    tarefas = [coletar_dados(fonte, latencia) for fonte, latencia in fontes]
    resultados = await asyncio.gather(*tarefas)
    print("Resultados:")
    for r in resultados:
        print(f"{r['fonte']}: {r['dados']}")

asyncio.run(main())
