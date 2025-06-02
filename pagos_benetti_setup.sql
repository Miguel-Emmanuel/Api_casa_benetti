-- Crear base de datos
CREATE DATABASE IF NOT EXISTS pagos_benetti CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario y otorgar permisos (cambia la contraseña por seguridad)
CREATE USER IF NOT EXISTS 'benetti_user'@'localhost' IDENTIFIED BY 'TuPasswordSegura123';
GRANT ALL PRIVILEGES ON pagos_benetti.* TO 'benetti_user'@'localhost';
FLUSH PRIVILEGES;

-- Puedes ejecutar este script en tu consola MySQL:
-- mysql -u root -p < pagos_benetti_setup.sql
