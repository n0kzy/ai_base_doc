Guide de standardisation pour le développement Python moderne. Priorise la vitesse d'exécution (Rust-based tooling), la sécurité de type (Static Typing) et la compatibilité agentic (Tool-calling optimization). Contient des règles strictes pour éliminer le code "legacy" (pip, flake8, black) au profit de la pile uv/ruff/ty.

🛠 1. Environment & Tooling (The 2026 Stack)
Rule 1.1: Dependency Management → Utiliser exclusivement uv. Interdiction d'utiliser pip ou poetry.

Correct: uv add pandas, uv run main.py.

Reason: Vitesse instantanée et verrouillage déterministe des dépendances.

Rule 1.2: Linting & Formatting → Utiliser Ruff pour TOUT (format, imports, lint).

Rule: Appliquer ruff check --fix et ruff format à chaque modification.

Reason: Remplace 5 outils lents par un seul binaire en Rust.

Rule 1.3: Project Structure → Toujours utiliser un layout src/.

Structure: project/src/app/, tests/, pyproject.toml.

🏗 2. Logic & Refactoring (Pythonic 2.0)
Rule 2.1: Logic Flattening → Remplacer les chaînes if/elif/else complexes par des dictionnaires ou le match statement (Python 3.10+).

Incorrect: if status == 'a': ... elif status == 'b': ...

Correct: mapping = {'a': func_a, 'b': func_b}; mapping.get(status, default)()

Rule 2.2: Comprehensions vs Loops → Préférer les list/dict comprehensions pour les transformations simples, mais rester sur des boucles for si la logique dépasse une ligne.

Rule 2.3: Lazy Evaluation → Utiliser des générateurs (yield) pour traiter les flux de données importants afin de minimiser l'empreinte RAM.

🔒 3. Type Safety & Validation
Rule 3.1: Strict Typing → Tous les arguments de fonction et retours doivent être typés. Utiliser Ty ou Pyright en mode strict.

Rule 3.2: Data Models → Utiliser Pydantic v2 pour toute donnée entrante (API, JSON, Config). Interdiction d'utiliser des dictionnaires bruts pour les structures de données complexes.

Pattern: class User(BaseModel): id: UUID; name: str.

Rule 3.3: Literal & Enums → Utiliser Literal pour les constantes de chaîne et Enum pour les catégories logiques.

⚡ 4. Performance & Data
Rule 4.1: Vectorization → Interdiction d'utiliser des boucles for sur des DataFrames. Utiliser Polars (Lazy API) au lieu de Pandas pour les nouveaux projets.

Correct: df.lazy().filter(pl.col("age") > 18).collect().

Rule 4.2: Asyncio → Utiliser async/await pour toutes les opérations I/O (requêtes API, DB, Filesystem). Utiliser AnyIO pour la compatibilité.

🤖 5. Agentic Integration (Instruction Tuning)
Rule 5.1: Docstring-as-Source → Les docstrings doivent suivre le format Google. Elles servent de description pour le "tool-calling" de l'agent.

Rule 5.2: Error Handling → Ne jamais faire un except Exception: pass. Toujours lever des exceptions spécifiques avec des messages d'erreur explicites que l'IA peut parser pour s'auto-corriger.