from sanic import Sanic
from sanic import response
from jinja2 import Environment, PackageLoader, select_autoescape

import sys, os
import datetime
# Enabling async template execution which allows you to take advantage
# of newer Python features requires Python 3.6 or later.

ROOT_DIR = "./images"

app = Sanic(__name__)

# Load the template environment with async support
template_env = Environment(
    loader=PackageLoader('static','templates'),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)
app.static('/images', './images')

# Load the template from file
template = template_env.get_template("index.html")


def list_files():
    images = [filename for filename in os.listdir(ROOT_DIR) if filename.endswith('png') or filename.endswith('jpg')]
    images = sorted(images, reverse=True)
    images = [(datetime.datetime.fromtimestamp(float(image.split('.', 1)[0])/1000).strftime('%c'), image) for image in images]
    return images

@app.route('/')
async def test(request):
    images = list_files()
    rendered_template = await template.render_async(
        images=images,
        url_for=app.url_for)
    return response.html(rendered_template)


app.run(host="0.0.0.0", port=8666, debug=True)