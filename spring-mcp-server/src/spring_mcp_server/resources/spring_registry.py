"""Registre statique de la documentation Spring — idiomatic, predictable."""

from dataclasses import dataclass

@dataclass(frozen=True)
class SpringModule:
    nom: str
    url_base: str
    description: str

REGISTRE_SPRING: dict[str, SpringModule] = {
    "spring-framework": SpringModule(
        nom="Spring Framework",
        url_base="https://docs.spring.io/spring-framework/reference/",
        description="Noyau du framework : IoC, AOP, MVC, JDBC...",
    ),
    "spring-boot": SpringModule(
        nom="Spring Boot",
        url_base="https://docs.spring.io/spring-boot/docs/current/reference/html/",
        description="Auto-configuration, starters, Actuator...",
    ),
    "spring-data": SpringModule(
        nom="Spring Data JPA",
        url_base="https://docs.spring.io/spring-data/jpa/reference/",
        description="Repositories, requêtes dérivées, JPQL...",
    ),
    "spring-security": SpringModule(
        nom="Spring Security",
        url_base="https://docs.spring.io/spring-security/reference/",
        description="Authentification, autorisation, OAuth2...",
    ),
    "spring-ai": SpringModule(
        nom="Spring AI",
        url_base="https://docs.spring.io/spring-ai/reference/",
        description="Intégration LLM, MCP, RAG, embeddings...",
    ),
}