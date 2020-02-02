# dnsmasq analyzer
Analyses dnsmasq logs and prints out some useful information 

## Note
The dnsmasq.conf file has to have 'log-queries=extra' and 'log-facility' as an enabled option in the conf file (and dnsmasq restarted) in order to get the correct info from the log file.

## Command Line Options:

<code>dnsmasq-analyzer [-d | --date]</code> Pass a date in format 'Jan 25' if you want to search for results on this date.
