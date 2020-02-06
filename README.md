# dnsmasq analyzer
Analyses dnsmasq logs and prints out some useful information 

## Note
The dnsmasq.conf file has to have 'log-queries=extra' and 'log-facility' as an enabled option in the conf file (and dnsmasq restarted) in order to get the correct info from the log file.
The script parses the $log file and outputs some dicts in json format (easier reading). 

## Structures
There are two main dictionaries used for keeping the data: ```did``` and ```request```. I created two structures/dictionaries because it was a little easier to see the data in different ways. I could use ```did``` and grab all stats from that dict to create the same thing as ```request``` but meh.

```did``` is sorted by all the dns ids from the dnsmasq log file. Each ```did``` dictionary entry is:

```did:```

    { 'dns_id': {
            'query_host': string, the host that the IP has asked dns to look up
            'query_ip': string, the IP that sent the query
            'reply': {  
                      'qr': string, the 'query response'. Could be one of 'cached', 'forwarded', 'reply'.
                      'reply_host': string, the host that was returned from the DNS in the reply.
                      'reply_ip': string, the IP that was reolved and returned back in the response/reply.
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
