# springdocs-mcp-server

Un serveur MCP (Model Context Protocol) spécialisé dans la documentation Spring et les migrations Spring Boot.

Permet aux clients MCP (Claude, autres outils IA) d'accéder à des outils et ressources pour :
- Rechercher dans la documentation officielle Spring.
- Consulter les guides de migration Spring Boot (2.x → 3.x, Java 11 → 21, etc.).
- Obtenir les breaking changes critiques.
- Générer des configurations OpenRewrite pour les migrations.

## 📋 Fonctionnalités

### 🔍 Recherche et Documentation Spring
- Rechercher dans les modules Spring (Framework, Boot, Data, Security, AI).
- Récupérer le contenu complet des pages de documentation.
- Lister tous les modules disponibles avec descriptions détaillées.

### 🚀 Guides de Migration Spring Boot & Java
- Générer des guides complets étape par étape.
- Types supportés : `spring-boot-2-3`, `java-11-21`, `hibernate-spring-data-jdbc`, `jakarta-javax`.
- Récupérer les breaking changes critiques filtrés par tags.
- Sources officielles de documentation pour chaque migration.

### 🔄 Migration Spring Batch
- Guides complets pour Spring Batch 4.x → 5.x.
- Types supportés : `spring-batch-4-5`, `spring-batch-5-52`, `spring-batch-java21`.
- Breaking changes Spring Batch avec exemples de code avant/après.
- Support des virtual threads Java 21.
- Tags disponibles : `batch-5`, `job-builder`, `chunk`, `job-repository`, `observability`, `java21`.

### 🔧 OpenRewrite
- Générer les configurations Maven prêtes à l'emploi pour les migrations.
- Types : `spring-boot-3`, `spring-boot-35`, `java-21`, `jakarta`.

### 💡 Prompts Experts
- **Prompts Migration** : Analyser du code, planifier une migration, migrer JPA vers JDBC.
- **Prompts Spring** : Migration Spring Boot, architecture hexagonale, suppression Hibernate.
- **Prompts Batch** : Migration Job Batch 4→5, analyse pour migration, optimisation Virtual Threads.
- Tous les prompts incluent des instructions détaillées et des exemples de code.

## 🚀 Installation

