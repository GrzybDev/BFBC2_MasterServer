from pydantic import BaseModel


class DomainPartition(BaseModel):
    domain: str
    subDomain: str
