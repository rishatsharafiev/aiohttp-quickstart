from aiohttp import web

async def hello(request):
    return web.Response(text="Hello, world")

async def get_handler(request):
    return web.Response(text="get_handler")

async def post_handler(request):
    return web.Response(text="post_handler")

async def put_handler(request):
    return web.Response(text="put_handler")

async def all_handler(request):
    text = f'all_handler, method: {request.method}'
    return web.Response(text=text)

async def get_without_head_handler(request):
    return web.Response(text="get_without_head_handler")

app = web.Application()

app.router.add_get('/', hello)
app.router.add_get('/get', get_handler)
app.router.add_post('/post', post_handler)
app.router.add_put('/put', put_handler)
app.router.add_route('*', '/path', all_handler)
app.router.add_get('/get_without_head', get_without_head_handler, allow_head=False) # HEAD will response code 405

web.run_app(app)