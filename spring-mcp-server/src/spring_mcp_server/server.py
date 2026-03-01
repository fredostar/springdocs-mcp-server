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
from spring_mcp_server.resources.migration_registry import (
    REGISTRE_MIGRATION,
    filtrer_par_tags,
)
from spring_mcp_server.resources.breaking_changes import (
    BREAKING_CHANGES,
    breaking_changes_par_tags,
)
from spring_mcp_server.tools.fetch_page import recuperer_contenu_doc
from spring_mcp_server.tools.migration_guide import (
    MIGRATIONS_SUPPORTEES,
    generer_guide_migration,
)
from spring_mcp_server.tools.openrewrite import (
    RECETTES_OPENREWRITE,
    generer_config_openrewrite,
)
from spring_mcp_server.prompts.migration_prompts import PROMPTS_MIGRATION

from spring_mcp_server.resources.batch_registry import (
    REGISTRE_BATCH,
    filtrer_batch_par_tags,
)
from spring_mcp_server.resources.batch_breaking_changes import (
    BATCH_BREAKING_CHANGES,
    batch_breaking_changes_par_tags,
)
from spring_mcp_server.tools.batch_migration_guide import (
    MIGRATIONS_BATCH_SUPPORTEES,
    generer_guide_batch,
)
from spring_mcp_server.prompts.batch_prompts import PROMPTS_BATCH

# Création du serveur MCP — Composable
mcp = FastMCP(
    name="spring-documentation-mcp",
    instructions=(
        "Serveur MCP de documentation Spring. "
        "Fournit des outils pour rechercher et consulter la documentation "
        "des modules Spring (Framework, Boot, Data, Security, AI). "
        "Serveur MCP spécialisé en migration Spring Boot et Java. "
        "Couvre : Spring Boot 2.x→3.x→3.5, Java 11→17→21, "
        "javax→jakarta, Hibernate→Spring Data JDBC. "
        "Fournit guides, breaking changes, recettes OpenRewrite et prompts experts. "
        "Toutes les réponses sont en français."
    ),
)


# ─── TOOLS ───────────────────────────────────────────────────────────────────
@mcp.tool(description=(
        "Génère un guide de migration Spring Batch complet avec exemples de code. "
        "Types : spring-batch-4-5, spring-batch-5-52, spring-batch-java21."
))
async def guide_migration_batch(
        type_migration: str,
        avec_contenu_officiel: bool = False,
) -> str:
    """Guide complet de migration Spring Batch avec avant/après code."""
    return await generer_guide_batch(type_migration, avec_contenu_officiel)


@mcp.tool(description=(
        "Retourne les breaking changes Spring Batch 5 avec exemples de code avant/après. "
        "Tags : batch-5, job-builder, chunk, job-repository, observability, java21."
))
async def breaking_changes_batch(tags: str) -> str:
    """Breaking changes Spring Batch filtrés par tags, avec code avant/après."""
    liste_tags = tuple(t.strip() for t in tags.split(","))
    bcs = batch_breaking_changes_par_tags(*liste_tags)

    if not bcs:
        return f"Aucun breaking change Spring Batch trouvé pour : {tags}"

    lignes = [f"## Breaking changes Spring Batch — {tags}\n"]
    for bc in bcs:
        lignes.append(f"### ⚠️ {bc.titre}")
        lignes.append(f"{bc.description}\n")
        lignes.append("**Avant (Spring Batch 4)**")
        lignes.append(f"```java{bc.avant}```")
        lignes.append("**Après (Spring Batch 5)**")
        lignes.append(f"```java{bc.apres}```\n")
    return "\n".join(lignes)


