# auth.ioit.acm.org

Static landing page for the chapter's Clerk account. The Clerk instance runs on
`clerk.auth.ioit.acm.org` (Frontend API) and `accounts.auth.ioit.acm.org`
(Account Portal), and uses `https://auth.ioit.acm.org` as its home URL, so
anything Clerk sends there lands on this page instead of a dead domain.

It links to the Account Portal, sign in and sign up on ioit.acm.org, and the
chapter website.

## Hosting

A cPanel subdomain on the same account as the website:

- Subdomain `auth.ioit.acm.org`, document root `~/auth.ioit.acm.org`. Creating
  it in cPanel also adds the DNS record; AutoSSL issues the certificate.
- `.htaccess` redirects HTTP to HTTPS, serves `index.html` for any path, and
  turns off directory listings.

Not deployed by CI. To update it, copy the files over:

```
scp deploy/auth-landing/index.html deploy/auth-landing/.htaccess \
    deploy/auth-landing/acm-logo-white.png acmhosting:auth.ioit.acm.org/
```
