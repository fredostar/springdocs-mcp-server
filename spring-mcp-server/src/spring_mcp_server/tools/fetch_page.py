"""Tool de récupération d'une page de documentation Spring."""

import httpx
from bs4 import BeautifulSoup


async def recuperer_contenu_doc(url: str) -> str:
    """Récupère et nettoie le contenu textuel d'une page de doc Spring."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            reponse = await client.get(url, follow_redirects=True)
            reponse.raise_for_status()
    except httpx.HTTPStatusError as e:
        return f"Erreur HTTP {e.response.status_code} lors de l'accès à : {url}"
    except httpx.RequestError:
        return f"Impossible d'accéder à : {url}"

    soup = BeautifulSoup(reponse.text, "html.parser")

    # Supprime nav, scripts, styles — garde le contenu principal
    for balise in soup(["nav", "script", "style", "footer", "header"]):
        balise.decompose()

    contenu = soup.find("article") or soup.find("main") or soup.body
    if contenu is None:
        return "Contenu introuvable."

    return contenu.get_text(separator="\n", strip=True)[:8000]