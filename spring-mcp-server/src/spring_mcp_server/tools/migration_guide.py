"""
Tool principal : génération de guide de migration étape par étape.
Combine données statiques + fetch dynamique.
"""

from spring_mcp_server.resources.migration_registry import (
    REGISTRE_MIGRATION,
    filtrer_par_tags,
)
from spring_mcp_server.resources.breaking_changes import breaking_changes_par_tags
from spring_mcp_server.tools.fetch_page import recuperer_contenu_doc


MIGRATIONS_SUPPORTEES = {
    "spring-boot-2-3": {
        "titre": "Spring Boot 2.x → 3.x",
        "tags": ("spring-boot-3", "jakarta", "hibernate"),
        "sources_cles": ["spring-boot-2x-3x", "jakarta-javax-migration", "openrewrite-spring-boot-3"],
        "etapes": [
            "1. Mettre à jour Java vers 17 minimum (21 recommandé)",
            "2. Migrer javax.* → jakarta.* (OpenRewrite ou sed)",
            "3. Mettre à jour spring-boot-starter-parent vers 3.x",
            "4. Vérifier les auto-configurations (spring.factories → .imports)",
            "5. Tester HikariCP datasource properties",
            "6. Vérifier les changements Hibernate 6",
            "7. Mettre à jour Spring Security si utilisé",
            "8. Lancer la suite de tests complète",
        ],
    },
    "java-11-21": {
        "titre": "Java 11 → 21",
        "tags": ("java17", "java21", "virtual-threads"),
        "sources_cles": ["java-11-17", "java-17-21", "openrewrite-java-21"],
        "etapes": [
            "1. Migrer Java 11 → 17 d'abord (LTS intermédiaire)",
            "2. Corriger les accès aux APIs internes JDK (--add-opens)",
            "3. Adopter les records pour les value objects",
            "4. Utiliser les sealed classes pour les hiérarchies fermées",
            "5. Migrer vers Java 21",
            "6. Évaluer l'adoption des virtual threads (Spring Boot 3.2+)",
            "7. Remplacer synchronized par ReentrantLock si virtual threads",
        ],
    },
    "hibernate-spring-data-jdbc": {
        "titre": "Hibernate/JPA → Spring Data JDBC",
        "tags": ("hibernate", "spring-data-jdbc", "ddd"),
        "sources_cles": ["hibernate-to-spring-jdbc", "spring-data-jdbc-reference", "spring-jdbc-template"],
        "etapes": [
            "1. Identifier les Aggregate Roots du domaine métier",
            "2. Supprimer les annotations JPA (@Entity, @OneToMany, etc.)",
            "3. Créer les interfaces Repository Spring Data JDBC",
            "4. Gérer les relations via @MappedCollection",
            "5. Remplacer JPQL par des requêtes @Query SQL natif",
            "6. Supprimer les dépendances spring-boot-starter-data-jpa",
            "7. Ajouter spring-boot-starter-data-jdbc",
            "8. Migrer les tests (pas de EntityManager)",
        ],
    },
    "jakarta-javax": {
        "titre": "javax → jakarta",
        "tags": ("jakarta", "javax"),
        "sources_cles": ["jakarta-javax-migration", "openrewrite-hibernate-jakarta"],
        "etapes": [
            "1. Auditer tous les imports javax.* dans le projet",
            "2. Appliquer la recette OpenRewrite JavaxMigrationToJakarta",
            "3. Mettre à jour les dépendances (Jakarta EE 9+ artifacts)",
            "4. Vérifier les fichiers de configuration XML (persistence.xml, web.xml)",
            "5. Tester l'ensemble des endpoints et la persistance",
        ],
    },
}


async def generer_guide_migration(type_migration: str, avec_contenu_officiel: bool = False) -> str:
    """
    Génère un guide de migration complet.
    Combine étapes statiques + breaking changes + fetch optionnel des guides officiels.
    """
    if type_migration not in MIGRATIONS_SUPPORTEES:
        types_disponibles = ", ".join(MIGRATIONS_SUPPORTEES.keys())
        return (
            f"Type de migration '{type_migration}' non supporté.\n"
            f"Types disponibles : {types_disponibles}"
        )

    migration = MIGRATIONS_SUPPORTEES[type_migration]
    lignes = [f"# Guide de migration : {migration['titre']}\n"]

    # Étapes statiques
    lignes.append("## Étapes de migration\n")
    lignes.extend(f"{etape}" for etape in migration["etapes"])

    # Breaking changes correspondants
    bcs = breaking_changes_par_tags(*migration["tags"])
    if bcs:
        lignes.append("\n## ⚠️ Breaking changes critiques\n")
        for bc in bcs:
            lignes.append(f"### {bc.titre}")
            lignes.append(f"**Problème** : {bc.description}")
            lignes.append(f"**Solution** : {bc.solution}\n")

    # Sources de référence
    lignes.append("\n## Sources officielles\n")
    for cle in migration["sources_cles"]:
        if cle in REGISTRE_MIGRATION:
            source = REGISTRE_MIGRATION[cle]
            lignes.append(f"- **{source.nom}** : {source.url}")

    # Fetch optionnel du contenu officiel
    if avec_contenu_officiel and migration["sources_cles"]:
        source_principale = REGISTRE_MIGRATION.get(migration["sources_cles"][0])
        if source_principale:
            lignes.append(f"\n## Contenu officiel — {source_principale.nom}\n")
            contenu = await recuperer_contenu_doc(source_principale.url)
            lignes.append(contenu[:3000])

    return "\n".join(lignes)