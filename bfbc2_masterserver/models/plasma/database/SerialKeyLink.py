from sqlmodel import Field, SQLModel


class SerialKeyLink(SQLModel, table=True):
    serial_id: int = Field(default=None, foreign_key="serialkey.id", primary_key=True)
    target_id: int = Field(
        default=None, foreign_key="serialkeytarget.id", primary_key=True
    )
