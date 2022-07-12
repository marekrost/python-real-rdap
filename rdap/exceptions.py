class RdapException(Exception):
    pass


class RdapError(Exception):
    def __init__(self, error_code: int, title: str, description: list):
        self.error_code = error_code
        self.title = title
        self.description = description

    @staticmethod
    def parse(data: dict):
        return RdapError(error_code=int(data['errorCode']), title=data['title'], description=data['description'])
