import requests
import json
import urllib3.util
import rdap.model


class RdapClient:
    def __init__(self):
        self.__bootstrap()

    def __bootstrap(self):
        authority_list = RdapClient.__get_data('https://data.iana.org/rdap/dns.json')
        self.authorities = {}
        for authority in authority_list['services']:
            for tld in authority[0]:
                self.authorities[tld] = authority[1][0]

    @staticmethod
    def __get_data(uri: str):
        data_response = requests.get(uri)
        data_content = data_response.content.decode('utf8')
        if data_response.status_code != 200:
            raise RuntimeError("RDAP [{0}] returned status {1}. Response content: {2}".format(
                uri, data_response.status_code, data_content))
        return json.loads(data_content)

    def get_domain(self, domain):
        tld = urllib3.util.parse_url(domain).host.split('.')[-1]
        try:
            authority = self.authorities[tld]
        except Exception as e:
            print(e)

        data = RdapClient.__get_data(authority + '/domain/' + domain)
        domain = rdap.model.Domain.parse(data)

        # get more relevant data if such link exists
        rel_links = [link for link in domain.links if 'related' in link.rel]
        if rel_links:
            data = RdapClient.__get_data(rel_links[0].href)
            domain = rdap.model.Domain.parse(data)

        return domain
