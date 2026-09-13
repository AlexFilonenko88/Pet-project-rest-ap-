from pydantic import BaseModel, ConfigDict, Field


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str | None = Field(max_length=25, min_length=3, default=None)


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(max_length=25, min_length=3, default=None)
