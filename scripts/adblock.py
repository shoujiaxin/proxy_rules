import re
import time
import urllib.request


def update_list():
    print('Loading EasyList China & EasyList...')

    url = 'https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    adblocklist = response.read().decode().split('\n')

    print('Update EasyList China & EasyList successfully')
    return adblocklist


def filter_list(adblocklist):
    rules = ["# Last Modified: " + time.asctime()]

    for line in adblocklist[1:]:
        if line == '':  # Blank lines
            continue
        elif line.startswith('!'):  # Comments
            continue
        elif line.startswith('$'):
            continue
        elif line.startswith('@@'):  # Exception rules
            continue
        elif line.startswith('##'):
            continue
        else:
            line = re.sub(r'^\|?https?://', '', line)
            line = re.sub(r'^\|\|', '', line)
            line = line.lstrip('.*')

            line = line.rstrip('/^*')
            line = re.sub(r':\d{2,5}$', '', line)  # Remove port

            # Only IPs and domains
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', line) or re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,9}$', line):
                rules.append(line)

    # Remove exception rules to avoid mistakes
    for line in adblocklist:
        if line.startswith('@@'):
            i = 0
            while i < len(rules):
                if rules[i] in line:
                    del rules[i]
                else:
                    i = i + 1

    rules = list(set(rules))
    rules.sort()
    return rules


def convert_to_rule(rules, rule_domain_prefix, rule_keyword_prefix, rule_ip_prefix, rule_suffix):
    for i in range(1, len(rules)):
        # IP
        if re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', rules[i]):
            rules[i] = rule_ip_prefix + rules[i] + '/32'
        # Domain
        elif '.' in rules[i]:
            rules[i] = rule_domain_prefix + rules[i]
        # Keyword
        else:
            rules[i] = rule_keyword_prefix + rules[i]
        rules[i] += rule_suffix
    print(str(len(rules) - 1) + ' rules converted')
