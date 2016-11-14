#!/usr/bin/env python
#-*- coding:utf8 -*-
# Desgin By Xiaok
from xk_application.xk_main import *

class LoginHandler(BaseHandler):
    def get(self,*args):
        if self.current_user:
            return self.redirect('/dashboard')
        self.render2("xk_login.html")

    def post(self,*args):
        username = self.get_argument('username')
        password = self.get_argument('password')
        remember = self.get_argument('remember','no')
        user = self.db.get('''select id,username,status from xk_users where username = %s and password = md5(%s)''',username,password)
        if user:
            if user['status'] == 'no':
                self.write('''<script type="text/javascript" >alert("''' + _("Users disabled, please contact the administrator!") + '''");history.go(-1);</script>''')
                return
        else:
            self.write('''<script type="text/javascript" >alert("''' + _("Wrong username or password!") + '''");history.go(-1);</script>''')
            return
        headers = self.request.headers
        login_host = self.request.remote_ip
        user_agent = headers.get('User-Agent')
        self.db.execute(''' insert into xk_login_logs (uid,username,login_host,user_agent) values (%s,%s,%s,%s) ''',user['id'],user['username'],login_host,user_agent)
        if remember == 'yes':
            expires = 30
        else:
            expires = None
        self.set_secure_cookie('xk_auth_token',username,expires_days=expires)
        referer_url = self.get_argument("next", "/dashboard")
        self.redirect(referer_url)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("xk_auth_token")
        self. redirect(self.get_login_url())
