TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres:postgres@localhost:5432/postgres"},
    "apps": {
        "models": {
            "models": ["tortoise_filters.models"],
            "default_connection": "default",
        },
    }
}