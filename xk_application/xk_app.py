#!/usr/bin/env python
#-*- coding:utf8 -*-
# Desgin By Xiaok
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.netutil
import tornado.process
import time
from xk_config.xk_setting import *
from xk_config.xk_url import *
from tornadobabel import locale
from tornadobabel.mixin import TornadoBabelMixin

MainSetting = dict(
    template_path = 'xk_html',
    static_path = 'xk_static',
    static_url_prefix = '/xk_static/',
    xsrf_cookies = False,
    cookie_secret = "db884468559f4c432bf1c1775f3dc9da",
    login_url = "/login",
    debug = options.debug,
    autoreload = options.debug,
)

class HttpApplication(tornado.web.Application):
    MYSQL_POLL_FREQUENCY = 3 * 60 * 1000

    def __init__(self):
        handlers = HandlersURL
        settings = MainSetting
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password,
            time_zone=options.timezone,charset='utf8')

        ping_db = lambda: self.db.query("select now()")
        tornado.ioloop.PeriodicCallback(ping_db,self.MYSQL_POLL_FREQUENCY).start()

class ProfileHandler(TornadoBabelMixin, tornado.web.RequestHandler):
    def get_user_locale(self):
        if self.current_user:
            return locale.get(self.current_user.locale)

        # Fallback to browser based locale detection
        return self.get_browser_locale()

def main():
    if options.ipv6:
        host = None
    else:
        host = "0.0.0.0"
    tornado.options.parse_command_line()
    locale.load_gettext_translations('translations', 'messages')

    if options.debug:
        http_server = tornado.httpserver.HTTPServer(request_callback=HttpApplication(),xheaders=True)
        http_server.listen(options.port,host)
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print '[%s] Listen On Port %s' % ( now, options.port )
    else:
        http_sockets = tornado.netutil.bind_sockets(options.port,host)
        tornado.process.fork_processes(num_processes=options.processes)
        http_server = tornado.httpserver.HTTPServer(request_callback=HttpApplication(),xheaders=True)
        http_server.add_sockets(http_sockets)

    tornado.ioloop.IOLoop.instance().start()
