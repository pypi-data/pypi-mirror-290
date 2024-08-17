from src.datasolutions.sql.analytical import Analytical
from src.datasolutions.sql.transactional import Transactional


class Sql:
    def __init__(self, api_key: str):
        self.transactional = Transactional(api_key)
        self.analytical = Analytical(api_key)
