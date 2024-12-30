CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    priority_level INT,
    name VARCHAR(255) NOT NULL,
    duration INT,
    due_date DATE,
    rhythm INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (priority_level) REFERENCES priority_levels(id) ON DELETE RESTRICT
);
