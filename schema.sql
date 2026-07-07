-- ============================================================
-- Cold-Chain Expiry Accelerator - MySQL Schema
-- Database: cold_chain_db
-- ============================================================

-- ------------------------------------------------------------
-- Table: users
-- Stores application user accounts for the login system.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id        INT           NOT NULL AUTO_INCREMENT,
    username       VARCHAR(80)   NOT NULL,
    email          VARCHAR(150)  NOT NULL,
    password_hash  VARCHAR(255)  NOT NULL COMMENT 'Bcrypt hashed password',
    role           VARCHAR(20)   NOT NULL DEFAULT 'staff'
                       COMMENT 'admin | manager | staff',
    is_active      TINYINT(1)    NOT NULL DEFAULT 1,
    created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email    (email),
    INDEX idx_users_role         (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================

CREATE DATABASE IF NOT EXISTS cold_chain_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE cold_chain_db;

-- ------------------------------------------------------------
-- Table: products
-- Stores temperature-sensitive product definitions.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    product_id       INT            NOT NULL AUTO_INCREMENT,
    product_name     VARCHAR(200)   NOT NULL,
    category         VARCHAR(100)   NOT NULL,
    ideal_temperature DOUBLE        NOT NULL COMMENT 'Ideal storage temperature in Celsius',
    maximum_temperature DOUBLE      NOT NULL COMMENT 'Maximum safe temperature in Celsius',
    shelf_life_days  INT            NOT NULL COMMENT 'Default shelf life in days',

    PRIMARY KEY (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ------------------------------------------------------------
-- Table: batches
-- Tracks individual product batches and their expiry status.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS batches (
    batch_id           INT          NOT NULL AUTO_INCREMENT,
    product_id         INT          NOT NULL,
    manufacturing_date DATE         NOT NULL,
    original_expiry    DATE         NOT NULL,
    adjusted_expiry    DATE         NOT NULL COMMENT 'Expiry adjusted for temperature violations',
    quantity           INT          NOT NULL,
    status             VARCHAR(20)  NOT NULL DEFAULT 'Safe'
                           COMMENT 'Safe | Warning | Critical | Expired',

    PRIMARY KEY (batch_id),
    CONSTRAINT fk_batches_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_batches_product_id   (product_id),
    INDEX idx_batches_status       (status),
    INDEX idx_batches_adjusted_expiry (adjusted_expiry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ------------------------------------------------------------
-- Table: temperature_logs
-- Records every temperature inspection for a batch.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS temperature_logs (
    log_id          INT             NOT NULL AUTO_INCREMENT,
    batch_id        INT             NOT NULL,
    temperature     DOUBLE          NOT NULL COMMENT 'Recorded temperature in Celsius',
    recorded_at     DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        COMMENT 'UTC timestamp of the reading',
    employee_name   VARCHAR(100)    NOT NULL,
    days_deducted   DOUBLE          NOT NULL DEFAULT 0.0
                        COMMENT 'Shelf-life days deducted due to this violation',

    PRIMARY KEY (log_id),
    CONSTRAINT fk_temp_logs_batch
        FOREIGN KEY (batch_id)
        REFERENCES batches (batch_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_temp_logs_batch_id    (batch_id),
    INDEX idx_temp_logs_recorded_at (recorded_at),
    INDEX idx_temp_logs_violations  (days_deducted, recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
