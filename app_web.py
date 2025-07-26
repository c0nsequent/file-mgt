from wsgiref.simple_server import make_server
from pathlib import Path
import urllib.parse
import clean_up_pictures as cl

found_pictures = []


def build_html(pictures):
    pics_html = '<br>'.join([Path(p).name for p in pictures]) if pictures else 'No pictures found'
    template = f"""
    <html>
    <head>
        <title>Cleaner Folders Web</title>
    </head>
    <body>
        <h1>Cleaner Folders</h1>
        <form method='post'>
            <label>Root Directory:<input type='text' name='root_dir'></label><br>
            <label><input type='checkbox' name='include_root'>Include underlying directories</label><br>
            <label>Target Directory:<input type='text' name='target_dir'></label><br>
            <label><input type='checkbox' name='sort'>Sort by date</label><br><br>
            <button type='submit' name='action' value='find'>Find Pictures</button>
            <button type='submit' name='action' value='move'>Move Pictures</button>
            <button type='submit' name='action' value='copy'>Copy Pictures</button>
        </form>
        <h2>Found Pictures ({len(pictures)})</h2>
        <div style='height:200px;overflow:auto;border:1px solid #000;'>{pics_html}</div>
    </body>
    </html>
    """
    return template


def app(environ, start_response):
    global found_pictures
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            length = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            length = 0
        body = environ['wsgi.input'].read(length).decode()
        data = urllib.parse.parse_qs(body)
        action = data.get('action', [''])[0]
        root_dir = data.get('root_dir', [''])[0]
        target_dir = data.get('target_dir', [''])[0]
        include_root = 'include_root' in data
        sort = 'sort' in data
        if action == 'find':
            found_pictures = cl.find_pictures(root_dir, root=include_root)
        elif action == 'move':
            cl.move_pictures(found_pictures, target_dir, sort=sort)
            found_pictures = []
        elif action == 'copy':
            cl.copy_pictures(found_pictures, target_dir, sort=sort)
            found_pictures = []
        start_response('303 See Other', [('Location', '/')])
        return [b'']
    else:
        html = build_html(found_pictures)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [html.encode()]


def run_server(port=8000):
    with make_server('', port, app) as httpd:
        print(f'Serving on port {port}...')
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
