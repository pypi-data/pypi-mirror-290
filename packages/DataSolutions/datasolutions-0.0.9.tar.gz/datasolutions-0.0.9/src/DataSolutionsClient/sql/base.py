from src.DataSolutionsClient.sql.analytical import Analytical
from src.DataSolutionsClient.sql.transactional import Transactional


class Sql:
    def __init__(self, api_key: str):
        self.transactional = Transactional(api_key)
        self.analytical = Analytical(api_key)
