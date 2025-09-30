# Justificacion de la base de datos

## 1) Modelo conceptual (visión breve)

* **Catálogo compartido**: `ingredients`, `recipes`, `recipe_ingredients`.
  Motivo: efecto red (reuso/compartir), menos duplicados, curaduría más simple.
* **Estado personal**: `users`, `plan_entries`, `inventory_items`, `user_saved_recipes` (+ alias opcional).
  Motivo: cada familia tiene su propio plan e inventario sin contaminar el catálogo.
* **Lista de compras**: se **calcula** desde `plan_entries` + `recipe_ingredients` – `inventory_items`.
  Motivo: cero fricción en MVP; si después querés “checklist & historial”, se agrega `shopping_list*` sin romper nada.

---

## 2) Entidades y atributos (qué son y para qué sirven)

### A. `users` — dueño del estado

* **id**: PK. Identifica a la familia/usuario.
* **email**: login/contacto, único.
* **family_name**: etiqueta visible (“Familia Rosales”).
* **created_at/updated_at**: auditoría mínima.
  **Relaciones**: 1–N con `plan_entries`, `inventory_items`, `user_saved_recipes`, (autor opcional en `recipes`).
  **Por qué**: separa el **estado personal** del **catálogo**; base para multiusuario y permisos.

### B. `ingredients` — catálogo canónico global

* **id**: PK.
* **name** (único): normalización (“Arroz” es “Arroz”, no “arros”).
* **category**: filtros y exploración (“verduras”, “carnes”).
* **default_unit**: guía (g/ml/u), ayuda a UI y a escalado de cantidades.
  **Relaciones**: N–N con `recipes` vía `recipe_ingredients`; 1–N con `inventory_items`.
  **Por qué**: evitar que cada usuario invente su propio “tomatito cherry xD”; facilita matching de inventario/lista.

> Nota: si necesitás preferencias de nombres por usuario, se sugiere `user_ingredient_aliases` (opcional).

### C. `recipes` — catálogo de recetas global, compartible

* **id**: PK.
* **owner_user_id** (nullable, FK `users`): autor/curador; `NULL` para “del sistema”.
* **name**: búsqueda y UX.
* **description** / **instructions**: contenido útil (no UI vacía).
* **servings_default**: escala cantidades 1→N.
* **prep_minutes/cook_minutes**: filtros “rápidas”, métricas de experiencia.
* **visibility** (Enum: public/unlisted/private): control básico de acceso.
  **Relaciones**: N–N con `ingredients` vía `recipe_ingredients`; 1–N con `plan_entries`.
  **Por qué**: compartir **sin duplicar**; visibilidad permite crecer hacia “social”/moderación.

### D. `recipe_ingredients` — despiece de receta

* **recipe_id** / **ingredient_id**: FK al par receta/ingrediente.
* **quantity** / **unit**: cantidades por `servings_default` (clave para escalar).
* **optional**: marca aderezos o toppings no críticos.
* **position**: orden lógico (UX: mostrar pasos/orden).
  **Índice único (recipe_id, ingredient_id)**: evita duplicados.
  **Por qué**: relación de muchos a muchos con datos (cantidad/unidad), base para **lista de compras**.

### E. `plan_entries` — planificación diaria

* **user_id**: de quién es el plan.
* **date**: día concreto (evita problemas ISO-week).
* **meal** (Enum `lunch|dinner` en MVP): slot del día.
* **recipe_id** (nullable): permite slot vacío o “por definir”.
* **servings**: escala si hoy cocinás para 3 y no 2.
* **notes**: ajustes puntuales (“sin cebolla”).
  **Índice único (user_id, date, meal)**: un solo slot por comida/día/usuario.
  **Por qué**: **simple y robusto**; la UI puede agrupar por semana sin persistir “weekly_plan”.

### F. `inventory_items` — stock mínimo por usuario

* **user_id**: dueño del inventario.
* **ingredient_id**: qué ingrediente es.
* **quantity / unit**: cuánto hay y en qué medida (sin conversión en MVP).
* **expires_at**: futura alerta de vencimientos (opcional).
* **is_active**: soft-delete simple.
* **created_at/updated_at**: auditoría.
  **Índices**: (user_id, ingredient_id) único → 1 registro por ingrediente.
  **Por qué**: descontar del “requerido” para la lista; soporta UI básica de stock.

### G. `user_saved_recipes` — overlay personal (favoritos/overrides)

