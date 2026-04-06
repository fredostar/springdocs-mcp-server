"""
Guide de migration Spring Batch — étapes + breaking changes + sources.
Combine données statiques et fetch dynamique.
"""

from spring_mcp_server.resources.batch_registry import REGISTRE_BATCH
from spring_mcp_server.resources.batch_breaking_changes import (
    batch_breaking_changes_par_tags,
)
from spring_mcp_server.tools.fetch_page import recuperer_contenu_doc


MIGRATIONS_BATCH_SUPPORTEES: dict[str, dict] = {
    "spring-batch-4-5": {
        "titre": "Spring Batch 4.x → 5.x",
        "tags": ("batch-5", "breaking-change", "job-builder", "chunk", "job-repository"),
        "sources_cles": [
            "spring-batch-4-5-migration",
            "openrewrite-spring-batch-5",
            "spring-batch-5-reference",
        ],
        "etapes": [
            "1.  Mettre à jour spring-boot-starter-parent vers 3.x (embarque Batch 5)",
            "2.  Remplacer JobBuilderFactory → JobBuilder(name, jobRepository)",
            "3.  Remplacer StepBuilderFactory → StepBuilder(name, jobRepository)",
            "4.  Ajouter PlatformTransactionManager en paramètre de chunk()",
            "5.  Supprimer la configuration manuelle de JobRepository si Spring Boot gère la DataSource",
            "6.  Migrer javax.* → jakarta.* (Spring Boot 3 requis)",
            "7.  Ajouter Micrometer si observability souhaitée",
            "8.  Évaluer VirtualThreadTaskExecutor si Java 21",
            "9.  Lancer OpenRewrite SpringBatch4To5Migration",
            "10. Valider les tests d'intégration JobLauncherTestUtils",
        ],
    },
    "spring-batch-5-52": {
        "titre": "Spring Batch 5.x → 5.2+",
        "tags": ("batch-5.2", "observability", "micrometer"),
        "sources_cles": [
            "spring-batch-52-release-notes",
            "spring-batch-observability",
        ],
        "etapes": [
            "1. Mettre à jour spring-boot-starter-parent vers 3.3+",
            "2. Vérifier les dépréciations introduites en 5.1",
            "3. Configurer l'observability Micrometer si pas encore fait",
            "4. Tester la compatibilité des ItemReader/Writer personnalisés",
        ],
    },
    "spring-batch-java21": {
        "titre": "Spring Batch + Java 21 — Modernisation",
        "tags": ("java21", "virtual-threads", "scalabilite"),
        "sources_cles": [
            "spring-batch-virtual-threads",
            "spring-batch-5-reference",
        ],
        "etapes": [
            "1. Passer à Java 21 (voir guide java-11-21)",
            "2. Activer spring.threads.virtual.enabled=true dans application.properties",
            "3. Remplacer ThreadPoolTaskExecutor par VirtualThreadTaskExecutor",
            "4. Convertir les value objects Batch en records Java",
            "5. Tester la scalabilité des steps parallèles avec virtual threads",
            "6. Vérifier l'absence de blocs synchronized avec I/O bloquante",
        ],
    },
}


async def generer_guide_batch(
        type_migration: str,
        avec_contenu_officiel: bool = False,
) -> str:
    """
    Génère un guide de migration Spring Batch complet.
    Inclut étapes, breaking changes avec exemples de code, et sources.
    """
    if type_migration not in MIGRATIONS_BATCH_SUPPORTEES:
        disponibles = ", ".join(MIGRATIONS_BATCH_SUPPORTEES.keys())
        return (
            f"Migration Batch '{type_migration}' non supportée.\n"
            f"Migrations disponibles : {disponibles}"
        )

    migration = MIGRATIONS_BATCH_SUPPORTEES[type_migration]
    lignes = [f"# Guide de migration Spring Batch : {migration['titre']}\n"]

    # Étapes
    lignes.append("## Étapes de migration\n")
    lignes.extend(migration["etapes"])

    # Breaking changes avec exemples de code
    bcs = batch_breaking_changes_par_tags(*migration["tags"])
    if bcs:
        lignes.append("\n## ⚠️ Breaking changes détaillés\n")
        for bc in bcs:
            lignes.append(bc.to_markdown())

    # Sources officielles
    lignes.append("\n## Sources officielles\n")
    for cle in migration["sources_cles"]:
        if cle in REGISTRE_BATCH:
            source = REGISTRE_BATCH[cle]
            lignes.append(f"- **{source.nom}** : {source.url}")

    # Fetch optionnel
    if avec_contenu_officiel and migration["sources_cles"]:
        source_principale = REGISTRE_BATCH.get(migration["sources_cles"][0])
        if source_principale:
            lignes.append(f"\n## Contenu officiel — {source_principale.nom}\n")
            contenu = await recuperer_contenu_doc(source_principale.url)
            lignes.append(contenu[:3000])

    return "\n".join(lignes)