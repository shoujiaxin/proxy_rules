import base64
import re
import time
import urllib.request


def update_list():
    print('Loading GFWList...')

    url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    gfwlist = base64.b64decode(response.read().decode()).decode().split('\n')

    print('Update GFWList successfully')
    return gfwlist


def filter_list(gfwlist):
    rules = ["# Last Modified: " + time.asctime()]

    for line in gfwlist[1:]:
        if line == '':  # Blank lines
            continue
        elif line.startswith('!'):  # Comments
            continue
        elif line.startswith('@@'):  # Exception rules
            continue
        else:
            line = re.sub(r'^\|?https?://', '', line)
            line = re.sub(r'^\|\|', '', line)
            line = line.lstrip('.*')

            if '/' in line:
                line = line.split('/')[0]
            elif re.match(r'^\w+\*\.', line):
                line = re.sub(r'^\w+\*\.', '', line)

            if not re.match(r'^[\w.-]+$', line):
                print('Unrecognized rule:', line)
                continue

            rules.append(line)

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
