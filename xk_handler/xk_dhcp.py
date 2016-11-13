#!/usr/bin/python
#-*- coding:utf8 -*-
# Desgin By Xiaok
from xk_application.xk_main import *

class DhcpPoolHandler(BaseHandler):
    MAC_CONFLICTS_STR = "2"
    IP_CONFLICTS_STR = "3"

    @Auth
    def get(self):
        #
        dhcp_options = self.db.query('''select * from xk_options where type = "dhcp"''')
        dhcp = {}
        for i in dhcp_options:
            dhcp[i['name']] = i['value']
        self.render2("xk_dhcp_pool.html",dhcp=dhcp,dhcp_pool="active")

    @Auth
    def post(self):
        status = self.get_argument("status")
        range_start = self.get_argument("range_start")
        range_end = self.get_argument("range_end")
        netmask = self.get_argument("netmask")
        lease = self.get_argument("lease")
        router = self.get_argument("router")
        dns1 = self.get_argument("dns1")
        dns2 = self.get_argument("dns2")
        domain = self.get_argument("domain")
        ntp = self.get_argument("ntp",'')
        comment = self.get_argument("comment")
        #self.db.execute('''insert into xk_dhcp_pool ( name,range_start,range_end,netmask,router,dns1,dns2,domain,lease,comment )
        #    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',name,range_start,range_end,netmask,router,dns1,dns2,domain,lease,comment)
        self.db.execute('''
            insert into xk_options (name,value,comment) values
            ('xk_dhcp_status',%s,_("DHCP Enable")),
            ('xk_dhcp_pool_start',%s,_("DHCP address pool start address")),
            ('xk_dhcp_pool_stop',%s,_("DHCP address pool end address")),
            ('xk_dhcp_pool_netmask',%s,_("DHCP address pool subnet mask")),
            ('xk_dhcp_pool_lease',%s,_("DHCP lease")),
            ('xk_dhcp_pool_gw',%s,_("DHCP Default Gateway")),
            ('xk_dhcp_pool_dns1',%s,_("DHCP primary DNS server")),
            ('xk_dhcp_pool_dns2',%s,_("DHCP secondary DNS server")),
            ('xk_dhcp_pool_domain',%s,_("DHCP default domain")),
            ('xk_dhcp_pool_ntp',%s,_("DHCP server time")),
            ('xk_dhcp_pool_comment',%s,_("DHCP address pool comments"))
            ON DUPLICATE KEY UPDATE name=values(name),value=values(value),comment=values(comment)
         ''',status,range_start,range_end,netmask,lease,router,dns1,dns2,domain,ntp,comment)
        self.write("1")

class DhcpHostHandler(BaseHandler):
    @Auth
    def get(self):
        dhcp_hosts = self.db.query("select *,case when action = 'allow' then 'selected' else '' end as allow_selected, case when action = 'ignore' then  'selected' else '' end as ignore_selected from xk_dhcp_host")
        self.render2("xk_dhcp_host.html",dhcp_hosts=dhcp_hosts,dhcp_pool="active")

    @Auth
    def post(self):
        hostname = self.get_argument("hostname")
        mac = self.get_argument("mac")
        ip = self.get_argument("ip")
        action = self.get_argument("action")
        comment = self.get_argument("comment")
        fun = self.get_argument("fun","add")
        id_ = self.get_argument("id",0) # For Edit
        sql_mac = "select id,mac from xk_dhcp_host where mac = '%s'" % mac.lower()
        sql_ip = "select id,ip from xk_dhcp_host where ip = '%s'" % ip
        if fun == "edit":
            sql = " and id != %s" % id_
            sql_mac += sql
            sql_ip += sql
        check_mac = self.db.query(sql_mac)
        check_ip = self.db.query(sql_ip)
        if check_mac:
            self.write(MAC_CONFLICTS_STR)
            return
        if check_ip:
            self.write(IP_CONFLICTS_STR)
            return
        if fun == "add":
            self.db.execute(" insert into xk_dhcp_host (hostname,mac,ip,action,comment) values (%s,%s,%s,%s,%s) ",hostname,mac.lower(),ip,action,comment)
        else: # For Edit
            self.db.execute("update xk_dhcp_host set hostname = %s, mac = %s, ip = %s, action = %s, comment = %s where id = %s",hostname,mac,ip,action,comment,id_)
        self.write("1")

