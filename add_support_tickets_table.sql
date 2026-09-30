CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    lecturer_id INTEGER NOT NULL,
    subject VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Open',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITHOUT TIME ZONE,
    resolved_by INTEGER,
    CONSTRAINT fk_support_lecturer FOREIGN KEY(lecturer_id) REFERENCES lecturers(id) ON DELETE CASCADE,
    CONSTRAINT fk_support_resolver FOREIGN KEY(resolved_by) REFERENCES users(id) ON DELETE SET NULL
);
