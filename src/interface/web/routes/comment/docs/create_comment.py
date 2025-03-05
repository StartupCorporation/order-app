CREATE_COMMENT = {
    201: {
        "description": "Comment has been created.",
        "model": None,
    },
    400: {
        "description": "Comment can't be created due to some constraints.",
        "content": {
            "application/json": {
                "examples": {
                    "Author name must contain only alphabetic characters": {
                        "value": {
                            "detail": "Author name must contain only alphabetic characters",
                        },
                    },
                    "Comment content too long": {
                        "value": {
                            "detail": "Comment content has invalid length",
                        },
                    },
                },
            },
        },
    },
}
