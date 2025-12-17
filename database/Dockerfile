# Dockerfile
# Image PostgreSQL 16 avec configuration kbrdb/kobra

# Utiliser l'image officielle PostgreSQL 16
FROM postgres:16

# Définir les métadonnées de l'image (optionnel)
LABEL maintainer="dr.mokira@gmail.com"
LABEL version="1.0"
LABEL description="PostgreSQL 16 for KOBRA"

# Copier le script de configuration dans le dossier d'initialisation
# Tous les fichiers dans /docker-entrypoint-initdb.d/ sont exécutés au premier démarrage
COPY init-kbrdb.sql /docker-entrypoint-initdb.d/

# S'assurer que le fichier a les bonnes permissions
RUN chmod 644 /docker-entrypoint-initdb.d/init-kbrdb.sql

# Exposer le port PostgreSQL par défaut
EXPOSE 5432

# L'image officielle PostgreSQL a déjà un CMD approprié
# Elle démarre automatiquement PostgreSQL avec les configurations
