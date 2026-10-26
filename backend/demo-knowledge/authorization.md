# Authorization

The Helix Engineering Platform uses role-based access control (RBAC) to determine which resources an authenticated user can access.

## Roles

The platform defines three primary roles:

- **Viewer** — Can read engineering documents and view operational dashboards.
- **Developer** — Can read documents, view dashboards, and access development resources.
- **Administrator** — Has full access, including user management, security configuration, and audit logs.

Users are assigned one or more roles by an administrator.

## Permission Checks

Authorization is evaluated after authentication succeeds.

The API gateway extracts the user's identity and roles from the validated JWT and passes the authorization context to downstream services.

Each protected endpoint declares the roles required to access it.

For example, an endpoint that modifies security configuration requires the `Administrator` role.

## Least Privilege

Services follow the principle of least privilege. A service receives only the permissions required for its operation.

Users should also receive the minimum role necessary to perform their responsibilities.

## Authorization Failures

If an authenticated user does not have the required permission, the API returns HTTP `403 Forbidden`.

Authorization failures are recorded in the security audit stream for investigation.

## Role Changes

Role changes take effect when the user's authorization context is refreshed. Existing access tokens continue to use the roles encoded when the token was issued.

Administrators can revoke sessions when an immediate permission change is required.
