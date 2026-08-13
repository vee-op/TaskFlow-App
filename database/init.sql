CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tasks (title, description)
VALUES
(
    'Learn Docker',
    'Understand Docker images, containers and networks'
),
(
    'Build TaskFlow',
    'Complete the three-tier Docker project'
),
(
    'Learn Docker Compose',
    'Understand multi-container applications'
);