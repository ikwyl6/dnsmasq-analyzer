#!/bin/python

# Little analyzer for dnsmasq logs. 
# Author: ikwyl6@protonmail.com
# 'log-queries=extra' and 'log-facility' need to 
# be set in the dnsmasq.conf file for this script to get all info
# and properly work.

import argparse, os, re, subprocess, json, time, mmap
from collections import Counter, OrderedDict
from datetime import date

#log = "/tmp/dnsmasq.log"
#log = "/var/log/dnsmasq/dnsmasq.log"
log = "/tmp/dnsmasq.log.1"
log_ = "/tmp/dnsmasq.log.sorted"
log_g = "/tmp/dnsmasq.log.grep"
dt = date.today().strftime("%b %d") # default if no date given
# 1,2,3:date with time, 4:process+pid, 5:id, 6:ip, 7: dns query/reply or resolve file, 8: ip4/ip6, 9:hostname
dnsmasq_regex = r'^(\w+)\ (\d+)\ (\d{2}:\d{2}:\d{2})\ (\w+\[[0-9]+\]:)\ (\d+)\ (\d+\.\d+\.\d+\.\d+)\/\d+\ ([\w/.]+)(\[(PTR|SOA|MX|A+)\])?\ (\w+[-\w.]+)\ (is|from|to)\ (.*)$'
request = {} # dict sorted by IP with all requests
did = {} # dict of all dns_id

# Sort file by id for easier processing
# https://stackoverflow.com/questions/8902206/subprocess-popen-io-redirect
def sort_logfile(inlog,outlog):
    st = time.time()
    with open(outlog,'w') as f:
        s = subprocess.Popen(["sort", "-k5", inlog],stdout=f)
        s.communicate()
    print("sort_logfile: --- %s seconds ---" % (time.time() - st))

# mmap atleast twice as fast as subprocess(grep) - thanks stackexchange
def grep_mmap(inlog,outlog,pattern):
    st = time.time()
    ol = open(outlog, "a")
    pattern = pattern.encode("utf-8") # needed for mmap searching and bytes compare
    with open(inlog, "r") as f: #, encoding="utf-8") as f:
        s = re.search(pattern, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ))
        if (s): 
            ol.write(str(s.group(0)))
    ol.close()
    print("grep_mmap: --- %s seconds ---" % (time.time() - st))

# Use subprocess(grep) to grep it out 
def grep_date(inlog,outlog,dt):
    st = time.time()
    with open(outlog, 'w') as f:
        s = subprocess.Popen(["grep", dt, inlog],stdout=f)
        s.communicate()
    print("grep_date: --- %s seconds ---" % (time.time() - st))

# maybe read and search file from bottom up? 
#with open(log_, 'r') as f:
#print(f.read()[::-1])

clp = argparse.ArgumentParser(prog='dns-stats', description='A little dnsmasq log parser')
clp.add_argument('-d', '--date', help='Pass a date \'Jan 25\' to script. Default is today\'s date')
clargs = clp.parse_args()

if (clargs.date): 
    # TODO: check that clp.date is right format
    # 
    dt = clargs.date

#grep_date(log,log_g, dt)
grep_mmap(log,log_g, dt)
sort_logfile(log_g,log_)
#dnsmasq_regex = dnsmasq_regex.encode("utf-8")
with open(log_, 'r') as f:
    for line in f:
        #print (line)
        m = re.search(dnsmasq_regex, line, re.MULTILINE)
        #m = re.search(dnsmasq_regex, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ))
        try: 
            (line_date, dns_id, ip, qtype, q_flag, host, ip_reply) = (m.group(1) + " " + m.group(2), m.group(5), m.group(6), m.group(7), m.group(8), m.group(10), m.group(12))
        except AttributeError as e:
            print ("error: " + str(e) + "\nline: " + line)
            continue
        if (line_date == dt):
            # sort by dns_id
            if dns_id not in did:
                # If not in the dict, initialize
                did.update({dns_id: {'query_host': host,
                    'query_ip': ip,
                    'reply': {} }})
            if (qtype != "query"):
                reply_key = len(did[dns_id]['reply']) + 1
                did[dns_id]['reply'][reply_key] = {'qr': qtype, 'reply_host': host, 'reply_ip': ip_reply}
            # Keep stats on queries themselves
            if (qtype == "query"):
                # If not in the dict, initialize
                if ip not in request:
                    request.update({ip: {'query_count': Counter(), 
                        'q_flag': Counter(),
                        'host': Counter()}})
                request[ip]['query_count'].update([qtype])
                request[ip]['q_flag'].update([q_flag])
                request[ip]['host'].update([host])

for i in request:
    request[i]['host'] = OrderedDict(request[i]['host'].most_common())


#print (json.dumps(did, indent=2))
print (json.dumps(request, indent=2))

