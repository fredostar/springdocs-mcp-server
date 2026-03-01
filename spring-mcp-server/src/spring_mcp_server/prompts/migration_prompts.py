"""Templates de prompts spécialisés migration Spring/Java."""

PROMPTS_MIGRATION = {
    "analyser-code-pour-migration": {
        "description": "Analyse un extrait de code Java pour identifier les points de migration",
        "template": (
            "Tu es un expert Software Crafter spécialisé en migration Spring et Java. "
            "Analyse le code Java suivant et identifie :\n"
            "1. Les imports javax.* à migrer vers jakarta.*\n"
            "2. Les annotations JPA/Hibernate à adapter\n"
            "3. Les patterns incompatibles avec Spring Boot 3.x\n"
            "4. Les APIs Java dépréciées avant Java {version_java_cible}\n"
            "5. Les suggestions de refactoring vers des patterns modernes\n\n"
            "Code à analyser :\n{code}\n\n"
            "Réponds en français avec des suggestions concrètes et du code corrigé."
        ),
        "arguments": ["code", "version_java_cible"],
    },
    "plan-migration-projet": {
        "description": "Génère un plan de migration complet pour un projet Spring Boot",
        "template": (
            "Tu es un expert en migration Spring Boot et Java. "
            "Génère un plan de migration détaillé pour un projet avec les caractéristiques suivantes :\n\n"
            "- Version Spring Boot actuelle : {version_spring_boot_source}\n"
            "- Version Spring Boot cible : {version_spring_boot_cible}\n"
            "- Version Java actuelle : {version_java_source}\n"
            "- Version Java cible : {version_java_cible}\n"
            "- ORM actuel : {orm} (ex: Hibernate, Spring Data JPA, JDBC)\n"
            "- Modules Spring utilisés : {modules_spring}\n\n"
            "Le plan doit inclure :\n"
            "1. Ordre des étapes de migration (du moins risqué au plus risqué)\n"
            "2. Commandes OpenRewrite à exécuter\n"
            "3. Points de validation entre chaque étape\n"
            "4. Risques identifiés et stratégies de rollback\n"
            "5. Estimation de complexité par étape\n\n"
            "Respecte les principes SOLID et Clean Architecture. "
            "Réponds en français."
        ),
        "arguments": [
            "version_spring_boot_source",
            "version_spring_boot_cible",
            "version_java_source",
            "version_java_cible",
            "orm",
            "modules_spring",
        ],
    },
    "migrer-entite-jpa-vers-jdbc": {
        "description": "Convertit une entité JPA/Hibernate en aggregate Spring Data JDBC",
        "template": (
            "Tu es un expert Spring Data et Domain-Driven Design. "
            "Convertis l'entité JPA suivante en Aggregate Root Spring Data JDBC.\n\n"
            "Entité JPA source :\n{code_entite_jpa}\n\n"
            "Règles à respecter :\n"
            "1. Supprimer toutes les annotations JPA (@Entity, @Table, @Column, etc.)\n"
            "2. Identifier si c'est un Aggregate Root ou une Value Object\n"
            "3. Gérer les relations via @MappedCollection (Spring Data JDBC)\n"
            "4. Pas de lazy loading — tout est chargé eagerly\n"
            "5. Créer le Repository correspondant\n"
            "6. Ajouter le schema SQL si nécessaire\n"
            "7. Respecter les principes SOLID et Clean Architecture\n\n"
            "Réponds en français avec le code Java complet."
        ),
        "arguments": ["code_entite_jpa"],
    },
}