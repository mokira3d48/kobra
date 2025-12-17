-- init-kbrdb.sql
-- Configuration complète pour la base kbrdb et l'utilisateur kobra

-- 1. Créer la base de données kbrdb
CREATE DATABASE kbrdb;

-- 2. Créer l'utilisateur kobra avec mot de passe chiffré
CREATE USER kobra WITH ENCRYPTED PASSWORD 'your-secret-password-here';

-- 3. Configurer l'encodage client
ALTER ROLE kobra SET client_encoding TO 'utf8';

-- 4. Configurer l'isolation des transactions
ALTER ROLE kobra SET default_transaction_isolation TO 'read committed';

-- 5. Configurer le fuseau horaire
ALTER ROLE kobra SET timezone TO 'Europe/Paris';

-- 6. Donner tous les privilèges sur la base kbrdb
GRANT ALL PRIVILEGES ON DATABASE kbrdb TO kobra;

-- 7. Configuration pour les tests Django (permission de créer des bases)
ALTER USER kobra CREATEDB;

-- Note: La ligne SUPERUSER est commentée, tu peux la décommenter si besoin
-- ALTER ROLE kobra SUPERUSER;

-- 8. Se connecter à kbrdb pour les permissions sur le schéma
\c kbrdb;

-- 9. Donner tous les droits sur le schéma public
GRANT ALL ON SCHEMA public TO kobra;

-- 10. (Optionnel) Vérification
SELECT current_database(), current_user, current_setting('timezone');
