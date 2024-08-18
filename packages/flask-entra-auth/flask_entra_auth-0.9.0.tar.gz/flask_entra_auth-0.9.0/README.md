# Flask Entra Auth

Flask extension for authenticating and authorising requests using the Entra identity platform.

## Overview

**Note:** This project is focused on needs within the British Antarctic Survey. It has been open-sourced in case it is
of interest to others. Some resources, indicated with a '🛡' or '🔒' symbol, can only be accessed by BAS staff or
project members respectively. Contact the [Project Maintainer](#project-maintainer) to request access.

**Note:** This extension was rewritten in version 0.8.0 with a new name and non-backwards compatible design.

## Purpose

Allows routes in a [Flask](https://flask.palletsprojects.com) application to be restricted using the
[Microsoft Entra](https://learn.microsoft.com/en-us/entra/) identity platform.

Use this if you use Entra ID and want to authenticate and optionally authorise users or clients of your Flask app.

## Install

The extension can be installed using Pip from [PyPi](https://pypi.org/project/flask-entra-auth):

```
$ pip install flask-entra-auth
```

**Note:** Since version 0.6.0, this extension requires Flask 2.0 or greater.

## Usage

After creating an [App Registration](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
in Entra, initialise and [Configure](#configuration) the extension in your Flask app:

```python
from flask import Flask, current_app
from flask_entra_auth.resource_protector import FlaskEntraAuth
from flask_entra_auth.token import EntraToken

app = Flask(__name__)
app.config["ENTRA_AUTH_CLIENT_ID"] = 'xxx'
app.config["ENTRA_AUTH_OIDC_ENDPOINT"] = 'xxx'
app.config["ENTRA_AUTH_ALLOWED_SUBJECTS"] = ['xxx']  # optional, allows all subjects if empty or not set
app.config["ENTRA_AUTH_ALLOWED_APPS"] = ['xxx']  # optional, allows all applications if empty or not set

auth = FlaskEntraAuth()
auth.init_app(app)

# Example routes

@app.route("/restricted/red")
@app.auth()
def authenticated():
    """Route requires authenticated user."""
    return "Authenticated route."

@app.route("/restricted/blue")
@app.auth(['APP_SCOPE_1'])
def authorised():
    """Route requires authenticated and authorised user, specifically having the 'APP_SCOPE_1' scope."""
    return "Authorised route."

@app.route("/restricted/green")
@app.auth(['APP_SCOPE_1 APP_SCOPE_2'])
def authorised_and():
    """Route requires authenticated and authorised user, specifically having both the 'APP_SCOPE_1' and 'APP_SCOPE_2' scopes."""
    return "Authorised route."

@app.route("/restricted/yellow")
@app.auth(['APP_SCOPE_1', 'APP_SCOPE_2'])
def authorised_either():
    """Route requires authenticated and authorised user, specifically having either the 'APP_SCOPE_1' or 'APP_SCOPE_2' scopes."""
    return "Authorised route."

@app.route("/restricted/purple")
@app.auth()
def current_token():
    """Get a claim from the current token"""
    token: EntraToken = current_app.auth.current_token
    return f"Hello {token.claims['name']}"
```

### Generating access tokens

See the official Microsoft [MSAL](http://msal-python.readthedocs.io/en/latest/) library, which can also validate ID
tokens.

### Inspecting access tokens

See the official Microsoft [jwt.ms](https://jwt.ms) tool for introspecting and debugging access tokens.

### Using scopes to control access

See the [Token Scopes](#token-scopes) section for more information.

### Generating fake tokens

See the [Testing Support](#testing-support) section for more information on how to generate fake tokens for application
testing.

## Configuration

These config options are read from the [Flask config](https://flask.palletsprojects.com/en/3.0.x/config/) object:

| Option                        | Required | Description                                  |
|-------------------------------|----------|----------------------------------------------|
| `ENTRA_AUTH_CLIENT_ID`        | Yes      | Entra Application (Client) ID                |
| `ENTRA_AUTH_OIDC_ENDPOINT`    | Yes      | OpenID configuration document URI            |
| `ENTRA_AUTH_ALLOWED_SUBJECTS` | No       | An allowed list of end-users                 |
| `ENTRA_AUTH_ALLOWED_APPS`     | No       | An allowed list of client applications       |
| `ENTRA_AUTH_CONTACT`          | No       | A URI to a contact website or mailto address |

The `CLIENT_ID` represents the Flask application being secured (i.e. a client of Entra ID).

The `ALLOWED_APPS` list of clients represents clients of the Flask application (as well as Entra ID).

See the Entra ID documentation for how to get the
[Client ID](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#application-id-client-id)
and [OIDC Endpoint](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#find-your-apps-openid-configuration-document-uri)
for your application.

See the [Error Handling](#error-handling) section for more information on the `ENTRA_AUTH_CONTACT` option.

## Implementation

### Resource protector

This extension provides a [AuthLib Flask](https://docs.authlib.org/en/latest/flask/2/resource-server.html) resource
protector, [`EntraResourceProtector`](./src/flask_entra_auth/resource_protector.py), to secure access to routes within an
application by requiring a valid user (authentication) and optionally one or more required
[Scopes](#token-scopes) (authorisation).

The AuthLib resource protector uses different validators for different token types. In this case a
[BearerTokenValidator](https://github.com/lepture/authlib/blob/master/authlib/oauth2/rfc6750/validator.py#L15),
[`EntraBearerTokenValidator`](./src/flask_entra_auth/resource_protector.py), is used to [Validate](#token-validation) a
bearer JSON Web Token (JWT) specified in the `Authorization` request header. If validation fails, an
[Error](#error-handling) is returned as the request response.

The AuthLib resource protector assumes the application is running its own OAuth server, and so has a record of tokens
it has issued and can determine their validity (not revoked, expired or having insufficient scopes). This assumption
doesn't hold for Entra tokens, so instead we validate the token using PyJWT and some additional checks statelessly.

For convenience, the resource protector is exposed as a Flask extension, including a `current_token` property that
gives access to the access token taken from the request as an [EntraToken](#entra-tokens) instance.

### Entra Tokens

This extension uses a custom [`EntraToken`](./src/flask_entra_auth/token.py) class to represent Entra
[Access Tokens](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens) (not ID tokens which can be
validated with the official [MSAL](http://msal-python.readthedocs.io) library).

This class provides token [Validation](#token-validation), [Introspection](#token-introspection) and access methods of
and to tokens and their claims.

**Note:** Creating an `EntraToken` instance will automatically and implicitly [Validate](#token-validation) a token.

**Note:** Validating an `EntraToken` instance will automatically fetch the OIDC metadata and the JSON Web Key Set
(JWKS) this specifies from their respective URIs, which are then [Cached](#oidc-and-jwks-caching).

**WARNING:** `EntraTokens` do not re-validate themselves automatically once created. It is assumed tokens will be tied
to a request, and that these will be processed before they become invalid (i.e. within ~60 seconds).

If desired, this class can be used outside the [Resource Protector](#resource-protector) by passing a token string,
OIDC metadata endpoint, client ID (audience) and optionally an allowed list of subjects and client applications:

```python
from flask import Flask
from flask_entra_auth.token import EntraToken

app = Flask(__name__)
app.config["ENTRA_AUTH_CLIENT_ID"] = 'xxx'
app.config["ENTRA_AUTH_OIDC_ENDPOINT"] = 'xxx'
app.config["ENTRA_AUTH_ALLOWED_SUBJECTS"] = ['xxx']  # optional, allows all subjects if empty or not set
app.config["ENTRA_AUTH_ALLOWED_APPS"] = ['xxx']  # optional, allows all applications if empty or not set

# allowing all subjects but a restricted list of client applications
token = EntraToken(
  token='eyJhbGciOiJSUzI1NiIsImtpZCI6IjBYZ0ZndE5iLXVHazU1LUdSX1BMQ3JzN29aREtLWlRRNE5YUVM2NnhyLWsiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2lzc3Vlci5hdXRoLmV4YW1wbGUuY29tIiwic3ViIjoidGVzdF9zdWJqZWN0IiwiYXVkIjoidGVzdF9hcHBfMSIsImV4cCI6MTcyMzQ1NzAwOCwibmJmIjoxNzIzNDUzNDA4LCJhenAiOiJ0ZXN0X2FwcF8yIiwidmVyIjoiMi4wIiwic2NwcyI6WyJTQ09QRV9BIiwiU0NPUEVfQiIsIlNDT1BFX0MiXSwicm9sZXMiOlsiUk9MRV8xIiwiUk9MRV8yIiwiUk9MRV8zIl19.jOoVhWLku34OUY4XBfUddeW39R0W2PxMmf_dKiSPr87pzg0m3d5_HqVOOVyB_qKvODPT8LHT3lrKIn1D9_67ERoa5clCn23DJAOZnux-hMXd19CCPWdBMu2yC1_kBzMdIkZbTgiuTjTleLYLl5JV3livdE0JVXaSHsj7Qt5c6yypfOBbk5uM4hYqpAnMpl6XToZgnBaI1SuRF2bj2bddLNzVxvg4yOYnX25Ruz5eMkKZonBI9FyumysD7CNOEnyANdaT4z4Z5siGI046hjt10if-Iz8EmDR7Srx_wX_KLng8qS0VE3qzxhEAycoBS6RKlZ2NRfPqkwkizUi0TlDLsA',
  oidc_endpoint='https://login.microsoftonline.com/{tenancy}/v2.0/.well-known/openid-configuration',
  client_id='test_app_1',
  allowed_apps=['deb4356e-1570-4d5a-bdaa-86cf545a8045']
)

# get a validated claim
print(token.claims['exp'])  # 1723457008

# get list of scopes
print(token.scopes)  # ['SCOPE_A', 'SCOPE_B', 'SCOPE_C', 'ROLE_1', 'ROLE_2', 'ROLE_3']
```

If validation fails (which is checked implicitly on init), an [`EntraAuthError`](#error-handling) exception will be raised.

#### OIDC and JWKS caching

Data from the OIDC metadata and JWKS endpoints are cached in memory for 60 seconds within (but not between) `EntraToken`
instances. This speeds up access to OIDC metadata properties, such as the JWKS and issuer, which otherwise would
trigger multiple requests to information that is very unlikely to change within the lifetime of a token.

### Token scopes

Typically, applications wish to limit which users or clients can perform particular actions (e.g. read vs. read-write)
using custom permissions. These can be defined within the Entra ID application registration and then checked by the
[Resource Protector](#resource-protector).

Entra distinguishes between permissions:

- that apply to client applications directly, termed _scps_ (scopes)
- that apply to users (or other principles such as service accounts) and delegated to client applications, termed _roles_

This extension combines any _scps_ and _roles_ into a generic list of _scopes_, returned by the `EntraToken.scopes`
property to make it easier to combine different combinations of permissions.

See the Entra Documentation for how to
[Register custom client scopes](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-expose-web-apis)
or to [Register custom user roles](https://learn.microsoft.com/en-us/entra/identity-platform/howto-add-app-roles-in-apps).

In addition to using scopes and checking these within Flask, Entra also offers features such as
[User Assignment](https://learn.microsoft.com/en-us/entra/identity-platform/howto-restrict-your-app-to-a-set-of-users)
which apply 'upstream' as part of [Generating Access Tokens](#generating-access-tokens).

The [Resource Protector](#resource-protector) decorator supports both _AND_ and _OR_ local operators for specifying
scopes. See the [AuthLib](https://docs.authlib.org/en/latest/flask/2/resource-server.html#multiple-scopes)
documentation for more information.

### Token validation

Microsoft does not provide an official library for validating [Entra Tokens](#entra-tokens) in Python.

This extension has opted to validate tokens using a combination of [PyJWT](https://pyjwt.readthedocs.io/) and
additional custom validation methods. This is in line with how others have solved the same
[problem](https://github.com/AzureAD/microsoft-authentication-library-for-python/issues/147).

#### Validation sequence

In summary:

- get signing keys (JWKS) from Entra Open ID Connect (OIDC) endpoint (to avoid hard-coding keys that Entra may rotate)
- validate standard claims using `pyjwt.decode()`
- additionally validate the (Entra) `ver` claim is '2.0' so we know which claims we should expect
- the `sub` and/or (Entra) `azp` claim values are validated against an allow list if set (otherwise all allowed)

In more detail:

1. load OIDC metadata to get expected issuer and location to JWKS
1. load JWKS
1. parse token (base64 decode, JSON parse into header, payload and signature parts)
1. match `kid` token header parameter to key in JWKS
1. validate token signature using signing key
1. validate issuer
1. validate audience
1. validate expiration
1. validate not before
1. validate issued at (omitted)
1. validate token schema version
1. validate subject (if configured)
1. validate client (if configured)
1. validate scopes (if configured)

#### Validation limitations

##### Authentication header

The [Resource Protector](#resource-protector) checks for a missing authorisation header but doesn't raise a specific
error for a missing auth scheme, or auth credential (i.e. either parts of the authorisation header). Instead, both
errors are interpreted as requesting an unknown token type (meaning HTTP auth scheme (basic/digest/bearer/etc.) not
OAuth type (access/refresh/etc.)) by the
[`parse_request_authorization()`](https://github.com/lepture/authlib/blob/master/authlib/oauth2/rfc6749/resource_protector.py#L108).
method.

Whilst this is technically true, it isn't as granular as we'd ideally like. Whilst it would be possible to overload the
`parse_request_authorization` method, it's currently not deemed necessary and instead extra detail is included in the
[Error](#error-handling) returned for a bad authorization header (i.e. no scheme, no credential or unsupported scheme).

##### `iat` claim

The optional `iat` claim is included in Entra tokens but is not validated because it can't be tested.

Currently, there is no combination of `exp`, `nbf` and `iat` claim values that mean only the `iat` claim is invalid,
which is necessary to write an isolated test for it. Without a test we can't ensure this works correctly and is
therefore disabled.

##### `jit` claim

The optional `jit` claim is not validated as this isn't included in Entra tokens.

### Token introspection

The [`EntraToken`](#entra-tokens) class provides a `rfc7662_introspection()` method that returns standard/common claims
from a token according to [RFC 7662](https://datatracker.ietf.org/doc/html/rfc7662) (OAuth Token Introspection).

This returns a dict that can returned as a response. As per the RFC, the token to be introspected MUST be specified as
form data. It MUST also be authenticated via a separate mechanism to the token. This latter feature is not provided by
this library and would need implementing separately.

**Note:** The optional `jti` claim is not included as this isn't included in Entra tokens.

Example route (without separate authentication mechanism):

```python
from flask import Flask, request
from flask_entra_auth.exceptions import EntraAuthError
from flask_entra_auth.token import EntraToken

app = Flask(__name__)
app.config["ENTRA_AUTH_CLIENT_ID"] = 'xxx'
app.config["ENTRA_AUTH_OIDC_ENDPOINT"] = 'xxx'

@app.route("/introspect", methods=["POST"])
def introspect_rfc7662():
    """
    Token introspection as per RFC7662.
    """
    try:
        token = EntraToken(
            token=request.form.get("token"),
            oidc_endpoint=app.config["ENTRA_AUTH_OIDC_ENDPOINT"],
            client_id=app.config["ENTRA_AUTH_CLIENT_ID"],
        )
        return token.rfc7662_introspection  # noqa: TRY300
    except EntraAuthError as e:
        return {"error": str(e)}, e.problem.status
```

### Error handling

Errors encountered when accessing or validating the access token are raised as exceptions. These inherit from a base
`EntraAuthError` exception and are based on [RFC7807](https://datatracker.ietf.org/doc/html/rfc7807), encoded as JSON.

Where an exception is raised within the [Resource Protector](#resource-protector) (including the
[`EntraToken`](#entra-tokens)  instance it creates), the exception is handled by returning as a Flask (error) response.

Example response:

```json
{
  "detail": "Ensure your request includes an 'Authorization' header and try again.",
  "status": 401,
  "title": "Missing authorization header",
  "type": "auth_header_missing"
}
```

#### Error point of contact URI

Optionally, a contact URI can be included in errors by setting the `ENTRA_AUTH_CONTACT` [Config](#configuration)
option to be included in errors returned by the [Resource Protector](#resource-protector) (standalone uses of the
[`EntraToken`](#entra-tokens) class do not support this feature).

Example response (where `app.config.["ENTRA_AUTH_CONTACT"]="mailto:support@example.com"`):

```json
{
  "contact": "mailto:support@example.com",
  "detail": "Ensure your request includes an 'Authorization' header and try again.",
  "status": 401,
  "title": "Missing authorization header",
  "type": "auth_header_missing"
}
```

### Testing support

If needed for application testing, this extension includes mock classes to generate fake tokens and signing keys. These
can be used to simulate different scopes and/or error conditions. This requires changing the app under test to:

- configure the [Resource Protector](#resource-protector) to load a fake OIDC endpoint:
  - by setting the `ENTRA_AUTH_OIDC_ENDPOINT` [Config](#configuration) option to this fake endpoint
  - this endpoint returning metadata referencing a fake JWKS endpoint
  - this JWKS endpoint in turn containing a fake JWK (signing key)
- make requests to the app with local/fake access tokens (i.e. not issued by Entra) configured with relevant claims

The [Resource Protector](#resource-protector) can be used as normal for authentication and authorisation using the
claims set in the fake token. Additional claims for `name`, `upn`, etc. can be included in these tokens as needed.

If using `pytest`, the [`pytest-httpserver`](https://pytest-httpserver.readthedocs.io) plugin is recommended to serve
this fake OIDC endpoint.

For example, these fixtures:

- return a Flask test client with a fake OIDC endpoint, JWKS endpoint and signing key
- return a JWT client that can generate tokens with overridden, omitted and additional claims

```python
import pytest
from pytest_httpserver import HTTPServer
from flask.testing import FlaskClient
from flask_entra_auth.mocks.jwks import MockJwks
from flask_entra_auth.mocks.jwt import MockClaims, MockJwtClient

# replace with reference to your Flask app or app factory
from your_app import app

mock_jwks = MockJwks()
mock_iss = 'fake-issuer'

@pytest.fixture()
def app_client(httpserver: HTTPServer) -> FlaskClient:
    """Flask test client configured with fake signing key."""
    oidc_metadata = {"jwks_uri": httpserver.url_for("/keys"), "issuer": mock_iss}
    httpserver.expect_request("/.well-known/openid-configuration").respond_with_json(oidc_metadata)
    httpserver.expect_request("/keys").respond_with_json(mock_jwks.as_dict())

    app.config['ENTRA_AUTH_OIDC_ENDPOINT'] = httpserver.url_for("/.well-known/openid-configuration")
    return app.test_client()

@pytest.fixture()
def jwt_client() -> MockJwtClient:
    claims = MockClaims(self_app_id=app.config['ENTRA_AUTH_CLIENT_ID'])  # so tokens have the expected audience
    return MockJwtClient(key=mock_jwks.jwk, claims=claims)
```

Then in a test:

```python
from flask.testing import FlaskClient
from flask_entra_auth.mocks.jwt import MockJwtClient

def test_ok(self, app_client: FlaskClient, jwt_client: MockJwtClient):
    """Request to authenticated route is successful."""
    token = jwt_client.generate()  # default claims and values

    response = app_client.get("/restricted", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

To tweak the claims in the token you can override their value, omit them by setting to `False` or add other claims. E.g:

```python
from flask_entra_auth.mocks.jwt import MockJwtClient

def test_tokens(self, jwt_client: MockJwtClient):
    t = jwt_client.generate()  # default claims and values
    t = jwt_client.generate(roles=False, scps=False)  # no scopes
    t = jwt_client.generate(roles=['MY_APP.FOO.READ', 'MY_APP.BAR.READ'], scps=['MY_APP.SOMETHING'])  # custom scopes
    t = jwt_client.generate(exp=1)  # expired token (don't use `0` as this equates to None and won't be overridden)
    t = jwt_client.generate(additional_claims={'name': 'Connie Watson', 'upn': 'conwat@bas.ac.uk'})  # additional claims
```

## Developing

See [Developing](DEVELOPING.md) documentation.

## Releases

- [latest release 🛡️](https://gitlab.data.bas.ac.uk/MAGIC/flask-entra-auth/-/releases/permalink/latest)
- [all releases 🛡️](https://gitlab.data.bas.ac.uk/MAGIC/flask-entra-auth/-/releases)
- [PyPi](https://pypi.org/project/flask-entra-auth/)

## Project maintainer

British Antarctic Survey ([BAS](https://www.bas.ac.uk)) Mapping and Geographic Information Centre
([MAGIC](https://www.bas.ac.uk/teams/magic)). Contact [magic@bas.ac.uk](mailto:magic@bas.ac.uk).

The project lead is [@felnne](https://www.bas.ac.uk/profile/felnne).

## Licence

Copyright (c) 2019 - 2024 UK Research and Innovation (UKRI), British Antarctic Survey (BAS).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
