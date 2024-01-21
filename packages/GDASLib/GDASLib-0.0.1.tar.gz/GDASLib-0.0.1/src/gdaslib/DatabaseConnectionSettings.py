from dataclasses import dataclass

@dataclass
class DatabaseConnectionSettings:
    """ parameters to connect to the database """
    host: str
    database: str
    user: str
    password: str