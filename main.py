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

async def get_resource_handler(request):
    return web.Response(text="get_resource_handler")

async def variable_resource_handler(request):
    name = request.match_info['name']
    return web.Response(text=f"Hello, {name}")

app = web.Application()

app.router.add_get('/', hello)
app.router.add_get('/get', get_handler)
app.router.add_post('/post', post_handler)
app.router.add_put('/put', put_handler)
app.router.add_route('*', '/path', all_handler)
app.router.add_get('/get_without_head', get_without_head_handler, allow_head=False) # HEAD will response code 405

resource = app.router.add_resource('/resource', name='resource')
resource.add_route('GET', get_resource_handler)

variable_resource = app.router.add_resource('/variable_resource/{name:\d+}')
variable_resource.add_route('GET', variable_resource_handler)

web.run_app(app)