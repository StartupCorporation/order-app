from yoyo import step


__depends__ = {"v0"}

steps = [
    step(
        apply="""
        CREATE TABLE callback_request (
            id UUID PRIMARY KEY DEFAULT (uuid_generate_v4()),
            customer_note VARCHAR(512),
            message_customer BOOLEAN NOT NULL,
            customer_info JSONB NOT NULL,
            created_at TIMESTAMP NOT NULL
        );
        ALTER TABLE order_ ALTER COLUMN created_at SET NOT NULL;
        """,
        rollback="""
        DROP TABLE callback_request;
        ALTER TABLE order_ ALTER COLUMN created_at DROP NOT NULL;
        """,
    ),
]
