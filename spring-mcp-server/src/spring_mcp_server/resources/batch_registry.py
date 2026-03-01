"""
Registre statique des sources de documentation Spring Batch.
Offline-first — complété par fetch dynamique à la demande.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BatchMigrationSource:
    nom: str
    url: str
    description: str
    tags: tuple[str, ...]


REGISTRE_BATCH: dict[str, BatchMigrationSource] = {
    # ── Spring Batch 4 → 5 ───────────────────────────────────────────────────
    "spring-batch-4-5-migration": BatchMigrationSource(
        nom="Spring Batch 4.x → 5.x — Migration Guide officiel",
        url="https://github.com/spring-projects/spring-batch/wiki/Spring-Batch-5.0-Migration-Guide",
        description=(
            "Guide officiel de migration Spring Batch 4.x vers 5.x. "
            "Couvre la suppression de JobBuilderFactory/StepBuilderFactory, "
            "la refonte de JobRepository, le nouveau modèle de configuration."
        ),
        tags=("spring-batch", "migration", "batch-5", "breaking-change"),
    ),
    "spring-batch-5-reference": BatchMigrationSource(
        nom="Spring Batch 5 — Documentation de référence",
        url="https://docs.spring.io/spring-batch/reference/",
        description=(
            "Documentation complète Spring Batch 5. "
            "Job, Step, Chunk, ItemReader/Writer/Processor, JobRepository, "
            "Observability, Virtual Threads."
        ),
        tags=("spring-batch", "reference", "batch-5"),
    ),
    "spring-batch-52-release-notes": BatchMigrationSource(
        nom="Spring Batch 5.2 — Release Notes",
        url="https://github.com/spring-projects/spring-batch/releases/tag/5.2.0",
        description=(
            "Notes de release Spring Batch 5.2. "
            "Nouveautés, dépréciations, breaking changes mineurs."
        ),
        tags=("spring-batch", "migration", "batch-5.2"),
    ),
    # ── Observability ─────────────────────────────────────────────────────────
    "spring-batch-observability": BatchMigrationSource(
        nom="Spring Batch 5 — Observability avec Micrometer",
        url="https://docs.spring.io/spring-batch/reference/monitoring-and-metrics.html",
        description=(
            "Intégration Micrometer dans Spring Batch 5. "
            "Métriques de jobs/steps, traces, health indicators."
        ),
        tags=("spring-batch", "observability", "micrometer", "batch-5"),
    ),
    # ── Java 21 + Spring Batch ─────────────────────────────────────────────────
    "spring-batch-virtual-threads": BatchMigrationSource(
        nom="Spring Batch 5 — Virtual Threads (Java 21)",
        url="https://docs.spring.io/spring-batch/reference/scalability.html",
        description=(
            "Scalabilité Spring Batch avec les virtual threads Java 21. "
            "TaskExecutor, parallel steps, async processing."
        ),
        tags=("spring-batch", "java21", "virtual-threads", "scalabilite"),
    ),
    # ── OpenRewrite ───────────────────────────────────────────────────────────
    "openrewrite-spring-batch-5": BatchMigrationSource(
        nom="OpenRewrite — Migrate to Spring Batch 5",
        url="https://docs.openrewrite.org/recipes/java/spring/batch/springbatch4to5migration",
        description=(
            "Recettes OpenRewrite pour migrer automatiquement "
            "de Spring Batch 4 vers Spring Batch 5."
        ),
        tags=("openrewrite", "spring-batch", "migration", "automatisation"),
    ),
}


def filtrer_batch_par_tags(*tags: str) -> dict[str, BatchMigrationSource]:
    """Retourne les sources Batch dont au moins un tag correspond."""
    return {
        cle: source
        for cle, source in REGISTRE_BATCH.items()
        if any(tag in source.tags for tag in tags)
    }