import requests


class Fullhunt:

    api_key = ''
    session = None

    def domain(self, domain: str) -> dict:
        url = f'https://fullhunt.io/api/v1/domain/{domain}/details'
        response = self.session.get(url)
        return response.json()

    def subdomains(self, domain: str) -> dict:
        url = f'https://fullhunt.io/api/v1/domain/{domain}/subdomains'
        response = self.session.get(url)
        return response.json()

    def search(self, query: dict) -> dict:
        # https://fullhunt.io/docs/global-search/filters
        url = f'https://fullhunt.io/api/v1/global/search'
        response = self.session.post(url, json=query)
        return response.json()

    def host(self, host: str) -> dict:
        url = f'https://fullhunt.io/api/v1/host/{host}'
        response = self.session.get(url)
        return response.json()

    def intelligence(self, domain: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/host?host={domain}'
        response = self.session.get(url)
        return response.json()

    def search_tag(self, tag: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/tag?tag={tag}'
        response = self.session.get(url)
        return response.json()

    def web_tech(self, technology: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/web-tech?tech={technology}'
        response = self.session.get(url)
        return response.json()

    def product(self, product: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/product?product={product}'
        response = self.session.get(url)
        return response.json()

    def intel_subdomains(self, subdomain: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/domain?domain={subdomain}'
        response = self.session.get(url)
        return response.json()

    def ip_to_hosts(self, ip: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/ip-to-hosts?ip={ip}'
        response = self.session.get(url)
        return response.json()

    def asn(self, asn: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/asn-to-hosts?asn={asn}'
        response = self.session.get(url)
        return response.json()

    def virt_asn(self, asn: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/asn-to-virtual-hosts?asn={asn}'
        response = self.session.get(url)
        return response.json()

    def hosts_in_range(self, ip_start: str, ip_end: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/ip-range-to-hosts?ip_start={ip_start}&ip_end={ip_end}'
        response = self.session.get(url)
        return response.json()

    def dns_mx(self, mx: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/dns-mx-to-hosts?dns_mx={mx}'
        response = self.session.get(url)
        return response.json()

    def dns_ns(self, ns: str) -> dict:
        url = f'https://fullhunt.io/api/v1/intel/dns-ns-to-hosts?dns_ns={ns}'
        response = self.session.get(url)
        return response.json()


class Session(Fullhunt):

    session = None

    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({'X-API-KEY': f'{api_key}'})


if __name__ == '__main__':
    pass
