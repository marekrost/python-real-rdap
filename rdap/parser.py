import model


class RdapParserInterface:
    def parse_link(self, data) -> model.Link:
        pass
