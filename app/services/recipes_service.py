"""Servicio que maneja la logica de negocio de las recetas.  Maneja el crud de las recetas y la tabla intermedia recipes_ingredients entre recetas e ingredientes"""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models import (
    IngredientResponse,
    Ingredients,
    RecipeIngredients,
    RecipeIngredientsResponse,
    Recipes,
    RecipesCreate,
    RecipesResponse,
)
from app.models.categories import Categories, CategorieSingleResponse


async def create_recipe(
    db: Session, recipe_data: RecipesCreate, owner_id: uuid.UUID
) -> RecipesResponse:
    """Crea una nueva receta en la base de datos con ingredientes asociados.

    Garantiza que todas las relaciones necesarias se cargan eagerly dentro del contexto
    async, evitando lazy-loading fuera de la sesión que causa MissingGreenlet.

    Args:
        db (Session): Sesión de base de datos asíncrona.
        recipe_data (RecipesCreate): Datos de la receta a crear.
        owner_id (uuid.UUID): ID del usuario propietario de la receta.

    Returns:
        RecipesResponse: DTO con la receta y sus ingredientes completamente cargados.

    Raises:
        HTTPException: Si hay errores de validación o base de datos.
    """
    recipe_id_local: uuid.UUID | None = None
    try:
        # 1. Crear la receta principal
        new_recipe = Recipes(
            name=recipe_data.name,
            description=recipe_data.description,
            instructions=recipe_data.instructions,
            prep_time=recipe_data.prep_time,
            servings=recipe_data.servings,
            visibility=recipe_data.visibility,
            owner_id=owner_id,
        )
        db.add(new_recipe)
        await db.commit()
        await db.refresh(new_recipe)
        # Guardar el ID localmente para evitar acceso perezoso después
        recipe_id_local = new_recipe.recipe_id

        # 2. Procesar ingredientes y crear relaciones
        for ing in recipe_data.ingredients:
            db_ingredient = None
            # Buscar ingrediente por id o nombre
            if ing.ingredient_id:
                stmt = select(Ingredients).where(
                    Ingredients.ingredient_id == ing.ingredient_id
                )
                result = await db.scalars(stmt)
                db_ingredient = result.first()
            elif ing.name:
                stmt = select(Ingredients).where(Ingredients.name == ing.name)
                result = await db.scalars(stmt)
                db_ingredient = result.first()
            # Si no existe, crearlo (requiere datos mínimos)
            if not db_ingredient:
                if not ing.name or not ing.category_id or not ing.default_unit:
                    await db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Faltan datos para crear el ingrediente: {ing.name}",
                    )
                db_ingredient = Ingredients(
                    name=ing.name,
                    category_id=ing.category_id,
                    default_unit=ing.default_unit,
                )
                db.add(db_ingredient)
                await db.commit()
                await db.refresh(db_ingredient)
            # Crear relación en recipe_ingredients
            recipe_ingredient = RecipeIngredients(
                recipe_id=recipe_id_local,
                ingredient_id=db_ingredient.ingredient_id,
                quantity=ing.quantity,
                optional=ing.optional if ing.optional is not None else False,
            )
            db.add(recipe_ingredient)
            await db.commit()

        # 3. Cargar la receta con relaciones eager (selectinload)
        # Esto evita lazy-loading cuando accedemos a los atributos en el DTO
        stmt = (
            select(Recipes)
            .where(Recipes.recipe_id == recipe_id_local)
            .options(
                selectinload(Recipes.recipe_ingredients).selectinload(
                    RecipeIngredients.ingredient
                )
            )
        )
        result = await db.execute(stmt)
        recipe_with_relations = result.scalar_one_or_none()
        if recipe_with_relations is None:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se pudo recuperar la receta creada con id {recipe_id_local}.",
            )

        # 4. Construir DTOs de ingredientes con categorías (eagerly loaded)
        recipe_ingredients_responses: list[RecipeIngredientsResponse] = []
        for ri in recipe_with_relations.recipe_ingredients:
            ingredient = ri.ingredient
            # Cargar categoría eagerly para evitar lazy-load
            stmt_cat = select(Categories).where(
                Categories.category_id == ingredient.category_id
            )
            result_cat = await db.execute(stmt_cat)
            category_obj = result_cat.scalar_one_or_none()
            if category_obj is None:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se encontró la categoría con id {ingredient.category_id} para el ingrediente {ingredient.name}.",
                )
            category_dto = CategorieSingleResponse(
                category_id=category_obj.category_id, name=category_obj.name
            )
            ingredient_response = IngredientResponse(
                ingredient_id=ingredient.ingredient_id,
                name=ingredient.name,
                category_id=ingredient.category_id,
                default_unit=ingredient.default_unit,
                category=category_dto,
            )
            recipe_ingredients_responses.append(
                RecipeIngredientsResponse(
                    quantity=ri.quantity,
                    optional=ri.optional,
                    ingredient=ingredient_response,
                )
            )
        # 5. Construir y retornar respuesta (todo dentro del contexto async)
        return RecipesResponse(
            recipe_id=recipe_with_relations.recipe_id,
            owner_id=recipe_with_relations.owner_id,
            name=recipe_with_relations.name,
            description=recipe_with_relations.description,
            instructions=recipe_with_relations.instructions,
            prep_time=recipe_with_relations.prep_time,
            servings=recipe_with_relations.servings,
            visibility=recipe_with_relations.visibility,
            created_at=recipe_with_relations.created_at,
            update_at=recipe_with_relations.update_at,
            recipe_ingredients=recipe_ingredients_responses,
        )
    except HTTPException:
        # Re-lanzar excepciones HTTP sin encapsular
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la receta: {str(e)}",
        ) from e
