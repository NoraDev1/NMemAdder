from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    bot_log_path = f'logs.txt'
    m_list = open(bot_log_path, "r").read()
    message_s = m_list.replace("\n","")
    return web.json_response(message_s)


async def web_server():
    web_app = web.Application(client_max_size=30000000000)
    web_app.add_routes(routes)
    return web_app
