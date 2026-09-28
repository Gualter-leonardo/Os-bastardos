CREATE DATABASE IF NOT EXISTS sistema_cursos
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sistema_cursos;

CREATE TABLE IF NOT EXISTS informacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

INSERT INTO informacao (usuario, senha)
VALUES ('admin', '1234')
ON DUPLICATE KEY UPDATE senha = VALUES(senha);

CREATE TABLE IF NOT EXISTS cursos2 (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    curso VARCHAR(150) NOT NULL,
    carga_horaria VARCHAR(50),
    instrutor VARCHAR(150),
    quantidade_uc INT NOT NULL,
    inicio VARCHAR(50),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grade (
    id_uc INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NULL,
    nome_uc VARCHAR(150) NOT NULL,
    horas_uc INT NOT NULL,
    posicao INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_grade_curso_posicao (id_curso, posicao),
    CONSTRAINT fk_grade_curso FOREIGN KEY (id_curso)
        REFERENCES cursos2 (id_curso) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS eventos (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao VARCHAR(255),
    data_evento DATE NOT NULL,
    categoria VARCHAR(80),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_data_evento (data_evento)
);

CREATE TABLE IF NOT EXISTS alunos (
    id_aluno INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
