# Demo Shop (DevPilot test project)

A tiny online shop: a Python API (FastAPI) and a web page, in one folder and one Docker image.
It exists to **try out DevPilot**. Some branches contain **bugs on purpose**.

> Do not deploy this anywhere real. The bugs and the fake passwords in it are deliberate.

## Run it

Docker is all you need.

```bash
docker compose up -d --build          # the shop on http://127.0.0.1:8090
docker compose --profile test run --rm --build test    # unit tests
```

Several copies can run side by side, one per stage. For example, `develop` as the "dev" stage:

```bash
git switch develop
SHOP_PORT=8091 docker compose -p shop-dev up -d --build    # http://127.0.0.1:8091
```

| Page | What |
|---|---|
| `/` | The shop (add to cart, discount code `WELCOME10`) |
| `/health` | `{"status": "ok"}` when the shop is alive |
| `/api/products`, `/api/cart/total` | The API |

## Branches (stages)

| Branch | Stage | Deploy workflow |
|---|---|---|
| `develop` | development | none (local copy) |
| `staging` | staging | `deploy-staging.yml` |
| `main` | production | `deploy-production.yml` |

The deploy workflows only print what they would do: there is no real server.

## Planted problems (what DevPilot should notice)

| Where | Problem | DevPilot today |
|---|---|---|
| PR `feature/discount-codes` → `develop` | Hard-coded password in `backend/app/settings.py` | Finding (high) + review comment |
| same PR | Python syntax error in `backend/app/discounts.py` | Finding (high) |
| same PR | Discounts over 100% make the total negative (logic bug) | **Not found yet**: needs the AI review planned for Phase 1b |
| PR `feature/holiday-config` → `develop` | `data/products.json` is not valid JSON | Finding (medium) |
| same PR | Leftover merge-conflict markers in `docs/holiday-sale.md` | Finding (high) |
| `develop` (pushed directly) | `/health` crashes (reads a setting that does not exist) | Stage **down** → finding → GitHub issue |
| `develop` | A unit test fails, so CI fails | CI failure finding on the development stage |

`main` and `staging` are clean.
