# -*- coding: utf-8 -*-
import os, sys, platform, json, requests, psutil, time
from flask import request
c0 , c1 , c2 , c3 , c4 , c5 = 0, 0, 0, 0, 0, 0
r0 , r1 , r2 , r3 , r4 , r5 = 0, 0, 0, 0, 0, 0
s0 , s1 , s2 , s3 , s4 , s5 = 0, 0, 0, 0, 0, 0
rxa, txa = 0, 0
tim = time.time()

def get_static_info():

    print("Gathering system information...")

    # OS Linux distribution family
    osDist = platform.linux_distribution()[0].lower()
    osFamily = ''
    if osDist == 'debian' or osDist == 'ubuntu' or osDist == 'kali' or osDist == 'raspbian':
        osFamily = 'debian'
    elif osDist == 'redhat' or osDist == 'redhat linux' or osDist == 'centos linux' or osDist == 'centos':
        osFamily = 'redhat'
    print("osDist=", osDist)
    print("osFamily=", osFamily)

    # OS full distribution
    rFullDist = os.popen('lsb_release -ds')
    osFullDist = rFullDist.read().strip('\n')
    rFullDist.close()
    print("osFullDist=", osFullDist)

    # OS short version
    osVer = ''
    if osDist == 'centos linux' or osDist == 'centos':
        rVer = os.popen('grep -oE  "[0-9.]+" /etc/redhat-release')
        osVer = rVer.read().strip('\n')[0:1]
        rVer.close()
    elif osDist == 'debian':
        rVer = os.popen('grep -oE  "[0-9.]+" /etc/issue')
        osVer = rVer.read().strip('\n')[0:1]
        rVer.close()
    elif osDist == 'ubuntu':
        rVer = os.popen('lsb_release -r --short')
        osVer = rVer.read().strip('\n')[0:2]
        rVer.close()
    print("osVer=", osVer)

    # OS codename
    osCodename = 'none'
    if osDist == 'ubuntu':
        osCodename = platform.linux_distribution()[2]
    elif osDist == 'debian':
        rCodename = os.popen('lsb_release -ds | grep -Po "(?<=\()\S+(?=\))"')
        osCodename = rCodename.read().strip('\n')
        rCodename.close()
    print("osCodename=", osCodename)

    # OS virtualization technology
    rVirt = os.popen('virt-what')
    osVirt = rVirt.read().strip('\n')
    rVirt.close()
    print("osVirt=", osVirt)

    # OS full version
    osVersion = platform.linux_distribution()[1]
    print("osVersion=", osVersion)

    # OS kernal version
    osKernel = platform.uname()[2]
    print("osKernel=", osKernel)

    # OS hostname
    osHostname = platform.node()
    print("osHostname=", osHostname)

    # OS bit
    osBit = platform.architecture()[0]
    print("osBit=", osBit)

    # CPU name
    rCPU = os.popen("echo $( awk -F: '/model name/ {name=$2} END {print name}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//' )")
    cpuName = rCPU.read().strip('\n')
    rCPU.close()
    print("cpuName=", cpuName)

    # CPU arch
    cpuArch = platform.uname()[4]
    print("cpuArch=", cpuArch)

    # CPU cores
    rCores = os.popen("echo $( awk -F: '/model name/ {core++} END {print core}' /proc/cpuinfo )")
    cpuCores = rCores.read().strip('\n')
    rCores.close()
    print("cpuCores=", cpuCores)

    # CPU frequency
    rFreq = os.popen("echo $( awk -F: '/cpu MHz/ {freq=$2} END {print freq}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//' )")
    cpuFreq = rFreq.read().strip('\n')
    rFreq.close()
    print("cpuFreq=", cpuFreq)

    # CPU bogomips
    rBogo = os.popen('cat /proc/cpuinfo | grep "bogomips" | grep -o "[0-9]*\.[0-9]*" | head -1')
    cpuBogo = rBogo.read().strip('\n')
    rBogo.close()
    print("cpuBogo=", cpuBogo)

    # CPU L3 cache
    rCPUCache = os.popen('cat /proc/cpuinfo | grep "cache size" | grep -o "[0-9]*" | head -1')
    cpuCache = rCPUCache.read().strip('\n')
    rCPUCache.close()
    print("cpuCache=", cpuCache)

    # RAM frequency
    ramFreq = 0
    rRAMFreq = os.popen('dmidecode | grep "Max Speed" | grep -o "[0-9]*"')
    ramFreq = int(rRAMFreq.read().strip('\n'))
    rRAMFreq.close()
    print("ramFreq=", ramFreq)

    # RAM type
    ramType = "unknown"
    if 0 < ramFreq <= 400:
        ramType = "DDR"
    elif 500 < ramFreq <= 800:
        ramType = "DDR2"
    elif 1000 < ramFreq <= 1600:
        ramType = "DDR3"
    elif 2000 <= ramFreq:
        ramType = "DDR4"
    print("ramType=", ramType)

    # Write cache
    strDict = {
        'osdist': osDist,
        'osfamily': osFamily,
        'osfulldist': osFullDist,
        'osver': osVer,
        'oscodename': osCodename,
        'osvirt': osVirt,
        'osversion': osVersion,
        'oskernel': osKernel,
        'oshostname': osHostname,
        'osbit': osBit,
        'cpuname': cpuName,
        'cpuarch': cpuArch,
        'cpucores': cpuCores,
        'cpufreq': cpuFreq,
        'cpubogo': cpuBogo,
        'cpucache': cpuCache,
        'ramfreq': ramFreq,
        'ramtype': ramType
    }

    strConfigPath = '/usr/local/omniwrench/device.json'
    strConfigDir = os.path.dirname(strConfigPath)

    print("Saving to: ", strConfigDir)

    if not os.path.exists(strConfigDir):
        os.makedirs(strConfigDir)
    with open(strConfigPath, 'w') as f:
        json.dump(strDict, f, sort_keys=True, indent=4)

