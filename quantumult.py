import os

from scripts import adblock, gfwlist

proxy_list = gfwlist.update_list()
proxy_rules = gfwlist.filter_list(proxy_list)
gfwlist.convert_to_rule(proxy_rules, 'host-suffix, ',
                        'host-keyword, ', 'ip-cidr, ', ', proxy')

with open(os.path.split(os.path.realpath(__file__))[0] + '/rules/quantumult_proxy.list', 'w') as f:
    f.write('\n'.join(proxy_rules))

adblock_list = adblock.update_list()
adblock_rules = adblock.filter_list(adblock_list)
adblock.convert_to_rule(adblock_rules, 'host-suffix, ',
                        'host-keyword, ', 'ip-cidr, ', ', reject')
with open(os.path.split(os.path.realpath(__file__))[0] + '/rules/quantumult_reject.list', 'w') as f:
    f.write('\n'.join(adblock_rules))
