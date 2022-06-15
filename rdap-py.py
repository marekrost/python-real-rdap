import rdap.client

if __name__ == "__main__":
    client = rdap.client.RdapClient()
    domain = client.get_domain('wordpress.com')

    print(domain)
