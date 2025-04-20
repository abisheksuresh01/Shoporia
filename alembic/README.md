# Database Migrations with Alembic

This directory contains the Alembic configuration for database migrations.

## Setup

1. Make sure you have the required dependencies installed:
   ```bash
   pip install alembic sqlalchemy psycopg2-binary
   ```

2. Ensure your `.env` file contains the correct `DATABASE_URL`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_agent
   ```

## Creating a New Migration

To create a new migration based on changes to your models:

```bash
alembic revision --autogenerate -m "Description of changes"
```

This will create a new migration file in the `versions` directory.

## Applying Migrations

To apply all pending migrations:

```bash
alembic upgrade head
```

To apply a specific migration:

```bash
alembic upgrade <revision_id>
```

## Rolling Back Migrations

To roll back the most recent migration:

```bash
alembic downgrade -1
```

To roll back to a specific migration:

```bash
alembic downgrade <revision_id>
```

## Checking Migration Status

To see the current migration status:

```bash
alembic current
```

To see the migration history:

```bash
alembic history
```

## Troubleshooting

If you encounter issues with migrations:

1. Make sure your database is running and accessible
2. Check that your models are correctly defined
3. Verify that your `DATABASE_URL` is correct
4. If needed, you can reset migrations by dropping all tables and running `alembic upgrade head` again 