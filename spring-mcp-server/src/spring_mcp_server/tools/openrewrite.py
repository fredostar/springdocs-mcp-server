"""
Tool dédié aux recettes OpenRewrite pour la migration.
"""

RECETTES_OPENREWRITE: dict[str, dict] = {
    "spring-boot-3": {
        "titre": "Migration complète vers Spring Boot 3",
        "recette": "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0",
        "description": "Migre automatiquement une application Spring Boot 2.x vers 3.x. "
                       "Inclut : javax→jakarta, mise à jour dépendances, "
                       "nouvelles auto-configurations.",
        "configuration_maven": """
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>5.34.1</version>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-spring</artifactId>
            <version>5.19.0</version>
        </dependency>
    </dependencies>
</plugin>""",
        "commande": "mvn rewrite:run",
    },
    "spring-boot-35": {
        "titre": "Migration vers Spring Boot 3.5",
        "recette": "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5",
        "description": "Migre vers Spring Boot 3.5. "
                       "Nécessite d'avoir appliqué la migration 3.0 au préalable.",
        "configuration_maven": """
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>5.34.1</version>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-spring</artifactId>
            <version>5.19.0</version>
        </dependency>
    </dependencies>
</plugin>""",
        "commande": "mvn rewrite:run",
    },
    "java-21": {
        "titre": "Migration vers Java 21",
        "recette": "org.openrewrite.java.migrate.UpgradeToJava21",
        "description": "Migre le code source vers Java 21. "
                       "Adopte les nouvelles APIs, supprime les usages dépréciés.",
        "configuration_maven": """
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>5.34.1</version>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.migrate.UpgradeToJava21</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-migrate-java</artifactId>
            <version>2.21.0</version>
        </dependency>
    </dependencies>
</plugin>""",
        "commande": "mvn rewrite:run",
    },
    "jakarta": {
        "titre": "Migration javax → jakarta",
        "recette": "org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta",
        "description": "Renomme tous les imports javax.* en jakarta.*. "
                       "Couvre JPA, Servlet, Validation, Mail, etc.",
        "configuration_maven": """
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>5.34.1</version>
    <configuration>
        <activeRecipes>
            <recipe>
                org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta
            </recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-migrate-java</artifactId>
            <version>2.21.0</version>
        </dependency>
    </dependencies>
</plugin>""",
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