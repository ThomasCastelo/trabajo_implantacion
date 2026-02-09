-- ============================================
-- MIGRACIÓN: Añadir edición y votos a comentarios
-- ============================================

-- Agregar columna fecha_modificacion a comentarios
ALTER TABLE comentarios ADD COLUMN fecha_modificacion TIMESTAMP NULL COMMENT 'Fecha de última edición';

-- Crear tabla para votos en comentarios
CREATE TABLE IF NOT EXISTS comentario_votos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comentario_id INT NOT NULL,
    usuario_id INT NOT NULL,
    tipo_voto ENUM('positivo', 'negativo') DEFAULT 'positivo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comentario_id) REFERENCES comentarios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unique_voto (comentario_id, usuario_id),
    INDEX idx_comentario (comentario_id),
    INDEX idx_usuario (usuario_id)
);
