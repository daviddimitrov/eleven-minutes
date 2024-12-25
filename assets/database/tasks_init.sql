CREATE TABLE IF NOT EXISTS public.tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES public.users(id) ON DELETE CASCADE,
    priority_level INTEGER REFERENCES public.priority_levels(id) ON DELETE RESTRICT,
    name VARCHAR(255) NOT NULL,
    duration INTEGER,
    due_date DATE,
    rhythm INTEGER
);