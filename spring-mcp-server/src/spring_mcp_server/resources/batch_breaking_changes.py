"""
Breaking changes critiques Spring Batch 4.x → 5.x.
Données statiques pour réponse immédiate offline.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BatchBreakingChange:
    titre: str
    avant: str       # code Spring Batch 4
    apres: str       # code Spring Batch 5
    description: str
    tags: tuple[str, ...]


BATCH_BREAKING_CHANGES: list[BatchBreakingChange] = [
    # ── JobBuilderFactory / StepBuilderFactory ────────────────────────────────
    BatchBreakingChange(
        titre="Suppression de JobBuilderFactory et StepBuilderFactory",
        avant="""
@Autowired
private JobBuilderFactory jobBuilderFactory;

@Autowired
private StepBuilderFactory stepBuilderFactory;

@Bean
public Job monJob() {
    return jobBuilderFactory.get("monJob")
        .start(monStep())
        .build();
}

@Bean
public Step monStep() {
    return stepBuilderFactory.get("monStep")
        .<String, String>chunk(10)
        .reader(reader())
        .writer(writer())
        .build();
}""",
        apres="""
@Bean
public Job monJob(JobRepository jobRepository, Step monStep) {
    return new JobBuilder("monJob", jobRepository)
        .start(monStep)
        .build();
}

@Bean
public Step monStep(JobRepository jobRepository,
                    PlatformTransactionManager transactionManager) {
    return new StepBuilder("monStep", jobRepository)
        .<String, String>chunk(10, transactionManager)
        .reader(reader())
        .writer(writer())
        .build();
}""",
        description=(
            "JobBuilderFactory et StepBuilderFactory sont supprimés dans Spring Batch 5. "
            "Il faut injecter JobRepository et PlatformTransactionManager directement "
            "dans les méthodes @Bean des Jobs et Steps."
        ),
        tags=("batch-5", "breaking-change", "job-builder", "step-builder"),
    ),

    # ── JobRepository ─────────────────────────────────────────────────────────
    BatchBreakingChange(
        titre="JobRepository — nouvelle API et configuration",
        avant="""
@Bean
public JobRepository jobRepository(DataSource dataSource,
                                   PlatformTransactionManager tx)
        throws Exception {
    JobRepositoryFactoryBean factory = new JobRepositoryFactoryBean();
    factory.setDataSource(dataSource);
    factory.setTransactionManager(tx);
    factory.setDatabaseType("POSTGRES");
    factory.afterPropertiesSet();
    return factory.getObject();
}""",
        apres="""
// Spring Batch 5 : auto-configuration via Spring Boot
// Aucune configuration manuelle nécessaire si DataSource est présente.

// Si configuration personnalisée requise :
@Bean
public JobRepository jobRepository(DataSource dataSource,
                                   PlatformTransactionManager tx)
        throws Exception {
    JobRepositoryFactoryBean factory = new JobRepositoryFactoryBean();
    factory.setDataSource(dataSource);
    factory.setTransactionManager(tx);
    // databaseType auto-détecté
    factory.afterPropertiesSet();
    return factory.getObject();
}""",
        description=(
            "Dans Spring Batch 5, JobRepository est auto-configuré par Spring Boot "
            "si une DataSource est présente. La propriété databaseType est auto-détectée. "
            "La configuration manuelle n'est plus nécessaire dans la plupart des cas."
        ),
        tags=("batch-5", "breaking-change", "job-repository"),
    ),

    # ── Chunk-oriented processing ─────────────────────────────────────────────
    BatchBreakingChange(
        titre="Chunk — PlatformTransactionManager requis explicitement",
        avant="""
// Spring Batch 4 : transactionManager injecté automatiquement
return stepBuilderFactory.get("step")
    .<String, String>chunk(10)
    .reader(reader())
    .writer(writer())
    .build();""",
        apres="""
// Spring Batch 5 : transactionManager OBLIGATOIRE en paramètre de chunk()
return new StepBuilder("step", jobRepository)
    .<String, String>chunk(10, transactionManager)
    .reader(reader())
    .writer(writer())
    .build();""",
        description=(
            "Dans Spring Batch 5, le PlatformTransactionManager doit être passé "
            "explicitement à la méthode chunk(). Il n'est plus injecté automatiquement "
            "depuis le contexte Spring."
        ),
        tags=("batch-5", "breaking-change", "chunk", "transaction"),
    ),

    # ── Observability ─────────────────────────────────────────────────────────
    BatchBreakingChange(
        titre="Observability — Micrometer intégré nativement",
        avant="""
// Spring Batch 4 : pas d'observability native
// Nécessitait des listeners personnalisés pour les métriques""",
        apres="""
// Spring Batch 5 : Micrometer auto-configuré
// Ajouter la dépendance :
// implementation 'io.micrometer:micrometer-core'

// Métriques disponibles automatiquement :
// spring.batch.job.duration
// spring.batch.step.duration
// spring.batch.item.read
// spring.batch.item.write

// Configuration optionnelle :
@Bean
public BatchObservabilityBeanPostProcessor batchObservability() {
    return new BatchObservabilityBeanPostProcessor();
}""",
        description=(
            "Spring Batch 5 intègre Micrometer nativement pour l'observability. "
            "Les métriques de jobs, steps, items sont exposées automatiquement "
            "sans configuration supplémentaire si Micrometer est dans le classpath."
        ),
        tags=("batch-5", "observability", "micrometer"),
    ),

    # ── Virtual Threads ───────────────────────────────────────────────────────
    BatchBreakingChange(
        titre="Virtual Threads — TaskExecutor pour steps parallèles",
        avant="""
// Spring Batch 4 : ThreadPoolTaskExecutor classique
@Bean
public TaskExecutor taskExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(4);
    executor.setMaxPoolSize(8);
    return executor;
}""",
        apres="""
// Spring Batch 5 + Java 21 : Virtual Threads
@Bean
public TaskExecutor taskExecutor() {
    return new VirtualThreadTaskExecutor("spring-batch-");
}

// Ou via Spring Boot 3.2+ :
// spring.threads.virtual.enabled=true

// Dans le Step :
return new StepBuilder("step", jobRepository)
    .<String, String>chunk(100, transactionManager)
    .reader(reader())
    .writer(writer())
    .taskExecutor(taskExecutor())
    .build();""",
        description=(
            "Avec Java 21 et Spring Batch 5, les virtual threads peuvent remplacer "
            "le ThreadPoolTaskExecutor pour les steps parallèles. "
            "VirtualThreadTaskExecutor est disponible dans Spring Framework 6.1+."
        ),
        tags=("batch-5", "java21", "virtual-threads", "scalabilite"),
    ),
]


def batch_breaking_changes_par_tags(*tags: str) -> list[BatchBreakingChange]:
    """Retourne les breaking changes Batch correspondant aux tags."""
    return [
        bc for bc in BATCH_BREAKING_CHANGES
        if any(t in bc.tags for t in tags)
    ]