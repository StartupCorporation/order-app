from yoyo import step


__depends__ = {}

steps = [
    step(
        apply="""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE TABLE IF NOT EXISTS order_status (
            id UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
            code VARCHAR(128) NOT NULL,
            name VARCHAR(128) NOT NULL,
            description VARCHAR(512)
        );
        CREATE TABLE IF NOT EXISTS order_ (
            id UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
            comment VARCHAR(512),
            message_customer BOOLEAN NOT NULL,
            customer_info JSONB NOT NULL,
            products JSONB NOT NULL,
            created_at TIMESTAMP,
            order_status_id UUID NOT NULL REFERENCES order_status (id)
        );
        INSERT INTO order_status (code, name, description)
        VALUES
            ('NEW', 'NEW', NULL),
            ('PROCESSING', 'PROCESSING', NULL),
            ('PRODUCTS_RESERVATION_FAILED', 'PRODUCTS_RESERVATION_FAILED', NULL),
            ('COMPLETED', 'COMPLETED', NULL),
            ('FAILED', 'FAILED', NULL);
        """,
        rollback="DROP TABLE order_, order_status;",
    ),
]
