"""Templates de prompts spécialisés migration Spring Batch."""

PROMPTS_BATCH = {
    "migrer-job-batch-4-vers-5": {
        "description": "Convertit une configuration de Job Spring Batch 4 vers Spring Batch 5",
        "template": (
            "Tu es un expert Spring Batch et Software Crafter. "
            "Migre la configuration Spring Batch 4 suivante vers Spring Batch 5.\n\n"
            "Configuration Spring Batch 4 :\n{code_batch_4}\n\n"
            "Règles obligatoires :\n"
            "1. Remplacer JobBuilderFactory par JobBuilder(name, jobRepository)\n"
            "2. Remplacer StepBuilderFactory par StepBuilder(name, jobRepository)\n"
            "3. Ajouter PlatformTransactionManager en paramètre de chunk()\n"
            "4. Injecter jobRepository et transactionManager via les paramètres @Bean\n"
            "5. Supprimer tout @Autowired sur les factories\n"
            "6. Respecter SOLID et Clean Architecture\n\n"
            "Réponds en français avec le code Java 21 complet et les explications."
        ),
        "arguments": ["code_batch_4"],
    },
    "analyser-job-pour-migration": {
        "description": "Analyse un Job Spring Batch pour identifier les points de migration",
        "template": (
            "Tu es un expert Spring Batch. "
            "Analyse ce code Spring Batch et identifie tous les points nécessitant "
            "une migration vers Spring Batch 5 :\n\n"
            "{code_job}\n\n"
            "Pour chaque point identifié, indique :\n"
            "1. Le problème exact\n"
            "2. Le niveau de risque (FAIBLE / MOYEN / ÉLEVÉ)\n"
            "3. La correction à apporter avec exemple de code\n"
            "4. Si OpenRewrite peut l'automatiser\n\n"
            "Réponds en français."
        ),
        "arguments": ["code_job"],
    },
    "optimiser-batch-virtual-threads": {
        "description": "Optimise un Step Spring Batch pour utiliser les virtual threads Java 21",
        "template": (
            "Tu es un expert Spring Batch et Java 21. "
            "Optimise ce Step Spring Batch pour tirer parti des virtual threads Java 21 :\n\n"
            "{code_step}\n\n"
            "Vérifie et adapte :\n"
            "1. Remplacer ThreadPoolTaskExecutor par VirtualThreadTaskExecutor\n"
            "2. Identifier les blocs synchronized problématiques avec les virtual threads\n"
            "3. Remplacer synchronized par ReentrantLock si nécessaire\n"
            "4. Vérifier la thread-safety des ItemReader/Writer\n"
            "5. Configurer le throttle-limit si nécessaire\n\n"
            "Respecte SOLID et Clean Architecture. "
            "Réponds en français avec le code Java 21 complet."
        ),
        "arguments": ["code_step"],
    },
}