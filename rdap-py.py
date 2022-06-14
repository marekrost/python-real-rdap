import rdap.client
import pprint

client = rdap.client.RdapClient()

domain = client.get_domain('wordpress.com')

print(domain.handle)
print(domain)
