"""Tool de recherche dans la documentation Spring."""

import httpx
from bs4 import BeautifulSoup

from spring_mcp_server.resources.spring_registry import REGISTRE_SPRING


async def rechercher_dans_spring_docs(
        requete: str,
        module: str = "spring-boot",
) -> list[dict[str, str]]:
    """
    Recherche dans la documentation Spring.
    Retourne une liste de résultats {titre, url, extrait}.
    """
    if module not in REGISTRE_SPRING:
        modules_disponibles = ", ".join(REGISTRE_SPRING.keys())
        raise ValueError(
            f"Module '{module}' inconnu. Modules disponibles : {modules_disponibles}"
        )

    spring_module = REGISTRE_SPRING[module]
    mots_cles = requete.lower().split()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            reponse = await client.get(spring_module.url_base, follow_redirects=True)
            reponse.raise_for_status()
    except httpx.HTTPStatusError as e:
        return [{
            "titre": spring_module.nom,
            "url": spring_module.url_base,
            "extrait": f"Erreur HTTP {e.response.status_code} lors de l'accès à la documentation.",
        }]
    except httpx.RequestError:
        return [{
            "titre": spring_module.nom,
            "url": spring_module.url_base,
            "extrait": "Impossible d'accéder à la documentation Spring.",
        }]

    soup = BeautifulSoup(reponse.text, "html.parser")
    base_url = str(reponse.url)
    resultats = []

    for lien in soup.find_all("a", href=True):
        texte = lien.get_text(strip=True)
        href = lien["href"]

        if not texte:
            continue

        # Construit l'URL absolue
        if href.startswith("http"):
            url_complete = href
        elif href.startswith("/"):
            url_complete = f"https://docs.spring.io{href}"
        else:
            url_complete = f"{base_url.rstrip('/')}/{href.lstrip('/')}"

        # Filtre les liens pertinents
        texte_lower = texte.lower()
        href_lower = href.lower()
        if any(mot in texte_lower or mot in href_lower for mot in mots_cles):
            resultats.append({
                "titre": texte,
                "url": url_complete,
                "extrait": f"Section : {texte}",
            })

    if not resultats:
        return [{
            "titre": spring_module.nom,
            "url": spring_module.url_base,
            "extrait": (
                f"Aucun résultat pour '{requete}' dans {spring_module.nom}. "
                f"Consultez la documentation principale."
            ),
        }]

    return resultats[:10]