-- ============================================
-- BASE DE DATOS MEJORADA CON TEMA DINOSAURIOS
-- ============================================

-- ============================================
-- TABLA: ERAS (Períodos geológicos)
-- ============================================
CREATE TABLE IF NOT EXISTS eras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    periodo_inicio INT COMMENT 'Millones de años',
    periodo_fin INT COMMENT 'Millones de años',
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
);

-- ============================================
-- TABLA: REGIONES (Localizaciones geográficas)
-- ============================================
CREATE TABLE IF NOT EXISTS regiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    pais VARCHAR(100),
    continente VARCHAR(50),
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
);

-- ============================================
-- TABLA: HABITATS (Tipos de entornos)
-- ============================================
CREATE TABLE IF NOT EXISTS habitats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    tipo_ambiente VARCHAR(50),
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
);

-- ============================================
-- TABLA: DINOSAURIOS (Mejorada)
-- ============================================
CREATE TABLE IF NOT EXISTS dinosaurios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(100),
    peso_kg DECIMAL(10, 2) COMMENT 'Peso en kilogramos',
    altura_metros DECIMAL(5, 2) COMMENT 'Altura en metros',
    longitud_metros DECIMAL(5, 2) COMMENT 'Longitud en metros',
    dieta VARCHAR(50) COMMENT 'Herbívoro, Carnívoro, Omnívoro',
    era_id INT,
    region_id INT,
    creador_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (era_id) REFERENCES eras(id) ON DELETE SET NULL,
    FOREIGN KEY (region_id) REFERENCES regiones(id) ON DELETE SET NULL,
    FOREIGN KEY (creador_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_nombre (nombre),
    INDEX idx_tipo (tipo),
    INDEX idx_era_id (era_id),
    INDEX idx_region_id (region_id)
);

-- ============================================
-- ACTUALIZAR TABLA DINOSAURIOS (si era antigua)
-- ============================================
-- Añadir columna descripcion si no existe
SET @col_desc := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'descripcion'
);
SET @sql_desc := IF(
    @col_desc = 0,
    'ALTER TABLE dinosaurios ADD COLUMN descripcion TEXT',
    'DO 1'
);
PREPARE stmt_desc FROM @sql_desc;
EXECUTE stmt_desc;
DEALLOCATE PREPARE stmt_desc;

-- Añadir columna tipo si no existe
SET @col_tipo := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'tipo'
);
SET @sql_tipo := IF(
    @col_tipo = 0,
    'ALTER TABLE dinosaurios ADD COLUMN tipo VARCHAR(100)',
    'DO 1'
);
PREPARE stmt_tipo FROM @sql_tipo;
EXECUTE stmt_tipo;
DEALLOCATE PREPARE stmt_tipo;

-- Añadir columna peso_kg si no existe
SET @col_peso := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'peso_kg'
);
SET @sql_peso := IF(
    @col_peso = 0,
    'ALTER TABLE dinosaurios ADD COLUMN peso_kg DECIMAL(10,2)',
    'DO 1'
);
PREPARE stmt_peso FROM @sql_peso;
EXECUTE stmt_peso;
DEALLOCATE PREPARE stmt_peso;

-- Añadir columna altura_metros si no existe
SET @col_altura := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'altura_metros'
);
SET @sql_altura := IF(
    @col_altura = 0,
    'ALTER TABLE dinosaurios ADD COLUMN altura_metros DECIMAL(5,2)',
    'DO 1'
);
PREPARE stmt_altura FROM @sql_altura;
EXECUTE stmt_altura;
DEALLOCATE PREPARE stmt_altura;

-- Añadir columna longitud_metros si no existe
SET @col_long := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'longitud_metros'
);
SET @sql_long := IF(
    @col_long = 0,
    'ALTER TABLE dinosaurios ADD COLUMN longitud_metros DECIMAL(5,2)',
    'DO 1'
);
PREPARE stmt_long FROM @sql_long;
EXECUTE stmt_long;
DEALLOCATE PREPARE stmt_long;

-- Añadir columna dieta si no existe
SET @col_dieta := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'dieta'
);
SET @sql_dieta := IF(
    @col_dieta = 0,
    'ALTER TABLE dinosaurios ADD COLUMN dieta VARCHAR(50)',
    'DO 1'
);
PREPARE stmt_dieta FROM @sql_dieta;
EXECUTE stmt_dieta;
DEALLOCATE PREPARE stmt_dieta;

-- Añadir columna era_id si no existe
SET @col_era := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'era_id'
);
SET @sql_era := IF(
    @col_era = 0,
    'ALTER TABLE dinosaurios ADD COLUMN era_id INT',
    'DO 1'
);
PREPARE stmt_era FROM @sql_era;
EXECUTE stmt_era;
DEALLOCATE PREPARE stmt_era;

-- Añadir columna region_id si no existe
SET @col_region := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'region_id'
);
SET @sql_region := IF(
    @col_region = 0,
    'ALTER TABLE dinosaurios ADD COLUMN region_id INT',
    'DO 1'
);
PREPARE stmt_region FROM @sql_region;
EXECUTE stmt_region;
DEALLOCATE PREPARE stmt_region;

