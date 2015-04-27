import re
import string
import random

import requests
from flask.ext.script import Command, Option


class GunicornServer(Command):
    """Run the app within Gunicorn"""

    def __init__(self,app, host='127.0.0.1', port=8080, workers=4):
        self.port = port
        self.host = host
        self.workers = workers
        self.app = app

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
        )

    def run(self, host, port, workers):
        from gunicorn.app.base import Application

        app = self.app

        class FlaskApplication(Application):
            def init(self, parser, opts, args):
                return {
                    'bind': '{0}:{1}'.format(host, port),
                    'workers': workers
                }

            def load(self):
                return app

        FlaskApplication().run()


def generate_random_string(size=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in xrange(size))


def get_page_title(url):
    regex = re.compile('<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)

    try:
        page_content = requests.get(url).text
        title = regex.search(page_content).group(1)
        return title
    except requests.RequestException:
        return ""


def get_all_form_errors(form):
    """
    Return all the field errors from a form.

    Return value e.g. -

    {
        'username': ['This field is required'],
        'password': ['Password should be at least 6 characters']
    }

    """

    form_errors = {}

    for field, errors in form.errors.items():
        for error in errors:
            if not form_errors.get(field):
                form_errors[field] = []
            form_errors[field].append(error)

    return form_errors
