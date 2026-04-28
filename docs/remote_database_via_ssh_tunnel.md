# Accessing PostgreSQL Databases via SSH Tunnel

This guide describes how to access PostgreSQL databases running inside Docker containers on a remote server using SSH tunnels. Each container exposes its PostgreSQL port on a unique port bound to the server’s loopback interface (`127.0.0.1`). Access is made possible through SSH port forwarding, without exposing PostgreSQL to the public network.

## Rationale for Using SSH Tunneling

This approach was chosen as the most secure and practical way to provide developer access to containerized PostgreSQL instances running on a shared server.

### Key Considerations:

- The server is hosted on **Hetzner** and protected by a **Hetzner Cloud Firewall**, which restricts all incoming traffic by default.
- Each PostgreSQL instance runs in a separate Docker container and listens only on the server’s `127.0.0.1` interface.
- If direct access to PostgreSQL were used (e.g., by exposing port `5432` to the public network), it would require:
  - Explicitly opening each container’s port in the Hetzner firewall
  - Coordinating port allocation and rules for each database and environment
  - Repeating this process for every newly added developer or container
- Managing firewall rules for dozens of services and developers is error-prone and not scalable.

### Advantages of SSH Tunnel Approach:

- **No need to open any PostgreSQL port externally**
- **Access is granted via SSH only**, using key-based authentication
- **Only a single firewall rule is required** (for SSH on port 22 or custom port)
- **Databases remain completely isolated from external networks**
- Developers can connect securely using standard tools like pgAdmin or DBeaver, with minimal setup

This model significantly reduces the risk surface while maintaining flexibility and ease of use for developers.

## Architecture Overview

Each PostgreSQL container:

- Listens on port `5432` internally
- Maps that port to a unique port on `127.0.0.1` of the host (e.g., `6543`, `6544`)
- Is reachable only through SSH port forwarding from the developer machine

Connection flow:

```

Developer Machine (pgAdmin, DBeaver, psql)
|
v
localhost:\<local_port>
|
v
SSH tunnel
|
v
forwards to
|
v
Remote Server 127.0.0.1:\<container_port>
|
v
Docker Container (PostgreSQL 5432)

```

## Server Configuration

Docker containers must expose PostgreSQL ports to `127.0.0.1:<unique_port>` on the host.

Example `docker-compose.yml`:

```yaml
services:
  pgsql-db1:
    image: postgres:16
    ports:
      - "127.0.0.1:6543:5432"

  pgsql-db2:
    image: postgres:16
    ports:
      - "127.0.0.1:6544:5432"
```

Requirements:

- Each container must use a different host port
- Binding must be to `127.0.0.1` only, to prevent external access

## Developer Setup

Common setup for any cases.

### SSH Configuration

Edit (or create) the SSH config file at `~/.ssh/config`:

```ssh
Host db1
    HostName your.server.com
    Port 2222                  # Replace with actual SSH port
    User your_ssh_user
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 5433 127.0.0.1:6543

Host db2
    HostName your.server.com
    Port 2222
    User your_ssh_user
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 5434 127.0.0.1:6544
```

Each `Host` section:

- Defines a name for the database connection (`db1`, `db2`)
- Maps a local port (`5433`, `5434`) on the developer's machine to a PostgreSQL container on the server

### Connecting to a Database

To connect to a database:

```bash
ssh db1
```

This opens an SSH session and enables port forwarding. The session must remain open while using the database.

Alternatively, to open the tunnel without an interactive shell:

```bash
ssh -N db1
```

This opens the tunnel only, without launching a remote shell.

### Configuring pgAdmin or DBeaver

Use the following settings:

| Parameter | Value                |
| --------- | -------------------- |
| Host      | `localhost`          |
| Port      | `5433` or `5434`     |
| User      | Database user        |
| Password  | Database password    |
| Database  | Name of the database |

Each forwarded local port corresponds to a different containerized database.

## Simplest developer setup

Steps with creating entries in `~/.ssh/config` and running command

```bash
ssh db1
```

can be skipped if used applications and extensions with SSH-Tunneling support.

### Setup for PostgreSQL extension

- add new connection with Postgres, SSH Tunnel type
- on main tab set DB data with host as `localhost`
- on SSH tunnel tab set server IP, server port
- set connection via `ssh keys`

## Switching Between Databases

If each SSH tunnel uses a unique local port, multiple tunnels can run concurrently. Each database is then accessible independently.

If all tunnels use the same local port (e.g., `5432`), only one tunnel can be active at a time. You must terminate one before starting another.

## Stopping a Tunnel

If a tunnel is opened interactively with `ssh db1`, exit the session normally:

```bash
exit
```

If the tunnel was started with `-N` or in background mode (`-f -N`), find and terminate the process:

```bash
ps aux | grep ssh | grep 5433
kill <PID>
```

Or use:

```bash
pkill -f "ssh -N db1"
```

## Summary

- PostgreSQL containers expose their internal port `5432` to unique `127.0.0.1:<port>` bindings on the server.
- Developers connect via SSH tunnels, mapping local ports (e.g., `5433`) to those server ports (e.g., `6543`).
- SSH config defines per-database access rules.
- Tools like pgAdmin or DBeaver can connect via `localhost:<local_port>`.
- Tunnels can be started interactively or without shell (`-N`).

## Connection Credentials

All credentials required to connect to PostgreSQL databases are stored centrally and securely in Azure DevOps.

To obtain the connection parameters (host, username, password, database name):

1. Open [Azure DevOps](https://dev.azure.com/)
2. Navigate to the **Pipelines** section
3. Open **Library**
4. Select the appropriate **variable group** for your environment (e.g., `dev`, `stage`, `prod`)
5. Look for variables such as:
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_PORT`

If a variable is marked as "secret", you must have appropriate permissions to view or request its value from the team lead or DevOps engineer.

> Note: The exposed host in these variables is for use **inside Docker containers**. For SSH tunneling from a developer machine, always use `localhost` and the forwarded port as configured in your local SSH tunnel.
