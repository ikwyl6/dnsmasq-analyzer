# dnsmasq analyzer
Analyses dnsmasq logs and prints out some useful information 

## Note
The dnsmasq.conf file has to have 'log-queries=extra' and 'log-facility' as an enabled option in the conf file (and dnsmasq restarted) in order to get the correct info from the log file.
The script parses the $log file and outputs some dicts in json format (easier reading). 

## Structures
There are two main dictionaries used for keeping the data: ```did``` and ```request```.
```did``` is sorted by all the dns ids from the dnsmasq log file. Each ```did``` dictionary entry is:

```did:```

    { 'dns_id': {
                'query_host': string, the host that is dns is looking up
                'query_ip': string, the IP that sent the query
                'reply': {  
                          'qr': string, the 'query response'
                          'reply_host': string, the host that was in the reply.
                          'reply_ip': string, the IP that was returned back in the response/reply.
                          }
                }
    }

```request:```

    { 'ip': {
              'query_count': int, how many queries has IP sent to DNS server
              'q_flag': string, 'A', 'AAAA', 'SOA', 'PTR'
              'host': string, the hostname that the 'ip' requested.
             }
    }
## Command Line Options:

<code>dnsmasq-analyzer [-d | --date]</code> Pass a date in format 'Jan 25' if you want to search for results on this date.
