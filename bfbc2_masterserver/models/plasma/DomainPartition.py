from pydantic import BaseModel


class DomainPartition(BaseModel):
    """
    The DomainPartition class is a subclass of the BaseModel class from the Pydantic library.

    This class represents a domain partition with a domain and a subdomain.

    Attributes:
        domain (str): The main domain.
        subDomain (str): The subdomain.
    """

    domain: str
    subDomain: str
