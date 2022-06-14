from dataclasses import dataclass


@dataclass
class Link:
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-4.2
    """
    href: str
    hreflang: list = None
    media: str = None
    rel: str = None
    title: str = None
    type: str = None
    value: str = None

    @staticmethod
    def parse(data: dict):
        return Link(
            href=data['href'],
            hreflang=data['hreflang'] if 'hreflang' in data else None,
            media=data['media'] if 'media' in data else None,
            rel=data['rel'] if 'rel' in data else None,
            title=data['title'] if 'title' in data else None,
            type=data['type'] if 'type' in data else None,
            value=data['value'] if 'value' in data else None)


@dataclass
class Notice:
    """
        Represents both Notice and Remark, since their type is identical
        https://datatracker.ietf.org/doc/html/rfc7483#section-4.3
    """
    description: list
    links: list = None
    title: str = None
    type: str = None

    @staticmethod
    def parse(data: dict):
        return Notice(
            description=data['description'],
            links=([Link.parse(link) for link in data['link']]) if 'links' in data else None,
            title=data['title'] if 'title' in data else None,
            type=data['type'] if 'type' in data else None)


@dataclass
class Event:
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-4.5
    """
    event_action: str
    event_date: str
    event_actor: str = None
    links: list = None

    @staticmethod
    def parse(data: dict):
        return Event(
            event_action=data['eventAction'],
            event_date=data['eventDate'],
            event_actor=data['eventActor'] if 'eventActor' in data else None,
            links=([Link.parse(link) for link in data['links']]) if 'links' in data else None)


@dataclass
class PublicId:
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-4.8
    """
    identifier: str
    type: str

    @staticmethod
    def parse(data: dict):
        return PublicId(
            identifier=data['identifier'],
            type=data['type'])


@dataclass
class IpAddresses:
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.2
    """
    v4: list
    v6: list

    @staticmethod
    def parse(data: dict):
        return IpAddresses(
            v4=data['v4'] if 'v4' in data else None,
            v6=data['v6'] if 'v6' in data else None)


@dataclass
class DsData:
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.3
        https://datatracker.ietf.org/doc/html/rfc7483#appendix-D
    """
    key_tag: int
    algorithm: int
    digest: str
    digest_type: str
    events: list = None
    links: list = None

    @staticmethod
    def parse(data: dict):
        return DsData(
            key_tag=int(data['keyTag']),
            algorithm=int(data['algorithm']),
            digest=data['digest'],
            digest_type=data['digestType'],
            events=([Event.parse(event) for event in data['events']]) if 'events' in data else None,
            links=([Link.parse(link) for link in data['links']]) if 'links' in data else None)


@dataclass
class KeyData:
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.3
        https://datatracker.ietf.org/doc/html/rfc7483#appendix-D
    """
    flags: int
    protocol: int
    public_key: str
    algorithm: str
    events: list = None,
    links: list = None

    @staticmethod
    def parse(data: dict):
        return KeyData(
            flags=int(data['flags']),
            protocol=int(data['protocol']),
            public_key=data['publicKey'],
            algorithm=data['algorithm'],
            events=([Event.parse(event) for event in data['events']]) if 'events' in data else None,
            links=([Link.parse(link) for link in data['links']]) if 'links' in data else None)


@dataclass
class SecureDns:
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.3
        https://datatracker.ietf.org/doc/html/rfc7483#appendix-D
    """
    zone_signed: bool = None
    delegation_signed: bool = None
    max_sig_life: int = None
    ds_data: DsData = None
    key_data: KeyData = None

    @staticmethod
    def parse(data: dict):
        return SecureDns(
            zone_signed=bool(data['zoneSigned']) if 'zoneSigned' in data else None,
            delegation_signed=bool(data['delegationSigned']) if 'delegationSigned' in data else None,
            max_sig_life=int(data['maxSigLife']) if 'maxSigLife' in data else None,
            ds_data=DsData.parse(data['dsData']) if 'dsData' in data else None,
            key_data=KeyData.parse(data['keyData']) if 'keyData' in data else None)


# Cannot apply dataclass due to possibly mandatory arguments in child classes
# Dataclass cannot generate such constructors properly with full list of arguments
class RdapObject:
    def __init__(self, object_class_name: str, entities: list = None, events: list = None, handle: str = None,
                 links: list = None, port43: str = None, notices: list = None, remarks: list = None,
                 status: str = None):
        self.object_class_name = object_class_name
        self.entities = entities
        self.events = events
        self.handle = handle
        self.links = links
        self.port43 = port43
        self.notices = notices
        self.remarks = remarks
        self.status = status

    def __tostring(self):
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        return f'{self.__class__.__name__}(' + f', '.join([f'{member}={getattr(self, member)}' for member in members]) \
               + f')'

    def __format__(self, format_spec):
        return self.__tostring()

    def __repr__(self):
        return self.__tostring()

    def __str__(self):
        return self.__tostring()

    @staticmethod
    def _parse_args(data: dict) -> dict:
        return {
            'object_class_name': data['objectClassName'],
            'entities': ([Entity.parse(entity) for entity in data['entities']]) if 'entities' in data else None,
            'events': ([Event.parse(event) for event in data['events']]) if 'events' in data else None,
            'handle': data['handle'] if 'handle' in data else None,
            'links': ([Link.parse(link) for link in data['links']]) if 'links' in data else None,
            'port43': data['port43'] if 'port43' in data else None,
            'remarks': ([Notice.parse(remark) for remark in data['remarks']]) if 'remarks' in data else None,
            'status': data['status'] if 'status' in data else None
        }


class Entity(RdapObject):
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.1
    """
    def __init__(self, vcard_array: list, roles: list, public_ids: list = None, networks: list = None,
                 autnums: list = None, **kwargs):
        super().__init__(**kwargs)
        self.vcard_array = vcard_array
        self.roles = roles
        self.public_ids = public_ids
        self.networks = networks
        self.autnums = autnums

    @staticmethod
    def parse(data: dict):
        parent_args = RdapObject._parse_args(data)
        return Entity(
            vcard_array=data['vcardArray'],
            roles=data['roles'],
            public_ids=([PublicId.parse(pid) for pid in data['publicIds']]) if 'publicIds' in data else None,
            networks=([IpNetwork.parse(network) for network in data['networks']]) if 'network' in data else None,
            autnums=([Autnum.parse(autnum) for autnum in data['autnums']]) if 'autnums' in data else None,
            **parent_args)