@mcp.tool(description="Liste les sources de documentation Spring Batch disponibles.")
async def lister_sources_batch(tag: str = "") -> str:
    """Retourne le registre des sources Batch, filtré par tag si fourni."""
    sources = filtrer_batch_par_tags(tag) if tag else REGISTRE_BATCH
    lignes = [f"## Sources Spring Batch{f' (tag: {tag})' if tag else ''}\n"]
    for cle, source in sources.items():
        lignes.append(f"### `{cle}` — {source.nom}")
        lignes.append(f"{source.description}")
        lignes.append(f"Tags : {', '.join(source.tags)}")
        lignes.append(f"URL : {source.url}\n")
    return "\n".join(lignes)

@mcp.tool(description=(
        "Génère un guide de migration complet étape par étape. "
        "Types disponibles : spring-boot-2-3, java-11-21, "
        "hibernate-spring-data-jdbc, jakarta-javax."
))
async def guide_migration(
        type_migration: str,
        avec_contenu_officiel: bool = False,
) -> str:
    """Guide complet pour un type de migration donné."""
    return await generer_guide_migration(type_migration, avec_contenu_officiel)


@mcp.tool(description=(
        "Retourne les breaking changes critiques pour un type de migration. "
        "Tags disponibles : spring-boot-3, jakarta, hibernate, java17, java21, "
        "spring-data-jdbc, virtual-threads."
))
async def breaking_changes_migration(tags: str) -> str:
    """Liste les breaking changes critiques filtrés par tags (séparés par virgule)."""
    liste_tags = tuple(t.strip() for t in tags.split(","))
    bcs = breaking_changes_par_tags(*liste_tags)

    if not bcs:
        return f"Aucun breaking change trouvé pour les tags : {tags}"

    lignes = [f"## Breaking changes pour : {tags}\n"]
    for bc in bcs:
        lignes.append(f"### ⚠️ {bc.titre}")
        lignes.append(f"**Problème** : {bc.description}")
        lignes.append(f"**Solution** : {bc.solution}\n")
    return "\n".join(lignes)


@mcp.tool(description=(
        "Génère la configuration OpenRewrite Maven pour une migration. "
        "Types : spring-boot-3, spring-boot-35, java-21, jakarta."
))
async def config_openrewrite(type_migration: str) -> str:
    """Configuration OpenRewrite prête à l'emploi pour Maven."""
    return generer_config_openrewrite(type_migration)


@mcp.tool(description=(
        "Récupère le contenu officiel d'une source de documentation de migration. "
        "Clés disponibles dans le registre : spring-boot-2x-3x, java-17-21, etc."
))
async def lire_guide_officiel(cle_source: str) -> str:
    """Fetch le contenu officiel d'une source du registre de migration."""
    if cle_source not in REGISTRE_MIGRATION:
        disponibles = ", ".join(REGISTRE_MIGRATION.keys())
        return f"Source '{cle_source}' inconnue. Disponibles : {disponibles}"

    source = REGISTRE_MIGRATION[cle_source]
    contenu = await recuperer_contenu_doc(source.url)
    return f"# {source.nom}\n\n{contenu}"


@mcp.tool(description="Liste toutes les sources de migration disponibles, avec filtrage optionnel par tag.")
async def lister_sources_migration(tag: str = "") -> str:
    """Retourne le registre des sources de migration, filtré par tag si fourni."""
    sources = filtrer_par_tags(tag) if tag else REGISTRE_MIGRATION
    lignes = [f"## Sources de migration disponibles{f' (tag: {tag})' if tag else ''}\n"]
    for cle, source in sources.items():
        lignes.append(f"### `{cle}` — {source.nom}")
        lignes.append(f"{source.description}")
        lignes.append(f"Tags : {', '.join(source.tags)}")
        lignes.append(f"URL : {source.url}\n")
    return "\n".join(lignes)
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