### Prérequis
- Python 3.13 ou supérieur
- `uv` (gestionnaire de paquets Python ultra-rapide) - [Installation](https://docs.astral.sh/uv/)

### Étapes d'installation

1. **Cloner le repository ou naviguer vers le répertoire du projet**
   ```bash
   cd /Users/fredericradigoy/Documents/mesProjets/springdocs/spring-mcp-server
   ```

2. **Installer les dépendances avec uv**
   ```bash
   uv sync
   ```
   Cela installe Python 3.13 automatiquement si nécessaire et résout toutes les dépendances.

## 🎯 Lancer le serveur localement

### Via uv (recommandé)

```bash
cd /Users/fredericradigoy/Documents/mesProjets/springdocs/spring-mcp-server
uv run spring-mcp-server
```

Le serveur démarre et attend les connexions MCP via stdio.

### Via Python directement

```bash
cd /Users/fredericradigoy/Documents/mesProjets/springdocs/spring-mcp-server
python -m spring_mcp_server.server
```

## 🧪 Tester avec MCP Inspector

[MCP Inspector](https://inspector.modelcontextprotocol.io) est l'outil officiel de débogage pour les serveurs MCP.

### Lancer MCP Inspector localement

1. **Installer MCP Inspector** (si pas déjà installé)
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. **Lancer MCP Inspector avec le serveur en arrière-plan**
   ```bash
   # Terminal 1 : Démarrer le serveur MCP
   cd /Users/fredericradigoy/Documents/mesProjets/springdocs/spring-mcp-server
   uv run spring-mcp-server
   
   # Terminal 2 : Lancer MCP Inspector
   mcp-inspector
   
   ou 
   npx @modelcontextprotocol/inspector uv run spring-mcp-server
   ```

3. **Configurer la connexion dans MCP Inspector**
   - L'interface web s'ouvre automatiquement (généralement sur `http://localhost:5173`).
   - Sélectionner "Add Server" ou configurer la connexion vers :
     - **Commande** : `uv run spring-mcp-server`
     - **Répertoire de travail** : `/Users/fredericradigoy/Documents/mesProjets/springdocs/spring-mcp-server`

4. **Tester les outils disponibles**
   
   Dans l'interface MCP Inspector, vous verrez tous les outils disponibles. Voici quelques exemples de tests :

   **Documentation Spring**
   - `rechercher_documentation` : Chercher "Spring Security" dans spring-boot.
   - `lire_page_documentation` : Récupérer le contenu d'une page officielle.
   - `lister_modules_spring` : Voir tous les modules disponibles.

   **Migration Spring Boot & Java**
   - `breaking_changes_migration` : Obtenir les breaking changes pour la migration vers Spring Boot 3 (tags : `spring-boot-3,jakarta`).
   - `guide_migration` : Générer un guide complet pour `spring-boot-2-3`.
   - `config_openrewrite` : Générer une configuration OpenRewrite pour Maven.
   - `lister_sources_migration` : Voir toutes les sources de documentation.

   **Migration Spring Batch**
   - `breaking_changes_batch` : Obtenir les breaking changes Batch 5 (tags : `batch-5,job-builder`).
   - `guide_migration_batch` : Générer un guide pour `spring-batch-4-5`.
   - `lister_sources_batch` : Voir les sources de documentation Batch disponibles.

   **Prompts (pour Claude ou autre IA)**
   - `prompt_migration_spring_boot` : Aide à la migration Spring Boot.
   - `prompt_plan_migration` : Planifier une migration complète.
   - `prompt_migrer_job_batch` : Migrer un Job Batch 4 vers 5.

## 📂 Structure du projet

```
spring-mcp-server/
├── main.py                          # Point d'entrée principal
├── pyproject.toml                   # Configuration du projet Python
├── README.md                        # Fichier README
├── uv.lock                          # Verrou des dépendances uv
└── src/spring_mcp_server/
    ├── __init__.py
    ├── server.py                    # Serveur MCP FastMCP (cœur)
    ├── tools/                       # Outils MCP exposés
    │   ├── fetch_page.py           # Récupération de contenu
    │   ├── search.py               # Recherche dans la documentation
    │   ├── migration_guide.py       # Guides de migration Spring Boot/Java
    │   ├── batch_migration_guide.py # Guides de migration Spring Batch
    │   └── openrewrite.py          # Configuration OpenRewrite
    ├── resources/                   # Données statiques
    │   ├── spring_registry.py       # Registre des modules Spring
    │   ├── migration_registry.py    # Sources de migration Spring Boot/Java
    │   ├── batch_registry.py        # Sources de migration Spring Batch
    │   ├── breaking_changes.py      # Breaking changes Spring Boot/Java
    │   └── batch_breaking_changes.py# Breaking changes Spring Batch
    └── prompts/                     # Prompts pré-configurés
        ├── spring_prompts.py        # Prompts documentation Spring
        ├── migration_prompts.py     # Prompts migration Spring Boot/Java
        └── batch_prompts.py         # Prompts migration Spring Batch
```

## 🔧 Dépendances

- **fastmcp** : Framework MCP moderne et composable.
- **httpx** : Client HTTP asynchrone pour récupérer les pages.
- **beautifulsoup4** : Parsing HTML pour extraire le contenu.

## 📝 Notes de développement

- Toutes les réponses sont en français.
- Le serveur utilise STDIO pour communiquer avec les clients MCP.
- Architecture composable avec séparation claire : Tools, Resources, Prompts.
- Les ressources sont chargées au démarrage pour optimiser les performances.




