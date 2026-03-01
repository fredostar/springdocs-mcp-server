"""
Breaking changes critiques par migration — données statiques.
Permet une réponse immédiate sans fetch réseau.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BreakingChange:
    titre: str
    description: str
    solution: str
    tags: tuple[str, ...]


BREAKING_CHANGES: list[BreakingChange] = [
    # ── Jakarta EE ───────────────────────────────────────────────────────────
    BreakingChange(
        titre="javax.* → jakarta.*",
        description="Spring Boot 3 requiert Jakarta EE 9+. "
                    "Tous les imports javax.persistence, javax.servlet, "
                    "javax.validation doivent être renommés.",
        solution="Utiliser OpenRewrite : org.openrewrite.java.migrate.jakarta."
                 "JavaxMigrationToJakarta. "
                 "Ou sed global : sed -i 's/javax\\./jakarta\\./g'",
        tags=("jakarta", "spring-boot-3", "hibernate"),
    ),
    # ── Spring Boot 3 ─────────────────────────────────────────────────────────
    BreakingChange(
        titre="Java 17 minimum requis",
        description="Spring Boot 3.x requiert Java 17 au minimum. "
                    "Spring Boot 3.2+ recommande Java 21.",
        solution="Mettre à jour le toolchain Maven/Gradle : "
                 "<java.version>17</java.version>",
        tags=("spring-boot-3", "java"),
    ),
    BreakingChange(
        titre="spring.datasource.* → HikariCP properties",
        description="Certaines propriétés de datasource ont changé de préfixe "
                    "ou sont dépréciées dans Spring Boot 3.",
        solution="Consulter le Spring Boot 3 Migration Guide section 'DataSource'. "
                 "Utiliser spring.datasource.hikari.* pour les propriétés HikariCP.",
        tags=("spring-boot-3", "datasource", "hikari"),
    ),
    BreakingChange(
        titre="@SpringBootTest — détection auto-configuration",
        description="Le mécanisme de détection des auto-configurations a changé "
                    "dans Spring Boot 3. Les fichiers spring.factories sont remplacés "
                    "par META-INF/spring/org.springframework.boot."
                    "autoconfigure.AutoConfiguration.imports",
        solution="Migrer les fichiers spring.factories vers le nouveau format "
                 "ou utiliser OpenRewrite.",
        tags=("spring-boot-3", "auto-configuration", "test"),
    ),
    # ── Hibernate ─────────────────────────────────────────────────────────────
    BreakingChange(
        titre="Hibernate 6 — changements de comportement",
        description="Spring Boot 3 embarque Hibernate 6. "
                    "Changements : génération SQL, naming strategy, types.",
        solution="Vérifier les requêtes JPQL générées. "
                 "Tester les mappings @Column(name=...). "
                 "Consulter le Hibernate 6 Migration Guide.",
        tags=("hibernate", "spring-boot-3", "persistence"),
    ),
    BreakingChange(
        titre="Suppression de Hibernate — Aggregate Root pattern",
        description="Lors du remplacement de Hibernate par Spring Data JDBC, "
                    "il faut adopter le pattern Aggregate Root. "
                    "Pas de lazy loading, pas de cascade automatique.",
        solution="Identifier les Aggregate Roots du domaine. "
                 "Implémenter les repositories Spring Data JDBC. "
                 "Gérer explicitement les relations via @MappedCollection.",
        tags=("hibernate", "spring-data-jdbc", "migration", "ddd"),
    ),
    # ── Java 21 ───────────────────────────────────────────────────────────────
    BreakingChange(
        titre="Strong encapsulation JDK internals",
        description="Java 17+ bloque l'accès aux APIs internes du JDK "
                    "(sun.*, com.sun.*). Certaines libs peuvent être impactées.",
        solution="Ajouter --add-opens si nécessaire temporairement. "
                 "Mettre à jour les dépendances qui utilisent ces APIs.",
        tags=("java17", "java21", "modules"),
    ),
    BreakingChange(
        titre="Virtual threads et synchronized",
        description="Java 21 virtual threads (Loom) peuvent être épinglés "
                    "sur un carrier thread si un bloc synchronized est utilisé "
                    "avec des opérations bloquantes.",
        solution="Remplacer synchronized par ReentrantLock dans les sections "
                 "critiques avec I/O bloquante pour bénéficier pleinement "
                 "des virtual threads.",
        tags=("java21", "virtual-threads", "loom"),
    ),
]


def breaking_changes_par_tags(*tags: str) -> list[BreakingChange]:
    """Retourne les breaking changes correspondant aux tags demandés."""
    return [bc for bc in BREAKING_CHANGES if any(t in bc.tags for t in tags)]