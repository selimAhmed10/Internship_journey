# JWT (json web token) threat analysis
Jwt is a stateless authentication mechanism mostly used in REST APIs and modern web applications.When a user login into the system using the username and password and when its successful the jwt issued a access token and a refresh token. The user then use the access token for any request there use the token to verify its actually you.its mainly use to verify its you.
#### In the token have 3 parts-
- Header(jwt and algorithm like that)
- Payload(jti, and information like id ,name etc can be use modified here i use the id and the role) - encode part
- And the signature( its to match)

When the user successfuly login then the server send two 
- access and ( normaly give access time less like 10 or close as per businees policy) use for access , after its time its expire then the access token doesnt work.
- refresh token (long like 3 or more as per business policy) use for new access token.

And in the token have these three parts.The server doest store the token because its stateless protocol, in server have the own identify protocal , when the user send the token to request the server firstly decode the payload and use his machanism make a singnature if math with the user singnature then he give access.


## 1. Token Leakage
The jwt totally depends on the token based. So one of the most common threats is token leakage or stolen. If an attacker obtains a valid token through browser,application logs,network interception or cros site scripting they can do anything act as the until the token expires.The server give access because of it match the siganature if okey everthing you can do.
   - Mitigation 
        1. Use https for all communication and request.
        3. Store tokens securely
        4. Keep access token lifetime short.

## 2. Long Token Expire
long lived access token increases the impact of token theft. If an attacker steals a token that remains valid for days, they can continue accessing protected resources without re authentication.
   - Mitigation:
        1. set the access token short 
        2. Rotate refresh tokens after each use.

## 3. Refresh token theft
Refresh tokens typically have a longer lifetime than the access token.If the attaker get the refresh token can generate access token when ever he want and can get fully access.
   - Mitigation:
        1. Enable refresh token rotation.
        2. Blacklist old refresh tokens after rotation.
        3. Allow users to revoke active sessions.
        4. Track token usage by device and IP address.
## 4. Weak secret key
JWT signatures rely on a secret signing key.If the signing key is weak,predictable or exposed,attackers may forge valid tokens and gain unauthorized access.
   - Mitigation:
        1. Use a long,randomly generated secret key.
        2. Store secrets in environment variables instead of source code.

## 5. Missing logout mechanism
JWT is stateless so logging out on the client side so the server still work using the token because of it will work untill the access token expire.Because it stateless the server only know when the token work untill it works
   - Mitigation:
        1. Implement refresh token black list after logout because it lifecycle long.
        2. maintain the session and block the sesion after logout and access token false after logout 
        3. Maintain a blacklist of revoked tokens.
## 6. Insecure token claims
Sensitive information should never be stored inside JWT payloads because the payload is Base64 encoded,not encrypted. So anyone possessing the token can decode and read its contents.
   - Mitigation:
        1. Store only non sensitive information such as user ID and role.
        2. Never include passwords,account balances, or confidential personal information in JWT claims.

## 7. The none Algorithm Attack

An attacker changes the JWT alg field to none(HS256 to none if the backend system cofigure porly). If the server accepts it without verifying the signature,the attacker can modify the token payload(change the role to admin) and gain unauthorized access.

   - Mitigation:
        1. Reject the none algorithm,allow only secure algorithms (HS256)
        2. Always verify the JWT signature before accepting the token.


