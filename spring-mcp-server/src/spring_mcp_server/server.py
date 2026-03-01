"""
Point de composition du serveur MCP Spring Documentation.

Architecture respectée :
- Data layer : Tools, Resources, Prompts (primitives MCP)
- Transport layer : STDIO (local) — géré par FastMCP
- Lifecycle : initialize/ready/notifications géré par FastMCP
"""

from fastmcp import FastMCP
from spring_mcp_server.resources.spring_registry import REGISTRE_SPRING
from spring_mcp_server.tools.fetch_page import recuperer_contenu_doc
from spring_mcp_server.tools.search import rechercher_dans_spring_docs
from spring_mcp_server.prompts.spring_prompts import PROMPTS_SPRING

# Création du serveur MCP — Composable
mcp = FastMCP(
    name="spring-documentation-mcp",
    instructions=(
        "Serveur MCP de documentation Spring. "
        "Fournit des outils pour rechercher et consulter la documentation "
        "des modules Spring (Framework, Boot, Data, Security, AI). "
        "Toutes les réponses sont en français."
    ),
)


# ─── TOOLS ───────────────────────────────────────────────────────────────────

@mcp.tool(
    description=(
            "Recherche dans la documentation d'un module Spring. "
            "Modules disponibles : spring-framework, spring-boot, spring-data, "
            "spring-security, spring-ai."
    )
)
async def rechercher_documentation(requete: str, module: str = "spring-boot") -> str:
    """Recherche un terme dans la documentation Spring. Répond en français."""
    resultats = await rechercher_dans_spring_docs(requete, module)
    if not resultats:
        return f"Aucun résultat trouvé pour '{requete}' dans le module '{module}'."

    lignes = [f"## Résultats pour '{requete}' dans {module}\n"]
    for r in resultats:
        lignes.append(f"**{r['titre']}**\n{r['url']}\n{r['extrait']}\n")
    return "\n".join(lignes)


@mcp.tool(
    description="Récupère le contenu complet d'une page de documentation Spring depuis son URL."
)
async def lire_page_documentation(url: str) -> str:
    """Lit et retourne le contenu d'une page de documentation Spring."""
    return await recuperer_contenu_doc(url)


@mcp.tool(
    description="Liste tous les modules Spring disponibles avec leurs URLs de documentation."
)
async def lister_modules_spring() -> str:
    """Retourne la liste des modules Spring disponibles dans ce serveur MCP."""
    lignes = ["## Modules Spring disponibles\n"]
    for cle, module in REGISTRE_SPRING.items():
        lignes.append(f"- **{module.nom}** (`{cle}`)\n  {module.description}\n  {module.url_base}")
    return "\n".join(lignes)


# ─── RESOURCES ────────────────────────────────────────────────────────────────

@mcp.resource("spring://modules")
async def resource_modules() -> str:
    """Resource : registre complet des modules Spring disponibles."""
    import json
    return json.dumps(
        {cle: {"nom": m.nom, "url": m.url_base, "description": m.description}
         for cle, m in REGISTRE_SPRING.items()},
        ensure_ascii=False,
        indent=2,
    )


@mcp.resource("spring://module/{module_id}")
async def resource_module(module_id: str) -> str:
    """Resource : détails d'un module Spring spécifique."""
    if module_id not in REGISTRE_SPRING:
        return f"Module '{module_id}' non trouvé."
    module = REGISTRE_SPRING[module_id]
    return (
        f"# {module.nom}\n\n"
        f"**Description** : {module.description}\n\n"
        f"**Documentation** : {module.url_base}"
    )


# ─── PROMPTS ──────────────────────────────────────────────────────────────────

@mcp.prompt(description="Aide à la migration entre deux versions de Spring Boot")
def prompt_migration_spring_boot(version_source: str, version_cible: str) -> str:
    template = PROMPTS_SPRING["migration-spring-boot"]["template"]
    return template.format(version_source=version_source, version_cible=version_cible)


@mcp.prompt(description="Guide architecture hexagonale avec Spring Boot")
def prompt_architecture_hexagonale() -> str:
    return PROMPTS_SPRING["architecture-hexagonale-spring"]["template"]


@mcp.prompt(description="Guide pour remplacer Hibernate par Spring JDBC/Data JDBC")
def prompt_supprimer_hibernate(nom_entite: str) -> str:
    template = PROMPTS_SPRING["supprimer-hibernate"]["template"]
    return template.format(nom_entite=nom_entite)


# ─── ENTRYPOINT ───────────────────────────────────────────────────────────────

def main() -> None:
    """Lance le serveur MCP en mode STDIO (transport local)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()