from pydantic import BaseModel, ConfigDict


book: str = ''


class BookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book: str