def get_ram_info():

    # RAM total
    rRAMTotal = os.popen('cat /proc/meminfo | grep "MemTotal" | grep -o "[0-9]*"')
    ramTotal = float("%.2f" % (int(rRAMTotal.read().strip('\n')) / 1024))
    rRAMTotal.close()

    # RAM Free
    rRAMFree = os.popen('cat /proc/meminfo | grep "MemFree" | grep -o "[0-9]*"')
    ramFree = float("%.2f" % (int(rRAMFree.read().strip('\n')) / 1024))
    rRAMFree.close()

    # RAM used
    ramUsed = float("%.2f" % (ramTotal - ramFree))

    # RAM cached
    rRAMCached = os.popen('cat /proc/meminfo | grep "Cached" | grep -o "[0-9]*" | head -1')
    ramCached = float("%.2f" % (int(rRAMCached.read().strip('\n')) / 1024))
    rRAMCached.close()

    # RAM buffers
    rRAMBuff = os.popen('cat /proc/meminfo | grep "Buffers" | grep -o "[0-9]*"')
    ramBuffers = float("%.2f" % (int(rRAMBuff.read().strip('\n')) / 1024))
    rRAMBuff.close()

    # RAM real used
    ramRealUsed = float("%.2f" % (ramTotal - ramFree - ramCached - ramBuffers))

    # RAM useable
    ramUsable = float("%.2f" % (ramTotal - ramRealUsed))

    # RAM useage percentage
    ramPercent = round(ramRealUsed / float(ramTotal) * 100, 2)
    global r5
    global r4
    global r3
    global r2
    global r1
    global r0
    r5 = r4
    r4 = r3
    r3 = r2
    r2 = r1
    r1 = r0
    r0 = ramPercent

    # Return
    strDict = {
        'total': ramTotal,
        'free': ramFree,
        'used': ramUsed,
        'cached': ramCached,
        'buffers': ramBuffers,
        'realused': ramRealUsed,
        'usable': ramUsable,
        'percent': ramPercent
    }
    return strDict

def get_swap_info():

    # Swap total
    swapTotal = 0
    rSwapTotal = os.popen('cat /proc/meminfo | grep "SwapTotal" | grep -o "[0-9]*"')
    swapTotal = float("%.2f" % (int(rSwapTotal.read().strip('\n')) / 1024))
    rSwapTotal.close()

    # Swap free
    swapFree = 0
    rSwapFree = os.popen('cat /proc/meminfo | grep "SwapFree" | grep -o "[0-9]*"')
    swapFree = float("%.2f" % (int(rSwapFree.read().strip('\n')) / 1024))
    rSwapFree.close()

    # Swap used
    swapUsed = float("%.2f" % (swapTotal - swapFree))

    # Swap usage percentage
    if swapTotal == 0:
        swapPercent = 0
    else:
        swapPercent = round(swapUsed / swapTotal * 100, 2)

    # Return
    strDict = {
        'total': swapTotal,
        'free': swapFree,
        'used': swapUsed,
        'percent': swapPercent
    }
    return strDict

def get_stroage_info():

    # Stroage name
    rStoName = os.popen('df | grep -o "/dev/[a-z]*[0-9]*" | head -1')
    stoName = rStoName.read().strip('\n')
    rStoName.close()

    # Stroage total
    rStoTotal = os.popen('df -m --output=source,size | grep "/dev/[a-z]*[0-9]*" | grep -o "[0-9]*\.*[0-9]*" | tail -1')
    stoTotal = "%.2f" % (int(rStoTotal.read().strip('\n')) / 1024 )
    rStoTotal.close()

    # Stroage used
    rStoUsed = os.popen('df -m --output=source,used | grep "/dev/[a-z]*[0-9]*" | grep -o "[0-9]*\.*[0-9]*" | tail -1')
    stoUsed = "%.2f" % (int(rStoUsed.read().strip('\n')) / 1024)
    rStoUsed.close()

    # Stroage available
    rStoFree = os.popen('df -m --output=source,avail | grep "/dev/[a-z]*[0-9]*" | grep -o "[0-9]*\.*[0-9]*" | tail -1')
    stoFree = "%.2f" % (int(rStoFree.read().strip('\n')) / 1024)
    rStoFree.close()

    # Stroage usage percentage
    rStoPercent = os.popen('df -m --output=source,pcent | grep "/dev/[a-z]*[0-9]*" | grep -o "[0-9]*" | tail -1')
    stoPercent = rStoPercent.read().strip('\n')
    rStoPercent.close()
    global s5
    global s4
    global s3
    global s2
    global s1
    global s0
    s5 = s4
    s4 = s3
    s3 = s2
    s2 = s1
    s1 = s0
    s0 = stoPercent

    # Return
    strDict = {
        'name': stoName,
        'total': stoTotal,
        'used': stoUsed,
        'free': stoFree,
        'percent': stoPercent
    }
    return strDict

