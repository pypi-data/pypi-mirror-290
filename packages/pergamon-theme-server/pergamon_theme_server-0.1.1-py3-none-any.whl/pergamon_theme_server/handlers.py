from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.write("""
            body {
                background-color: #0A1121;
                color: white;
            }
            #header {
                background-color: #0A1121;
            }
            .btn {
                background: #2BCCE4;
                border-color: #2BCCE4;
                color: white;
            }
            .btn:hover {
                background: #2BCCE4;
                border-color: #2BCCE4;
            }
            .rendered_html {
                display: none;
            }
        """)


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, '/customcss')
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)