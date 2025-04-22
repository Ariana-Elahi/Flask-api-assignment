# Capital City Time API

- **URL**: `http://<your-vm-external-ip>:5001/api/time`
- **Method**: `GET`
- **Authentication**: Requires `Authorization: Bearer secret-token`

## Query Parameters
- `city` (required): Capital city (e.g., `london`, `kabul`).

## Example Request
```bash
curl -H "Authorization: Bearer K7cEjvvx4D" "http://<your-vm-external-ip>:5001/api/time?city=london"