"""Templates de prompts pour les interactions Spring — composable, domain-based."""

PROMPTS_SPRING = {
    "migration-spring-boot": {
        "description": "Aide à la migration vers une version de Spring Boot",
        "template": (
            "Tu es un expert Spring Boot. "
            "Aide à migrer une application de Spring Boot {version_source} "
            "vers Spring Boot {version_cible}. "
            "Concentre-toi sur les breaking changes, les dépendances à mettre à jour "
            "et les patterns de code à adapter. "
            "Réponds en français."
        ),
        "arguments": ["version_source", "version_cible"],
    },
    "architecture-hexagonale-spring": {
        "description": "Guide pour implémenter l'architecture hexagonale avec Spring",
        "template": (
            "Tu es un Software Crafter expert Spring. "
            "Explique comment implémenter l'architecture hexagonale (ports & adapters) "
            "dans une application Spring Boot, en respectant SOLID et Clean Architecture. "
            "Donne des exemples concrets de code Java. "
            "Réponds en français."
        ),
        "arguments": [],
    },
    "supprimer-hibernate": {
        "description": "Guide pour remplacer Hibernate par du JDBC natif",
        "template": (
            "Tu es un expert Spring Data. "
            "Explique comment remplacer Hibernate/JPA par Spring JDBC ou Spring Data JDBC "
            "dans une application Spring Boot, pour l'entité {nom_entite}. "
            "Respecte les principes SOLID et Clean Architecture. "
            "Réponds en français."
        ),
        "arguments": ["nom_entite"],
    },
}