# API Gateway

The Helix Engineering Platform uses an API gateway as the single entry point for external API requests.

## Request Flow

Incoming requests pass through the following stages:

1. TLS termination
2. Request validation
3. JWT authentication
4. Role-based authorization
5. Rate limiting
6. Request routing
7. Response processing

The gateway rejects invalid requests before forwarding them to downstream services.

## Authentication and Authorization

The gateway validates the JWT access token issued by the authentication service.

After successful validation, the gateway extracts the user identity and roles from the token. The authorization layer then checks whether the requested endpoint permits the user's roles.

Authentication failures return HTTP `401 Unauthorized`.

Authorization failures return HTTP `403 Forbidden`.

## Rate Limiting

The gateway applies rate limits based on the authenticated user identity and source IP address.

Normal API clients are limited to 100 requests per minute.

Requests that exceed the configured limit receive HTTP `429 Too Many Requests`.

Rate-limit events are recorded for operational monitoring.

## Routing

The gateway routes requests to internal services based on the API path.

For example:

- `/auth/*` routes to the authentication service.
- `/users/*` routes to the user service.
- `/documents/*` routes to the document service.
- `/search/*` routes to the retrieval service.

Internal services are not directly exposed to external clients.

## Observability

The gateway generates structured request logs containing the request ID, route, response status, latency, and authenticated user identifier when available.

Sensitive information such as passwords, access tokens, and authorization headers is never written to logs.
