import asyncio

LOCALHOST = "127.0.0.1"
PORTA = 8888

async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"[servidor] conexão de {addr}")
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            msg = data.decode().strip()
            response = f"[servidor] {addr} -> {msg!r}\n"
            print(response)
            writer.write(response.encode())
            await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[servidor] encerrou conexão de {addr}")

async def main():
    server = await asyncio.start_server(handler, LOCALHOST, PORTA)
    print(f"[servidor] executando em {LOCALHOST}:{PORTA}")
    async with server:
        await server.serve_forever()

asyncio.run(main())
