#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, redirect
import util, os, json

app = Flask(__name__)
version = "1.0.0 Alpha"

# Make the WSGI interface available at the top level so wfastcgi can get it.
# wsgi_app = app.wsgi_app
@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():

    j = json.loads(open('/usr/local/omniwrench/device.json', 'r').read())
    cpuname = j.get('cpuname').strip()
    osfulldist = j.get('osfulldist').strip()
    oshostname = j.get('oshostname').strip()
    oskernel = j.get('oskernel').strip()

    ipvisitor = util.get_visitor_ip()

    return render_template('dashboard.html', cpuname=cpuname, osfulldist=osfulldist,
                           oshostname=oshostname, oskernel=oskernel, ipvisitor=ipvisitor)

@app.route('/resource')
def resource():
    j = json.loads(open('/usr/local/omniwrench/device.json', 'r').read())
    cpuname = j.get('cpuname').strip()
    cpucores = j.get('cpucores').strip()
    cpufreq = j.get('cpufreq').strip()
    cpucache = j.get('cpucache').strip()
    cpuarch = j.get('cpuarch').strip()
    cpubogo = j.get('cpubogo').strip()
    ramfreq = j.get('ramfreq')
    ramtype = j.get('ramtype').strip()
    noraminfo = 0
    if ramfreq==0:
        noraminfo = 1

    r = util.get_ram_info()
    ramtotal = r.get('total')
    ramused = r.get('used')
    ramrealused = r.get('realused')
    ramcached = r.get('cached')
    rambuffers = r.get('buffers')
    ramusable = r.get('usable')
    rampercent = r.get('percent')

    s = util.get_swap_info()
    swaptotal = s.get('total')
    swapused = s.get('used')
    swappercent = s.get('percent')
    noswap = 0
    if swaptotal==0:
        noswap = 1

    t = util.get_stroage_info()
    stoname = t.get('name')
    stototal = t.get('total')
    stoused = t.get('used')
    stofree = t.get('free')
    stopercent = t.get('percent')

    return render_template('resource.html', cpuname=cpuname, cpucores=cpucores,
                           cpufreq=cpufreq, cpucache=cpucache, cpuarch=cpuarch,
                           cpubogo=cpubogo, ramfreq=ramfreq, ramtype=ramtype,
                           noraminfo=noraminfo, ramtotal=ramtotal, ramused=ramused,
                           ramrealused=ramrealused, ramcached=ramcached,
                           rambuffers=rambuffers, ramusable=ramusable,
                           rampercent=rampercent, swaptotal=swaptotal,
                           swapused=swapused, swappercent=swappercent, noswap=noswap,
                           stoname=stoname, stototal=stototal, stoused=stoused,
                           stofree=stofree, stopercent=stopercent)

@app.route('/system')
def system():
    j = json.loads(open('/usr/local/omniwrench/device.json', 'r').read())
    osfulldist = j.get('osfulldist').strip()
    osfamily = j.get('osfamily').strip()
    osversion = j.get('osversion').strip()
    oscodename = j.get('oscodename').strip()
    osbit = j.get('osbit').strip()
    oskernel = j.get('oskernel').strip()
    oshostname = j.get('oshostname').strip()
    osvirt = j.get('osvirt').strip()
    return render_template('system.html', osfulldist=osfulldist, osfamily=osfamily,
                           osversion=osversion, oscodename=oscodename, osbit=osbit,
                           oskernel=oskernel, oshostname=oshostname, osvirt=osvirt)

@app.route('/network')
def network():
    return render_template('network.html')

@app.route('/about')
def about():
    pass

@app.route('/api/get_local_ip')
def get_local_ip():
    return jsonify({'content': util.get_local_ip()})

@app.route('/api/get_ip_location')
def get_ip_location():
    return jsonify({'content': util.get_ip_location()})

@app.route('/api/get_ram_info')
def get_ram_info():
    return jsonify(util.get_ram_info())

@app.route('/api/get_stroage_info')
def get_stroage_info():
    return jsonify(util.get_stroage_info())

@app.route('/api/get_uptime')
def get_uptime():
    return jsonify(util.get_uptime())

@app.route('/api/get_cpu_percent')
def get_cpu_percent():
    return jsonify({'content': util.get_cpu_percent()})

@app.route('/api/get_cpu_percents')
def get_cpu_percents():
    return jsonify(util.get_cpu_percents())

@app.route('/api/get_ram_percents')
def get_ram_percents():
    return jsonify(util.get_ram_percents())

@app.route('/api/get_stroage_percents')
def get_stroage_percents():
    return jsonify(util.get_stroage_percents())

@app.route('/api/get_net_info')
def get_net_info():
    return jsonify(util.get_net_info())

if __name__ == '__main__':

    # Check for device info cache
    strConfigDir = "/usr/local/omniwrench"
    if not os.path.exists(strConfigDir):
        util.get_static_info()

    # Run Manager
    app.run('0.0.0.0', 80)
