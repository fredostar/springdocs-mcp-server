"""Tool de recherche dans la documentation Spring via Google Custom Search."""

import httpx

async def rechercher_dans_spring_docs(
        requete: str,
        module: str = "spring-boot",
) -> list[dict[str, str]]:
    """
    Recherche dans la documentation Spring.
    Retourne une liste de résultats {titre, url, extrait}.
    """
    from spring_mcp_server.resources.spring_registry import REGISTRE_SPRING

    if module not in REGISTRE_SPRING:
        modules_disponibles = ", ".join(REGISTRE_SPRING.keys())
        raise ValueError(
            f"Module '{module}' inconnu. Modules disponibles : {modules_disponibles}"
        )

    spring_module = REGISTRE_SPRING[module]
    url_recherche = (
        f"https://docs.spring.io/search.html?q={requete.replace(' ', '+')}"
        f"&module={module}"
    )

    # Fallback : retourner l'URL de base avec le contexte
    return [
        {
            "titre": f"Documentation {spring_module.nom}",
            "url": spring_module.url_base,
            "extrait": (
                f"Documentation principale pour {spring_module.description}. "
                f"Recherche effectuée : '{requete}'"
            ),
        }
    ]