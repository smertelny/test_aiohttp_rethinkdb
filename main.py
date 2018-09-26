import asyncio
import rethinkdb as r
import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2

r.set_loop_type('asyncio')

async def conn_pool():
    return await r.connect(port=28015) # Change port on your own

async def subscribe(ws):
    conn = await conn_pool()
    try:
        res = await r.table('tv_shows').changes().run(conn)
        print("Waiting for news!")
        while await res.fetch_next():
            item = await res.next()
            await ws.send_str(str(item))
    except r.ReqlOpFailedError:
        await ws.send_str("Could not connect to DB")
        conn.close()
    finally:
        conn.close()
        

async def index(request):
    ws = web.WebSocketResponse()
    try:
        await ws.prepare(request)
        await ws.send_str("Hello!")
        asyncio.ensure_future(subscribe(ws))
        async for msg in ws:
            print("MESSAGE!!!!")
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(f"Message echo: {msg.data}")
        print('Closing!')
        return ws
    finally:
        ws.close()

@aiohttp_jinja2.template('index.j2')
async def main(request):
    return {}

app = web.Application()
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader('./templates'),
    auto_reload=True
)
app['static_root_url'] = "/static"
app.add_routes([
    web.get('/', main),
    web.get('/ws', index),
    web.static('/static', './static')
])

# web.run_app(app, host="localhost", port=8000)
