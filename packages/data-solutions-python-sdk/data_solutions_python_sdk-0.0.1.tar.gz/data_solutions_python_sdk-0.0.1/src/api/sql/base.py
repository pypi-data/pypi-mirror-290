from src.api.sql.analytical.base import Analytical
from src.api.sql.transactional.base import Transactional


class Sql:
    def __init__(self, api_key: str):
        self.transactional = Transactional(api_key)
        self.analytical = Analytical(api_key)