* **user_id / recipe_id**: a quién le gusta qué.
* **custom_name/custom_servings**: personalización sin duplicar receta global.
* **pinned/notes**: UX (“ancladas de la semana”).
  **Índice único (user_id, recipe_id)**.
  **Por qué**: **personalización sin fork**; evita contaminar el catálogo.

---

## 3) Relaciones clave (para qué las queremos)

* `users` 1–N `plan_entries` → plan por familia/día/comida.
* `users` 1–N `inventory_items` → stock privado.
* `users` 1–N `user_saved_recipes` → favoritos y overrides.
* `recipes` N–N `ingredients` (vía `recipe_ingredients`) → despiece con cantidades.
* `recipes` 1–N `plan_entries` → plan alimentado de recetas globales.
* `users` 1–N `recipes` (como owner opcional) → autoría/curaduría, no scope estricto.

**Justificación**: separa **conocimiento** (catálogo) de **estado** (plan/inventario), lo que:

* minimiza duplicados,
* permite compartir desde el día 1,
* y deja la puerta abierta a permisos/versionado sin migraciones duras.

---

## 4) Reglas de negocio que blinda el esquema

* **Plan único por slot**: `(user_id, date, meal)` **único** → no hay dos cenas el mismo día.
* **Ingrediente normalizado**: `ingredients.name` **único** → lista de compras sin ambigüedades (“tomate” ≠ “Tomates”).
* **Relación receta–ingrediente única**: `(recipe_id, ingredient_id)` **único** → no duplicás filas con el mismo ingrediente.
* **Inventario simple**: `(user_id, ingredient_id)` **único** → una existencia por ingrediente (si luego querés lotes: `inventory_batches` sin romper nada).
* **Personalización no destructiva**: `(user_id, recipe_id)` **único** en `user_saved_recipes` → favoritos/overrides limpios.

---

## 5) Por qué sirve al MVP (y cómo escala)

**MVP (rapidez):**

* CRUD mínimo: `recipes`, `ingredients`, `recipe_ingredients`.
* Plan: `plan_entries` (sin “weekly_plan” y sin cálculos raros de semana ISO).
* Inventario: `inventory_items` (1 fila por ingrediente).
* **Lista de compras**: derivada al vuelo → reduce tablas/procesos en MVP.

**Evolución (sin migraciones traumáticas):**

* **Checklist & historial de compras** → agregar `shopping_list` + `shopping_list_items`.
* **Plantillas/semanas clonables** → agregar `weekly_plan` + `planned_meals` como capa opcional.
* **Lotes y vencimientos finos** → `inventory_batches`.
* **Social/versionado** → `recipe_versions`, `recipe_forks`, `ratings`, `comments`.
* **Dietas/alergias** → `user_dietary_prefs` y filtros sobre `recipe_ingredients`.

---

## 6) Índices y performance (lo justo y necesario)

* `plan_entries`: `(user_id, date, meal)` **unique** + índice por `user_id` → consultas semanales rápidas.
* `recipe_ingredients`: `(recipe_id, ingredient_id)` **unique** + índices por `recipe_id` → joins de lista/plan fluidos.
* `inventory_items`: `(user_id, ingredient_id)` **unique`** → match inventario vs requerida sin subconsultas raras.
* `ingredients.name` **unique** → búsquedas por nombre, autocomplete.
* `recipes.name`, `recipes.visibility`, `recipes.owner_user_id` → explorar/filtrar; baratos en SQLite.

---

## 7) Riesgos conocidos y mitigaciones

* **Unidades heterogéneas**: no hay conversión automática (diseño intencional de MVP).
  Mitigación: mantener `default_unit` y UI consistente; agregar tabla de unidades/factores si hace falta.
* **Alias de ingredientes**: choque entre “Harina 000” vs “Harina común”.
  Mitigación: `user_ingredient_aliases` (opcional) o curaduría del catálogo.
* **Plan vs Semana ISO**: calculamos semanas en la capa de servicios; evitamos inconsistencias persistidas.
  Mitigación: si el negocio lo exige, más adelante se persiste `weekly_plan`.

---

## 8) Conclusión

* **Separar catálogo (global) de estado (por usuario)** es lo que permite:

  1. **MVP rápido** (menos tablas, menos sincronización),
  2. **Compartir desde el inicio** (recetas/ingredientes comunes),
  3. **Escalar sin sangre** (añadir listas persistentes, plantillas, lotes, social, etc.).
* Las **constraints** propuestas (uniques + FKs + enums básicos) garantizan integridad sin sobrecargar el desarrollo inicial.
* Resultado: **simple donde importa, flexible donde conviene**. Si mañana pedís features “pro”, el modelo no te encierra.
