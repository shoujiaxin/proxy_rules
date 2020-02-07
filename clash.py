import os

from scripts import adblock, gfwlist

proxy_list = gfwlist.update_list()
proxy_rules = gfwlist.filter_list(proxy_list)
gfwlist.convert_to_rule(proxy_rules, '  - DOMAIN-SUFFIX,',
                        '  - DOMAIN-KEYWORD,', '  - IP-CIDR,', ',Proxy')

with open(os.path.split(os.path.realpath(__file__))[0] + '/rules/clash_proxy.list', 'w') as f:
    f.write('\n'.join(proxy_rules))

adblock_list = adblock.update_list()
adblock_rules = adblock.filter_list(adblock_list)
adblock.convert_to_rule(adblock_rules, '  - DOMAIN-SUFFIX,',
                        '  - DOMAIN-KEYWORD,', '  - IP-CIDR,', ',REJECT')
with open(os.path.split(os.path.realpath(__file__))[0] + '/rules/clash_reject.list', 'w') as f:
    f.write('\n'.join(adblock_rules))
