#!/usr/bin/env python
#-*- coding:utf8 -*-
# Desgin By Xiaok
from xk_application.xk_main import *
import platform,os,sys,math

class IndexHandler(BaseHandler):
    DEFAULT_UNIT = 1024

    def get_hostname(self):
        h = os.popen("hostname")
        return h.read().strip()

    def get_uptime(self):
        f = open('/proc/uptime','r')
        r = f.read()
        u = r.split()
        f.close()
        uptime = self.format_seconds(int(float(u[0])))
        cpu_num = os.popen("cat /proc/cpuinfo  | grep processor | wc -l")
        cpu_num = int(cpu_num.read().strip())
        free = int(float(u[1])) * 100 / (int(float(u[0]))*cpu_num)
        uptime['free'] = free
        return uptime

    def get_ip(self):
        r = os.popen("ip a | grep inet | grep -Ev 'inet6|127.0.0.1' | awk -F'[ /]+' '{print $3}'")
        r = r.read()
        ip = r.split()
        if len(ip) > 1:
            ip = ', '.join(ip)
        else:
            ip = ip[0]
        return ip

    def get_load(self):
        f = open('/proc/loadavg')
        l = f.read().split()
        f.close()
        loadavg_1 = l[0]
        loadavg_5 = l[1]
        loadavg_15 = l[2]
        return [loadavg_1,loadavg_5,loadavg_15]

    def get_mem(self):
        f = open('/proc/meminfo')
        m = f.readlines()
        f.close()
        mem = {}
        for n in m:
            if len(n) < 2 : continue
            name = n.split(':')[0]
            var = n.split()[1]
            mem[name] = int(var) * self.DEFAULT_UNIT
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        MemUsedPercent = mem['MemUsed'] * 100 / mem['MemTotal']
        mem['MemUsedPercent'] = MemUsedPercent
        return mem

    def get_hdd(self):
        d = os.statvfs('/')
        all = d.f_frsize * d.f_blocks
        free = d.f_frsize * d.f_bavail
        used = ( d.f_blocks - d.f_bavail ) * d.f_frsize
        usedPercent = ( d.f_blocks - d.f_bavail ) * 100 / d.f_blocks
        return {"all":all, "free":free, "used":used, "usedPercent":usedPercent}

    def net_stat(self):
        net = {}
        f = open("/proc/net/dev")
        lines = f.readlines()
        f.close()
        i = 1
        for line in lines:
            if i < 3 :
               i += 1
               continue
            con = line.split(':')
            name = con[0].split()[0]
            var = con[1].split()
            net[name] = var
            i += 1
        net_in = 0
        net_out = 0
        for i in net:
            if i == 'lo':continue
            net_in += int(net[i][0])
            net_out += int(net[i][8])
        #net_in = net_in / 1024 / 1024
        #net_out = net_out / 1024 /1024
        return {"in":net_in,"out":net_out}

    def get_os_version(self):
        OS = platform.linux_distribution()
        os_arch = platform.machine()
        if 'Red Hat Enterprise Linux Server' in OS:
            os_name = 'RHEL'
        else:
            os_name = OS[0]
        os_version = OS[1]
        return "%s %s %s" % ( os_name,os_version,os_arch)

    def get_dnsmasq(self):
        status = os.system("/etc/init.d/dnsmasq status")
        v1 = os.popen("dnsmasq --version | head -1 | awk '{print $3}'")
        version = v1.read().strip()
        return {"version":version, "status":status}

    def get_cpuinfo(self):
        '''
        http://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
        read in cpu information from file
        The meanings of the columns are as follows, from left to right:
            0cpuid: number of cpu
            1user: normal processes executing in user mode
            2nice: niced processes executing in user mode
            3system: processes executing in kernel mode
            4idle: twiddling thumbs
            5iowait: waiting for I/O to complete
            6irq: servicing inte   def getcpuload(self):

        #the formulas from htop 
             user    nice   system  idle      iowait irq   softirq  steal  guest  guest_nice
        cpu  74608   2520   24433   1117073   6176   4054  0        0      0      0

        Idle=idle+iowait
        NonIdle=user+nice+system+irq+softirq+steal
        Total=Idle+NonIdle # first line of file for all cpus

        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
        '''
        cpu_infos = {} #collect here the information
        with open('/proc/stat','r') as f_stat:
            lines = [line.split(' ') for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

        #compute for every cpu
        
        for cpu_line in lines:
            if '' in cpu_line: cpu_line.remove('')#remove empty elements
            cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
            cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

            Idle=idle+iowait
            NonIdle=user+nice+system+irq+softrig+steal

            Total=Idle+NonIdle
            #update dictionionary
            cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
        return cpu_infos

    def get_cpu(self):
        cpu_infos = self.get_cpuinfo()
        Total = 0
        Idle = 0
        for cpu in cpu_infos:
            Total += cpu_infos[cpu]['total']
            Idle += cpu_infos[cpu]['idle']
        return (math.ceil((((Total-Idle)/Total)*100)*100))/100

    @Auth
    def get(self):
        #print self.get_login_url()
        #print self.current_user
        #print self.user_info()
        data = {
            "uptime":self.get_uptime(),
            "ip":self.get_ip(),
            "net":self.net_stat(),
            "mem":self.get_mem(),
            "load":self.get_load(),
            "os":self.get_os_version(),
            "hdd":self.get_hdd(),
            "dnsmasq":self.get_dnsmasq(),
            "hostname":self.get_hostname(),
            "cpu":self.get_cpu()
        }
        #print data
        self.render2("xk_index.html",dashboard="active",data=data)
