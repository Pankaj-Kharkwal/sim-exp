# Getting Started with Sim

This guide provides instructions for setting up and running Sim using various methods.

## Cloud-hosted

The easiest way to get started is by using the cloud-hosted version at [sim.ai](https://sim.ai).

## Self-hosted

You can also host Sim on your own infrastructure.

### Prerequisites

- [Docker](https://www.docker.com/get-started) must be installed and running on your machine.
- [Bun](https://bun.sh/) runtime
- PostgreSQL 12+ with [pgvector extension](https://github.com/pgvector/pgvector)

### NPM Package

```bash
npx simstudio
```

This will start Sim on `http://localhost:3000`.

**Options:**

| Flag | Description |
|------|-------------|
| `-p, --port <port>` | Port to run Sim on (default `3000`) |
| `--no-pull` | Skip pulling latest Docker images |

### Docker Compose

1.  Clone the repository:
    ```bash
    git clone https://github.com/simstudioai/sim.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd sim
    ```
3.  Start Sim:
    ```bash
    docker compose -f docker-compose.prod.yml up -d
    ```

Access the application at [http://localhost:3000/](http://localhost:3000/).

#### Using Local Models with Ollama

Run Sim with local AI models using [Ollama](https://ollama.ai):

```bash
# Start with GPU support (automatically downloads gemma3:4b model)
docker compose -f docker-compose.ollama.yml --profile setup up -d

# For CPU-only systems:
docker compose -f docker-compose.ollama.yml --profile cpu --profile setup up -d
```

### Manual Setup

1.  Clone and install dependencies:
    ```bash
    git clone https://github.com/simstudioai/sim.git
    cd sim
    bun install
    ```
2.  Set up PostgreSQL with pgvector:
    - **Using Docker (Recommended):**
      ```bash
      docker run --name simstudio-db \
        -e POSTGRES_PASSWORD=your_password \
        -e POSTGRES_DB=simstudio \
        -p 5432:5432 -d \
        pgvector/pgvector:pg17
      ```
    - **Manual Installation:**
      - Install PostgreSQL 12+ and the pgvector extension. See the [pgvector installation guide](https://github.com/pgvector/pgvector#installation).
3.  Set up environment:
    ```bash
    cd apps/sim
    cp .env.example .env
    ```
    Update your `.env` file with the database URL:
    ```
    DATABASE_URL="postgresql://postgres:your_password@localhost:5432/simstudio"
    ```
4.  Set up the database:
    ```bash
    cd packages/db
    cp .env.example .env
    ```
    Update your `packages/db/.env` file with the database URL:
    ```
    DATABASE_URL="postgresql://postgres:your_password@localhost:5432/simstudio"
    ```
    Then run the migrations:
    ```bash
    bunx drizzle-kit migrate --config=./drizzle.config.ts
    ```
5.  Start the development servers:
    - **Recommended:**
      ```bash
      bun run dev:full
      ```
    - **Alternative:**
      - Next.js app: `bun run dev`
      - Realtime socket server: `cd apps/sim && bun run dev:sockets`

### Copilot API Keys

To use Copilot on a self-hosted instance:

1.  Go to [https://sim.ai](https://sim.ai) → Settings → Copilot and generate a Copilot API key.
2.  Set the `COPILOT_API_KEY` environment variable in your self-hosted `apps/sim/.env` file to that value.

## Additional Setup Content

### Ready to Test

Content from `READY_TO_TEST.md`.

### Start Services

Content from `START_SERVICES.md`.

