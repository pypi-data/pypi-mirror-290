from DataSolutions.sql.analytical import Analytical
from DataSolutions.sql.transactional import Transactional


class Sql:
    def __init__(self, api_key: str):
        self.transactional = Transactional(api_key)
        self.analytical = Analytical(api_key)
