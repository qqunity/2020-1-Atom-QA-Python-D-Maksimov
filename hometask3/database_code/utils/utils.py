import numpy as np


def get_uniq_ip_addresses(req):
    ip_addresses = list(map(lambda ip_address: ip_address.replace(ip_address, ip_address.split()[0]), req))
    u_ip_addresses = list(np.unique(np.array(ip_addresses)))
    return u_ip_addresses


def get_uniq_urls(req):
    urls = list(map(lambda url: url.replace(url, url.split()[6]), req))
    u_urls = list(np.unique(np.array(urls)))
    return u_urls
