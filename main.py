from aiohttp import web
import aiohttp_jinja2
import jinja2
import os

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
    url_for = request.app.router.get('variable_resource').url_for(name='john_doe').with_query({'a': 'b'})
    return web.Response(text=f"Hello, {name}. Your url is {url_for}")

class Handler:

    def __init__(self):
        pass

    def handle_intro(self, request):
        return web.Response(text="Hello, world")

    async def handle_greeting(self, request):
        name = request.match_info.get('name', "Anonymous")
        txt = "Hello, {}".format(name)
        return web.Response(text=txt)

handler = Handler()

class ClassBasedView(web.View):
    async def get(self):
        return web.Response(text='HTTP GET: class based view')

    async def post(self):
        return web.Response(text='HTTP POST: class based view')

async def json_handler(request):
    data = {'some': 'data'}
    return web.json_response(data)

@aiohttp_jinja2.template('login.html')
async def get_login(request):
    return {}

async def post_login(request):
    data = await request.post()
    login = data['login']
    password = data['password']
    return web.json_response({
        'login': login,
        'password': password
    })

@aiohttp_jinja2.template('mp3_uploader.html')
async def get_mp3_handler(request):
    return {}

async def post_mp3_handler(request):

    reader = await request.multipart()

    # /!\ Don't forget to validate your inputs /!\

    # reader.next() will `yield` the fields of your form

    field = await reader.next()

    assert field.name == 'mp3'
    filename = field.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0

    BASE_DIR = os.path.dirname(__file__)
    MEDIA_PATH = 'media'
    with open(os.path.join(BASE_DIR, MEDIA_PATH, filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app.router.add_get('/', hello)
app.router.add_get('/get', get_handler)
app.router.add_post('/post', post_handler)
app.router.add_put('/put', put_handler)
app.router.add_route('*', '/path', all_handler)
app.router.add_get('/get_without_head', get_without_head_handler, allow_head=False) # HEAD will response code 405

resource = app.router.add_resource('/resource', name='resource')
resource.add_route('GET', get_resource_handler)

variable_resource = app.router.add_resource('/variable_resource/{name:\d+}', name='variable_resource')
variable_resource.add_route('GET', variable_resource_handler)

app.router.add_get('/intro', handler.handle_intro)
app.router.add_get('/greet/{name}', handler.handle_greeting)

app.router.add_view('/cbv', ClassBasedView)

for resource in app.router.resources():
    print(resource)

for name, resource in app.router.named_resources().items():
    print(name, resource)

app.router.add_routes([
    web.get('/get_alt', get_handler),
    web.post('/post_alt', post_handler),
])

routes = web.RouteTableDef()

@routes.get('/handle_get')
async def handle_get(request):
    return web.Response(text="handle_get")


@routes.post('/handle_post')
async def handle_post(request):
    return web.Response(text="handle_post")

@routes.view("/handle_view")
class HandleView(web.View):

    async def get(self):
        return web.Response(text="handle_view_get")

    async def post(self):
        return web.Response(text="handle_view_post")

app.router.add_routes(routes)
app.router.add_get('/json_handler', json_handler)

login_resource = app.router.add_resource('/login', name='login')
login_resource.add_route('GET', get_login)
login_resource.add_route('POST', post_login)

mp3_uploader_resource = app.router.add_resource('/mp3_uploader', name='mp3_uploader')
mp3_uploader_resource.add_route('GET', get_mp3_handler)
mp3_uploader_resource.add_route('POST', post_mp3_handler)

web.run_app(app)