def get_uptime():

    # Uptime
    rUptime = open("/proc/uptime")
    con = rUptime.read().split()
    rUptime.close()
    all_sec = float(con[0])
    MINUTE,HOUR,DAY = 60,3600,86400

    # Return
    strDict = {
        'days': int(all_sec / DAY ),
        'hours': int((all_sec % DAY) / HOUR),
        'minutes': int((all_sec % HOUR) / MINUTE)
    }
    return strDict

def get_local_ip():
    rIPLocal = os.popen('curl -s ip.cn | grep -o "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"')
    ipLocal = rIPLocal.read().strip('\n')
    rIPLocal.close()
    return ipLocal

def get_visitor_ip():
    return request.remote_addr

def get_ip_location():

    # IP location
    r = requests.get('http://freeapi.ipip.net/' + request.remote_addr)
    c = ""
    for s in r.json():
        c = c + s + " "

    return c

def get_cpu_percent():
    global c5
    global c4
    global c3
    global c2
    global c1
    global c0
    c5 = c4
    c4 = c3
    c3 = c2
    c2 = c1
    c1 = c0
    c0 = psutil.cpu_percent()
    return c0

def get_ram_percents():
    return {'content': [r5, r4, r3, r2, r1, r0]}

def get_cpu_percents():
    return {'content': [c5, c4, c3, c2, c1, c0]}

def get_stroage_percents():
    return {'content': [s5, s4, s3, s2, s1, s0]}

def get_net_info():

    # Probably network interface name
    rIf = os.popen('ls /sys/class/net | grep -v lo | head -1')
    iface = rIf.read().strip('\n')
    rIf.close()

    # Net info
    rNet = os.popen('cat /proc/net/dev | grep "%s"' % iface)
    s = (' '.join((rNet.read().strip('\n').split()))).split(' ')
    rNet.close()
    iface = s[0][0:-1]

    # Packets sent & recv
    rxp = s[2]
    txp = s[10]

    # Amount sent & recv
    rxb = int(s[1])
    txb = int(s[9])

    rx, tx = "", ""
    if 0 <= rxb < 1024:
        rx = str(rxb) + " B"
    elif 1024 <= rxb < 1024**2:
        rx = ("%.2f" % (rxb / 1024)) + " KB"
    elif 1024**2 <= rxb < 1024**3:
        rx = ("%.2f" % (rxb / 1024**2)) + " MB"
    else:
        rx = ("%.2f" % (rxb / 1024**3)) + " GB"

    if 0 <= txb < 1024:
        tx = str(txb) + " B"
    elif 1024 <= txb < 1024**2:
        tx = ("%.2f" % (txb / 1024)) + " KB"
    elif 1024**2 <= txb < 1024**3:
        tx = ("%.2f" % (txb / 1024**2)) + " MB"
    else:
        tx = ("%.2f" % (txb / 1024**3)) + " GB"

    # Average Speed
    global rxa
    global txa
    global tim
    timNow = time.time()
    rxd = (rxb - rxa) / (timNow - tim)
    txd = (txb - txa) / (timNow - tim)
    tim = time.time()
    rxs, txs = "", ""
    if rxa == 0 and txa == 0:
        rxa = rxb
        txa = txb
        rxs = "0 B/s"
        txs = "0 B/s"
    else:
        if 0 <= rxd < 1024:
            rxs = ("%.2f" % (rxd)) + " B/s"
        elif 1024 <= rxd < 1024**2:
            rxs = ("%.2f" % (rxd / 1024)) + " KB/s"
        elif 1024**2 <= rxd < 1024**3:
            rxs = ("%.2f" % (rxd / 1024**2)) + " MB/s"
        else:
            rxs = ("%.2f" % (rxd / 1024**3)) + " GB/s"

        if 0 <= txd < 1024:
            txs = ("%.2f" % (txd)) + " B/s"
        elif 1024 <= txd < 1024**2:
            txs = ("%.2f" % (txd / 1024)) + " KB/s"
        elif 1024**2 <= txd < 1024**3:
            txs = ("%.2f" % (txd / 1024**2)) + " MB/s"
        else:
            txs = ("%.2f" % (txd / 1024**3)) + " GB/s"

        rxa = rxb
        txa = txb

    # Return
    strDict = {
        'iface': iface,
        'rx': rx,
        'tx': tx,
        'rxs': rxs,
        'txs': txs,
        'rxp': rxp,
        'txp': txp
    }
    return strDict