-- Añadir columna creador_id si no existe
SET @col_creador := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND COLUMN_NAME = 'creador_id'
);
SET @sql_creador := IF(
    @col_creador = 0,
    'ALTER TABLE dinosaurios ADD COLUMN creador_id INT',
    'DO 1'
);
PREPARE stmt_creador FROM @sql_creador;
EXECUTE stmt_creador;
DEALLOCATE PREPARE stmt_creador;

-- Crear índices si no existen
SET @idx_tipo := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND INDEX_NAME = 'idx_tipo'
);
SET @sql_idx_tipo := IF(
    @idx_tipo = 0,
    'CREATE INDEX idx_tipo ON dinosaurios(tipo)',
    'DO 1'
);
PREPARE stmt_idx_tipo FROM @sql_idx_tipo;
EXECUTE stmt_idx_tipo;
DEALLOCATE PREPARE stmt_idx_tipo;

SET @idx_era := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND INDEX_NAME = 'idx_era_id'
);
SET @sql_idx_era := IF(
    @idx_era = 0,
    'CREATE INDEX idx_era_id ON dinosaurios(era_id)',
    'DO 1'
);
PREPARE stmt_idx_era FROM @sql_idx_era;
EXECUTE stmt_idx_era;
DEALLOCATE PREPARE stmt_idx_era;

SET @idx_region := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'dinosaurios'
      AND INDEX_NAME = 'idx_region_id'
);
SET @sql_idx_region := IF(
    @idx_region = 0,
    'CREATE INDEX idx_region_id ON dinosaurios(region_id)',
    'DO 1'
);
PREPARE stmt_idx_region FROM @sql_idx_region;
EXECUTE stmt_idx_region;
DEALLOCATE PREPARE stmt_idx_region;

-- ============================================
-- TABLA: DINOSAURIOS_HABITATS (Relación N-M)
-- ============================================
CREATE TABLE IF NOT EXISTS dinosaurios_habitats (
    dinosaurio_id INT NOT NULL,
    habitat_id INT NOT NULL,
    PRIMARY KEY (dinosaurio_id, habitat_id),
    FOREIGN KEY (dinosaurio_id) REFERENCES dinosaurios(id) ON DELETE CASCADE,
    FOREIGN KEY (habitat_id) REFERENCES habitats(id) ON DELETE CASCADE,
    INDEX idx_dinosaurio_id (dinosaurio_id),
    INDEX idx_habitat_id (habitat_id)
);

-- ============================================
-- TABLA: USUARIOS (Existente, con campos extra)
-- ============================================
-- Añadir columna rol si no existe
SET @col_rol := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'usuarios'
      AND COLUMN_NAME = 'rol'
);
SET @sql_rol := IF(
    @col_rol = 0,
    'ALTER TABLE usuarios ADD COLUMN rol VARCHAR(50) DEFAULT ''usuario'' COMMENT ''usuario o admin''',
    'DO 1'
);
PREPARE stmt_rol FROM @sql_rol;
EXECUTE stmt_rol;
DEALLOCATE PREPARE stmt_rol;

-- Añadir columna activo si no existe
SET @col_activo := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'usuarios'
      AND COLUMN_NAME = 'activo'
);
SET @sql_activo := IF(
    @col_activo = 0,
    'ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE',
    'DO 1'
);
PREPARE stmt_activo FROM @sql_activo;
EXECUTE stmt_activo;
DEALLOCATE PREPARE stmt_activo;

-- Crear índice si no existe
SET @idx_rol := (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'usuarios'
      AND INDEX_NAME = 'idx_rol'
);
SET @sql_idx := IF(
    @idx_rol = 0,
    'CREATE INDEX idx_rol ON usuarios(rol)',
    'DO 1'
);
PREPARE stmt_idx FROM @sql_idx;
EXECUTE stmt_idx;
DEALLOCATE PREPARE stmt_idx;

-- ============================================
-- INSERTAR DATOS DE PRUEBA
-- ============================================

-- Eras
INSERT INTO eras (nombre, periodo_inicio, periodo_fin, descripcion) VALUES
('Triásico', 252, 201, 'Primera era de los dinosaurios'),
('Jurásico', 201, 145, 'Era dorada de los dinosaurios'),
('Cretácico', 145, 66, 'Última era de los dinosaurios')
ON DUPLICATE KEY UPDATE nombre = nombre;

-- Regiones
INSERT INTO regiones (nombre, pais, continente, descripcion) VALUES
('Montana (USA)', 'Estados Unidos', 'América del Norte', 'Zona rica en fósiles'),
('Liaoning', 'China', 'Asia', 'Depósitos de fósiles del Cretácico'),
('Región de Chubut', 'Argentina', 'América del Sur', 'Zona de descubrimientos recientes'),
('Alberta', 'Canadá', 'América del Norte', 'Famosa por sus dinosaurios del Cretácico')
ON DUPLICATE KEY UPDATE nombre = nombre;

-- Hábitats
INSERT INTO habitats (nombre, tipo_ambiente, descripcion) VALUES
('Llanura Aluvial', 'Terrestre', 'Grandes llanuras con ríos'),
('Bosque Tropical', 'Terrestre', 'Densos bosques con vegetación exuberante'),
('Sabana Seca', 'Terrestre', 'Zona árida con poca vegetación'),
('Ribera Fluvial', 'Semiácuática', 'Márgenes de ríos y lagos')
ON DUPLICATE KEY UPDATE nombre = nombre;