@mcp.resource("migration://batch/registre")
async def resource_batch_registre() -> str:
    """Registre complet des sources Spring Batch."""
    import json
    return json.dumps(
        {
            cle: {
                "nom": s.nom,
                "url": s.url,
                "description": s.description,
                "tags": list(s.tags),
            }
            for cle, s in REGISTRE_BATCH.items()
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.resource("migration://batch/breaking-changes/{tag}")
async def resource_batch_breaking_changes(tag: str) -> str:
    """Breaking changes Spring Batch filtrés par tag, avec code avant/après."""
    bcs = batch_breaking_changes_par_tags(tag)
    import json
    return json.dumps(
        [
            {
                "titre": bc.titre,
                "description": bc.description,
                "avant": bc.avant,
                "apres": bc.apres,
                "tags": list(bc.tags),
            }
            for bc in bcs
        ],
        ensure_ascii=False,
        indent=2,
    )

@mcp.resource("migration://registre")
async def resource_registre() -> str:
    """Registre complet de toutes les sources de migration."""
    import json
    return json.dumps(
        {
            cle: {
                "nom": s.nom,
                "url": s.url,
                "description": s.description,
                "tags": list(s.tags),
            }
            for cle, s in REGISTRE_MIGRATION.items()
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.resource("migration://breaking-changes/{tag}")
async def resource_breaking_changes(tag: str) -> str:
    """Breaking changes filtrés par tag."""
    bcs = breaking_changes_par_tags(tag)
    import json
    return json.dumps(
        [{"titre": bc.titre, "description": bc.description, "solution": bc.solution}
         for bc in bcs],
        ensure_ascii=False,
        indent=2,
    )


@mcp.resource("migration://types-supportes")
async def resource_types_supportes() -> str:
    """Types de migration supportés avec leurs étapes."""
    import json
    return json.dumps(MIGRATIONS_SUPPORTEES, ensure_ascii=False, indent=2)


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
@mcp.prompt(description=PROMPTS_BATCH["migrer-job-batch-4-vers-5"]["description"])
def prompt_migrer_job_batch(code_batch_4: str) -> str:
    return PROMPTS_BATCH["migrer-job-batch-4-vers-5"]["template"].format(
        code_batch_4=code_batch_4
    )


@mcp.prompt(description=PROMPTS_BATCH["analyser-job-pour-migration"]["description"])
def prompt_analyser_job_batch(code_job: str) -> str:
    return PROMPTS_BATCH["analyser-job-pour-migration"]["template"].format(
        code_job=code_job
    )


@mcp.prompt(description=PROMPTS_BATCH["optimiser-batch-virtual-threads"]["description"])
def prompt_optimiser_batch_virtual_threads(code_step: str) -> str:
    return PROMPTS_BATCH["optimiser-batch-virtual-threads"]["template"].format(
        code_step=code_step
    )


@mcp.prompt(description=PROMPTS_MIGRATION["analyser-code-pour-migration"]["description"])
def prompt_analyser_code(code: str, version_java_cible: str = "21") -> str:
    template = PROMPTS_MIGRATION["analyser-code-pour-migration"]["template"]
    return template.format(code=code, version_java_cible=version_java_cible)


@mcp.prompt(description=PROMPTS_MIGRATION["plan-migration-projet"]["description"])
def prompt_plan_migration(
        version_spring_boot_source: str,
        version_spring_boot_cible: str,
        version_java_source: str,
        version_java_cible: str,
        orm: str = "Hibernate/JPA",
        modules_spring: str = "Web, Data JPA, Security",
) -> str:
    template = PROMPTS_MIGRATION["plan-migration-projet"]["template"]
    return template.format(
        version_spring_boot_source=version_spring_boot_source,
        version_spring_boot_cible=version_spring_boot_cible,
        version_java_source=version_java_source,
        version_java_cible=version_java_cible,
        orm=orm,
        modules_spring=modules_spring,
    )


@mcp.prompt(description=PROMPTS_MIGRATION["migrer-entite-jpa-vers-jdbc"]["description"])
def prompt_migrer_entite_jpa(code_entite_jpa: str) -> str:
    template = PROMPTS_MIGRATION["migrer-entite-jpa-vers-jdbc"]["template"]
    return template.format(code_entite_jpa=code_entite_jpa)

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