# Authentication

The Helix Engineering Platform uses JSON Web Tokens (JWTs) for API authentication.

## Login Flow

When a user submits valid credentials, the authentication service verifies the credentials and issues a short-lived access token. The access token contains the user identity and expiration timestamp.

Clients include the access token in the `Authorization` header using the Bearer scheme:

`Authorization: Bearer <token>`

The API gateway validates the token before forwarding the request to downstream services.

## Token Expiration

Access tokens expire after 15 minutes. Clients must obtain a new token using the refresh-token flow after expiration.

Refresh tokens are stored securely and have a longer lifetime than access tokens.

## Failed Login Attempts

The authentication service records failed login attempts in the security audit stream. Five failed attempts from the same account within ten minutes trigger a temporary account lock.

The lock lasts for 15 minutes unless an administrator manually unlocks the account.

## Security Logging

Authentication events are published to Kafka so that downstream security and observability services can process them asynchronously.

The events include the user identifier, timestamp, source IP address, authentication result, and event type. Passwords and raw access tokens are never included in security events.
