CREATE TABLE IF NOT EXISTS priority_levels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO priority_levels (name)
VALUES
    ('ASAP'),
    ('HIGH'),
    ('MEDIUM'),
    ('LOW');