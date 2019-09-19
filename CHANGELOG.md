## Changelog

### v0.4.0

- Story No. 1137: Add Sentry to `braintree-gateway`.

### v0.3.1

- Changed the Auth0 audience variable for production.

### v0.3.0

- Story No. 1083: Port `braintree-gateway` to Python 3.7.
- Story No. 1091: Switch `braintree-gateway` Git deployment to GitLab.com.
- Story No. 1146: Add production Auth0 to `braintree-gateway`.

### v0.2.1

- Changed Gunicorn port.

### v0.2.0

- Changed the postgres port in `Vagrantfile`.
- Minor changes to the service configuration.
- Updated the Ansible role to work with Python 3.5.

### v0.1.2

- Fixed the wrong Git URL in the Ansible role.
- Updated the Ansible role to use the Python3 version supported by default in Ubuntu 16.04.

### v0.1.1

- `auth0.py`: Updated the `_get_jwks` method to use `requests` to decode the JSON response instead of using the `json` package.
- `cors.py`: Updated the `process_response` method of the `MiddlewareCors` class to set the response `Access-Control-Allow-Origin` header to `*` regardless of whether the incoming request is related to CORS or not.

### v0.1.0

- Initial release.
