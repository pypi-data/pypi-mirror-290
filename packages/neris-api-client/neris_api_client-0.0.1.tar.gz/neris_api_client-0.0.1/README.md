# NERIS API Client

A Python class to interact with the NERIS API programmatically.

## Usage
The client requires a username and password for authentication and authorization of requests unless the `env` argument is set to `local`
at instantiation. The `local` environment is intended for development use on local machines and bypasses auth.

```python
from neris_api_client import NerisApiClient

client = NerisApiClient(username="neris.user", password="*******", env="dev")

# Get an organization
org = client.get_org("FD24027240")
```
