from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_category_service
from app.schemas.category import CategoryCreateSchema, CategoryUpdateSchema, CategorySchema
from app.services.category import CategoryService, CategoryNotFound


router = APIRouter(prefix='/categories')


@router.get('')
def read_categories(
    category_service: CategoryService = Depends(get_category_service)
) -> list[CategorySchema]:
    return category_service.list_categories()


@router.post('', status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_service)
) -> CategorySchema:
    return category_service.create_category(category_create=payload)


@router.patch('/{id}')
def update_category(
    id: str,
    payload: CategoryUpdateSchema,
    category_service: CategoryService = Depends(get_category_service)
) -> CategorySchema:
    try:
        return category_service.update_category(category_id=id, category_update=payload)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    id: str,
    category_service: CategoryService = Depends(get_category_service)
) -> None:
    try:
        return category_service.delete_category(category_id=id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