class NameServer(RdapObject):
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.2
    """

    def __init__(self, ldh_name: str, unicode_name: str = None, ip_addresses: IpAddresses = None, **kwargs):
        super().__init__(**kwargs)
        self.ldh_name = ldh_name
        self.unicode_name = unicode_name
        self.ip_addresses = ip_addresses

    @staticmethod
    def parse(data: dict):
        parent_args = RdapObject._parse_args(data)
        return NameServer(
            ldh_name=data['ldhName'],
            unicode_name=data['unicodeName'] if 'unicodeName' in data else None,
            ip_addresses=IpAddresses.parse(data['ipAddresses']) if 'ipAddresses' in data else None,
            **parent_args)


class Domain(RdapObject):
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.3
    """

    def __init__(self, ldh_name: str, nameservers: list, secure_dns: SecureDns, unicode_name: str = None,
                 variants: list = None, public_ids: list = None, network: str = None, **kwargs):
        super().__init__(**kwargs)
        self.ldh_name = ldh_name
        self.unicode_name = unicode_name
        self.variants = variants
        self.nameservers = nameservers
        self.secure_dns = secure_dns
        self.public_ids = public_ids
        self.network = network

    @staticmethod
    def parse(data: dict):
        parent_args = RdapObject._parse_args(data)
        return Domain(
            ldh_name=data['ldhName'],
            unicode_name=data['unicodeName'] if 'unicodeName' in data else None,
            variants=data['variants'] if 'variants' in data else None,
            nameservers=[NameServer.parse(ns) for ns in data['nameservers']],
            secure_dns=SecureDns.parse(data['secureDNS']),
            public_ids=([PublicId.parse(pid) for pid in data['publicIds']]) if 'publicIds' in data else None,
            network=IpNetwork.parse(data['network']) if 'network' in data else None,
            **parent_args)


class IpNetwork(RdapObject):
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.4
    """

    def __init__(self, start_address: str, end_address: str, ip_version: str, name: str, type: str, country: str,
                 parent_handle: str, **kwargs):
        super().__init__(**kwargs)
        self.start_address = start_address
        self.end_address = end_address
        self.ip_version = ip_version
        self.name = name
        self.type = type
        self.country = country
        self.parent_handle = parent_handle

    @staticmethod
    def parse(data: dict):
        parent_args = RdapObject._parse_args(data)
        return IpNetwork(
            start_address=data['startAddress'],
            end_address=data['endAddress'],
            ip_version=data['ipVersion'],
            name=data['name'],
            type=data['type'],
            country=data['country'],
            parent_handle=data['parentHandle'],
            **parent_args)


class Autnum(RdapObject):
    """
        https://datatracker.ietf.org/doc/html/rfc7483#section-5.5
    """

    def __init__(self, start_autnum: int, end_autnum: int, name: str, type: str, country: str, **kwargs):
        super().__init__(**kwargs)
        self.start_autnum = start_autnum
        self.end_autnum = end_autnum
        self.name = name
        self.type = type
        self.country = country

    @staticmethod
    def parse(data: dict):
        parent_args = RdapObject._parse_args(data)
        return Autnum(
            start_autnum=int(data['startAutnum']),
            end_autnum=int(data['endAutnum']),
            name=data['name'],
            type=data['type'],
            country=data['country'],
            **parent_args)
