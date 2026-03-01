"""
Registre statique des ressources de migration Spring et Java.
Source unique de vérité — offline-first.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MigrationSource:
    nom: str
    url: str
    description: str
    tags: tuple[str, ...]


REGISTRE_MIGRATION: dict[str, MigrationSource] = {
    # ── Spring Boot ──────────────────────────────────────────────────────────
    "spring-boot-2x-3x": MigrationSource(
        nom="Spring Boot 2.x → 3.x",
        url="https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide",
        description="Guide officiel de migration Spring Boot 2.x vers 3.x. "
                    "Couvre Jakarta EE, Java 17 minimum, auto-configuration, Actuator.",
        tags=("spring-boot", "migration", "jakarta"),
    ),
    "spring-boot-3x-35": MigrationSource(
        nom="Spring Boot 3.x → 3.5",
        url="https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.5-Release-Notes",
        description="Notes de release Spring Boot 3.5. "
                    "Nouveautés, dépréciations, breaking changes.",
        tags=("spring-boot", "migration", "3.5"),
    ),
    # ── Jakarta EE ───────────────────────────────────────────────────────────
    "jakarta-javax-migration": MigrationSource(
        nom="javax → jakarta (Jakarta EE 9+)",
        url="https://docs.spring.io/spring-framework/reference/6.0-migration-guide.html",
        description="Migration des namespaces javax.* vers jakarta.*. "
                    "Concerne JPA, Servlet, Validation, Mail, etc.",
        tags=("jakarta", "javax", "migration", "spring-framework"),
    ),
    # ── Java ─────────────────────────────────────────────────────────────────
    "java-11-17": MigrationSource(
        nom="Java 11 → 17",
        url="https://docs.oracle.com/en/java/javase/17/migrate/migrating-jdk-8-later-jdk-releases.html",
        description="Migration Java 11 vers Java 17 LTS. "
                    "Sealed classes, records, pattern matching, strong encapsulation modules.",
        tags=("java", "migration", "java17"),
    ),
    "java-17-21": MigrationSource(
        nom="Java 17 → 21",
        url="https://docs.oracle.com/en/java/javase/21/migrate/index.html",
        description="Migration Java 17 vers Java 21 LTS. "
                    "Virtual threads (Loom), sequenced collections, pattern matching switch.",
        tags=("java", "migration", "java21", "virtual-threads"),
    ),
    "java-21-release-notes": MigrationSource(
        nom="Java 21 — Nouveautés complètes",
        url="https://www.oracle.com/java/technologies/javase/21-relnotes.html",
        description="Release notes officielles Java 21. "
                    "Virtual threads, record patterns, string templates (preview).",
        tags=("java", "java21", "release-notes"),
    ),
    # ── Hibernate → Spring JDBC ──────────────────────────────────────────────
    "hibernate-to-spring-jdbc": MigrationSource(
        nom="Hibernate → Spring Data JDBC",
        url="https://docs.spring.io/spring-data/jdbc/reference/",
        description="Documentation Spring Data JDBC. "
                    "Alternative légère à JPA/Hibernate. Aggregate roots, repositories.",
        tags=("hibernate", "spring-data-jdbc", "migration", "persistence"),
    ),
    "spring-data-jdbc-reference": MigrationSource(
        nom="Spring Data JDBC — Reference",
        url="https://docs.spring.io/spring-data/jdbc/reference/jdbc.html",
        description="Référence complète Spring Data JDBC : "
                    "mapping, requêtes, events, auditing.",
        tags=("spring-data-jdbc", "reference"),
    ),
    "spring-jdbc-template": MigrationSource(
        nom="JdbcTemplate — Reference",
        url="https://docs.spring.io/spring-framework/reference/data-access/jdbc.html",
        description="JdbcTemplate, NamedParameterJdbcTemplate. "
                    "Accès JDBC bas niveau sans ORM.",
        tags=("jdbc", "spring-framework", "persistence"),
    ),
    # ── OpenRewrite ──────────────────────────────────────────────────────────
    "openrewrite-spring-boot-3": MigrationSource(
        nom="OpenRewrite — Migrate to Spring Boot 3",
        url="https://docs.openrewrite.org/recipes/java/spring/boot3/springboot3bestpractices",
        description="Recettes OpenRewrite pour migrer automatiquement vers Spring Boot 3. "
                    "javax→jakarta, dépendances, auto-configuration.",
        tags=("openrewrite", "spring-boot", "migration", "automatisation"),
    ),
    "openrewrite-java-21": MigrationSource(
        nom="OpenRewrite — Migrate to Java 21",
        url="https://docs.openrewrite.org/recipes/java/migrate/upgradetojava21",
        description="Recettes OpenRewrite pour migrer le code Java vers Java 21.",
        tags=("openrewrite", "java", "java21", "migration"),
    ),
    "openrewrite-hibernate-jakarta": MigrationSource(
        nom="OpenRewrite — Hibernate javax→jakarta",
        url="https://docs.openrewrite.org/recipes/java/migrate/jakarta/javaxpersistencetojakartapersistence",
        description="Recettes OpenRewrite pour migrer javax.persistence → jakarta.persistence.",
        tags=("openrewrite", "hibernate", "jakarta", "migration"),
    ),
    # ── Spring Boot Migrator ──────────────────────────────────────────────────
    "spring-boot-migrator": MigrationSource(
        nom="Spring Boot Migrator (SBM)",
        url="https://github.com/spring-projects-experimental/spring-boot-migrator",
        description="Outil CLI de migration automatique vers Spring Boot 3. "
                    "Analyse le projet et applique des recettes de migration.",
        tags=("sbm", "spring-boot", "migration", "automatisation"),
    ),
}


def filtrer_par_tags(*tags: str) -> dict[str, MigrationSource]:
    """Retourne les sources dont au moins un tag correspond."""
    return {
        cle: source
        for cle, source in REGISTRE_MIGRATION.items()
        if any(tag in source.tags for tag in tags)
    }