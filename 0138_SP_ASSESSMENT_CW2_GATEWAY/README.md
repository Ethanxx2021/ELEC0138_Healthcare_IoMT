# 0138_SP_ASSESSMENT_CW2_GATEWAY

FastAPI-based zero-trust gateway for Coursework 2 of ELEC0138 Healthcare IoMT.  
This component sits in front of the AI sanitization engine and is responsible for:

- schema validation
- device/token verification
- device–patient binding
- rate limiting
- blacklist / quarantine control
- contextual input construction
- policy enforcement
- audit logging
- batch testing and evaluation

## Recommended repository structure

This folder is intended to sit alongside the teammate AI folder in the group repository:

```text
ELEC0138_Healthcare_IoMT/
├─ 0138_SP_ASSESSMENT_CW2_AI/
└─ 0138_SP_ASSESSMENT_CW2_GATEWAY/
```

Because of that layout, `agent_adapter.py` should import the AI module from the sibling folder, not from a nested folder.

## Main files

- `app.py` — FastAPI entry point
- `auth.py` — device/token verification
- `schema.py` — request / response schemas
- `rate_limit.py` — request throttling
- `blacklist.py` — quarantine / blacklist logic
- `policy.py` — final gateway action logic
- `logs.py` — in-memory audit log helpers
- `database.py` — SQLite audit log table
- `storage.py` — persistent audit log writing
- `context_builder.py` — current payload + recent history → detector input
- `agent_adapter.py` — bridge to the teammate AI module
- `test_cases.py` — manual test cases
- `gateway_batch_test.py` — batch evaluation script
- `sample_payload.json` — example valid request
- `poisoning_payload.json` — example malicious request

## Dependencies

Install the Python packages used by the gateway:

```bash
pip install fastapi uvicorn requests pydantic
```

## How to run

Open one terminal and start the gateway:

```bash
uvicorn app:app --reload
```

Open another terminal and run the batch evaluation:

```bash
python gateway_batch_test.py
```

## External AI dependency

This gateway is designed to call the teammate folder:

`0138_SP_ASSESSMENT_CW2_AI`

That folder must already be present in the group repository, and Ollama must be running locally if you want to use `external` mode.

## Notes

This upload should **not** include:

- `venv/`
- `.git/`
- `__pycache__/`
- `gateway.db`
- generated PNG evaluation figures unless your team explicitly wants them committed
