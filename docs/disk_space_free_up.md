# Disk Space Recovery on CI/CD Docker Servers

On servers that use continuous integration/continuous deployment (CI/CD) pipelines, disk space can gradually fill up due to the accumulation of Docker images, build cache, and unused data layers. This document outlines the safe and recommended steps for identifying and reclaiming disk space, specifically avoiding the deletion of Docker volumes (except in specific cases like full database removal).

---

## Why Disk Space Fills Up

### Common Causes:

- Frequent CI/CD builds create new Docker layers and images.
- Old images remain unused but are not automatically deleted.
- Build cache is stored between builds and accumulates over time.

---

## What Are Dangling Images?

**Dangling images** are intermediate image layers that are no longer tagged or referenced by any container. They often appear as `<none>:<none>` in `docker images` output.

### Why They Are Created:

- When rebuilding images, Docker may leave behind the old untagged layers.
- These are not automatically removed unless explicitly cleaned.

---

## Checking Disk Usage

Before cleanup, it's helpful to evaluate Docker's disk usage:

```bash
docker system df
```

For a more detailed breakdown:

```bash
docker system df -v
```

---

## Safe Cleanup Options

### Option 1: Remove Only Dangling Images

This will remove unused intermediate layers that are not associated with any container or image.

```bash
docker image prune -f
```

- Safe: Yes
- Docker volumes: Not affected
- Containers: Not affected

---

### Option 2: Remove Dangling and Unused Images

This will remove all dangling images, as well as unused images (images not currently used by any container).

```bash
docker image prune -a -f
```

- Safe: Yes (if you're sure you don't need the old, unused images)
- Docker volumes: Not affected
- Containers: Not affected

---

### Option 3: Remove Build Cache Only

Docker stores build layers in a cache that can accumulate over time, especially on CI/CD servers.

```bash
docker builder prune -f
```

- Safe: Yes (especially if cache is not reused)
- Docker volumes: Not affected
- Containers: Not affected

---

### Option 4: Full Cleanup (Images + Cache, No Volumes)

This is the most aggressive form of cleanup, but it still preserves volumes.

```bash
docker system prune -a -f
docker builder prune -f
```

- Removes: All unused images, containers, networks, and build cache.
- Keeps: Volumes (safe for production data)

---

## Notes on Volumes

Docker volumes should **never** be deleted during cleanup unless:

- You are fully removing a service and its data (e.g., deleting a PostgreSQL database entirely).
- You are certain the volume is unused and no data loss will occur.

To list and review volumes:

```bash
docker volume ls
```

To inspect a volume:

```bash
docker volume inspect <volume_name>
```

---

## Summary Table

| Cleanup Type                  | Command(s)                                              | Safe for Production | Removes Build Cache | Keeps Volumes |
| ----------------------------- | ------------------------------------------------------- | ------------------- | ------------------- | ------------- |
| Dangling images only          | `docker image prune -f`                                 | Yes                 | No                  | Yes           |
| Dangling + unused images      | `docker image prune -a -f`                              | Yes (if unused)     | No                  | Yes           |
| Build cache only              | `docker builder prune -f`                               | Yes                 | Yes                 | Yes           |
| Full cleanup (images + cache) | `docker system prune -a -f` + `docker builder prune -f` | Yes                 | Yes                 | Yes           |

---

## Recommended Practice for CI/CD Servers

- Schedule periodic cleanup (daily/weekly) using cron or GitLab/GitHub CI runners.
- Prefer using `docker image prune -f` + `docker builder prune -f` for automated pipelines or `docker system prune -f`.
- Always monitor `docker system df` to proactively detect space issues.
