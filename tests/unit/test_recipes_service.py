import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

from app.models.ingredients import Categories, Ingredients
from app.models.recipes import (
    RecipeIngredientsCreateInput,
    RecipesCreate,
    RecipeVisibility,
)
from app.services.recipes_service import create_recipe


@pytest_asyncio.fixture
async def sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session


@pytest_asyncio.fixture
async def category(sqlite_session: AsyncSession) -> Categories:
    cat = Categories(name="Verduras")
    sqlite_session.add(cat)
    await sqlite_session.commit()
    await sqlite_session.refresh(cat)
    return cat


@pytest.mark.asyncio
async def test_create_recipe_with_new_and_existing_ingredients(
    sqlite_session: AsyncSession, category: Categories
) -> None:
    # Acceder a category_id inmediatamente y guardar en variable local
    category_id = category.category_id

    # Crear un ingrediente existente
    ing_existente = Ingredients(
        name="Papa", category_id=category_id, default_unit="unidad"
    )
    sqlite_session.add(ing_existente)
    await sqlite_session.commit()
    await sqlite_session.refresh(ing_existente)

    owner_id = uuid.uuid4()
    recipe_data = RecipesCreate(
        name="Tortilla de papas",
        description="Receta clásica",
        instructions="Batir huevos, mezclar con papas y freír.",
        prep_time=30,
        servings=4,
        visibility=RecipeVisibility.PUBLIC,
        ingredients=[
            RecipeIngredientsCreateInput(
                ingredient_id=ing_existente.ingredient_id,
                name="Papa",
                category_id=category_id,
                default_unit="unidad",
                quantity=2,
                optional=False,
            ),
            RecipeIngredientsCreateInput(
                ingredient_id=None,
                name="Huevo",
                category_id=category_id,
                default_unit="unidad",
                quantity=3,
                optional=False,
            ),
        ],
    )
    result = await create_recipe(sqlite_session, recipe_data, owner_id)
    assert result.name == "Tortilla de papas"
    assert result.owner_id == owner_id
    assert len(result.recipe_ingredients) == 2
    nombres = [ri.ingredient.name for ri in result.recipe_ingredients]
    assert "Papa" in nombres
    assert "Huevo" in nombres
    # Verifica que el ingrediente nuevo fue creado
    huevos = [
        ri.ingredient
        for ri in result.recipe_ingredients
        if ri.ingredient.name == "Huevo"
    ]
    assert huevos[0].ingredient_id is not None
    assert huevos[0].default_unit == "unidad"
