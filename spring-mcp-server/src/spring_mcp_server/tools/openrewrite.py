"""
Tool dédié aux recettes OpenRewrite pour la migration.
"""

_REWRITE_PLUGIN_VERSION = "5.34.1"
_REWRITE_SPRING_VERSION = "5.19.0"
_REWRITE_MIGRATE_JAVA_VERSION = "2.21.0"


def _plugin_xml(recette: str, artifact_id: str, artifact_version: str) -> str:
    return f"""
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>{_REWRITE_PLUGIN_VERSION}</version>
    <configuration>
        <activeRecipes>
            <recipe>{recette}</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>{artifact_id}</artifactId>
            <version>{artifact_version}</version>
        </dependency>
    </dependencies>
</plugin>"""


RECETTES_OPENREWRITE: dict[str, dict] = {
    "spring-boot-3": {
        "titre": "Migration complète vers Spring Boot 3",
        "recette": "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0",
        "description": "Migre automatiquement une application Spring Boot 2.x vers 3.x. "
                       "Inclut : javax→jakarta, mise à jour dépendances, "
                       "nouvelles auto-configurations.",
        "configuration_maven": _plugin_xml(
            "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0",
            "rewrite-spring",
            _REWRITE_SPRING_VERSION,
        ),
        "commande": "mvn rewrite:run",
    },
    "spring-boot-35": {
        "titre": "Migration vers Spring Boot 3.5",
        "recette": "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5",
        "description": "Migre vers Spring Boot 3.5. "
                       "Nécessite d'avoir appliqué la migration 3.0 au préalable.",
        "configuration_maven": _plugin_xml(
            "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5",
            "rewrite-spring",
            _REWRITE_SPRING_VERSION,
        ),
        "commande": "mvn rewrite:run",
    },
    "java-21": {
        "titre": "Migration vers Java 21",
        "recette": "org.openrewrite.java.migrate.UpgradeToJava21",
        "description": "Migre le code source vers Java 21. "
                       "Adopte les nouvelles APIs, supprime les usages dépréciés.",
        "configuration_maven": _plugin_xml(
            "org.openrewrite.java.migrate.UpgradeToJava21",
            "rewrite-migrate-java",
            _REWRITE_MIGRATE_JAVA_VERSION,
        ),
        "commande": "mvn rewrite:run",
    },
    "jakarta": {
        "titre": "Migration javax → jakarta",
        "recette": "org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta",
        "description": "Renomme tous les imports javax.* en jakarta.*. "
                       "Couvre JPA, Servlet, Validation, Mail, etc.",
        "configuration_maven": _plugin_xml(
            "org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta",
            "rewrite-migrate-java",
            _REWRITE_MIGRATE_JAVA_VERSION,
        ),
        "commande": "mvn rewrite:run",
    },
}


def generer_config_openrewrite(type_migration: str) -> str:
    """Retourne la configuration Maven OpenRewrite pour un type de migration."""
    if type_migration not in RECETTES_OPENREWRITE:
        disponibles = ", ".join(RECETTES_OPENREWRITE.keys())
        return f"Migration '{type_migration}' non disponible. Disponibles : {disponibles}"

    recette = RECETTES_OPENREWRITE[type_migration]
    return (
        f"# OpenRewrite — {recette['titre']}\n\n"
        f"**Recette** : `{recette['recette']}`\n\n"
        f"**Description** : {recette['description']}\n\n"
        f"## Configuration Maven\n"
        f"```xml{recette['configuration_maven']}```\n\n"
        f"## Lancement\n"
        f"```bash\n{recette['commande']}\n```\n\n"
        f"⚠️ **Toujours lancer en dry-run d'abord** :\n"
        f"```bash\nmvn rewrite:dryRun\n```"
    )