-- Agregar columna de imagen a las tablas existentes
ALTER TABLE dinosaurios ADD COLUMN imagen VARCHAR(500) NULL;
ALTER TABLE eras ADD COLUMN imagen VARCHAR(500) NULL;
ALTER TABLE regiones ADD COLUMN imagen VARCHAR(500) NULL;
ALTER TABLE habitats ADD COLUMN imagen VARCHAR(500) NULL;

-- Crear tabla de comentarios
CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dinosaurio_id INT NOT NULL,
    usuario_id INT NOT NULL,
    comentario_padre_id INT NULL,
    contenido TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dinosaurio_id) REFERENCES dinosaurios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (comentario_padre_id) REFERENCES comentarios(id) ON DELETE CASCADE,
    INDEX idx_dinosaurio (dinosaurio_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_padre (comentario_padre_id)
);
