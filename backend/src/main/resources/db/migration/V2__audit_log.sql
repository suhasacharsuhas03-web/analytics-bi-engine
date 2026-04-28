CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL,
    performed_by VARCHAR(100),
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

CREATE INDEX idx_entity_type_id 
ON audit_log(entity_type, entity_id);

CREATE INDEX idx_action ON audit_log(action);
CREATE INDEX idx_performed_at ON audit_log(performed_at);