## Changelog

### v0.1.1

- `auth0.py`: Updated the `_get_jwks` method to use `requests` to decode the JSON response instead of using the `json` package.
- `cors.py`: Updated the `process_response` method of the `MiddlewareCors` class to set the response `Access-Control-Allow-Origin` header to `*` regardless of whether the incoming request is related to CORS or not.

### v0.1.0

- Initial release.
