# springdocs-mcp-server

Un serveur MCP (Model Context Protocol) spécialisé dans la documentation Spring et les migrations Spring Boot.

Permet aux clients MCP (Claude, autres outils IA) d'accéder à des outils et ressources pour :
- Rechercher dans la documentation officielle Spring.
- Consulter les guides de migration Spring Boot (2.x → 3.x, Java 11 → 21, etc.).
- Obtenir les breaking changes critiques.
- Générer des configurations OpenRewrite pour les migrations.

## 📋 Fonctionnalités

### Recherche et Documentation
- Rechercher dans les modules Spring (Framework, Boot, Data, Security, AI).
- Récupérer le contenu complet des pages de documentation.
- Lister tous les modules disponibles.

### Guides de Migration
- Générer des guides complets étape par étape.
- Types supportés : `spring-boot-2-3`, `java-11-21`, `hibernate-spring-data-jdbc`, `jakarta-javax`.
- Récupérer les breaking changes filtrés par tags.

### OpenRewrite
- Générer les configurations Maven pour les migrations.
- Types : `spring-boot-3`, `spring-boot-35`, `java-21`, `jakarta`.

### Prompts Experts
- Accès à des prompts pré-configurés pour l'assistance en migration et documentation.

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
   - Dans l'interface, vous verrez tous les outils disponibles.
   - Exemples :
     - `rechercher_documentation` : Chercher "Spring Security" dans spring-boot.
     - `breaking_changes_migration` : Obtenir les breaking changes pour la migration vers Spring Boot 3.
     - `guide_migration` : Générer un guide complet pour une migration.
     - `config_openrewrite` : Générer une configuration OpenRewrite pour Maven.

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
    │   ├── migration_guide.py       # Guides de migration
    │   └── openrewrite.py          # Configuration OpenRewrite
    ├── resources/                   # Données statiques
    │   ├── spring_registry.py       # Registre des modules Spring
    │   ├── migration_registry.py    # Sources de migration
    │   └── breaking_changes.py      # Breaking changes catalogués
    └── prompts/                     # Prompts pré-configurés
        ├── spring_prompts.py        # Prompts documentation
        └── migration_prompts.py     # Prompts migration
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




