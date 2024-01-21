<!--
SPDX-FileCopyrightText: 2023 Matthias Riße <matthias.risze@t-online.de>

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# SMTP2Paperless

NOTE: when I refer to "paperless" I always mean paperless-ngx,
since that is the only relevant version of paperless today.


## What?

A "SMTP to Paperless API" proxy.
You configure your document scanner to send scans as emails via SMTP to this software with a recipient of `<paperless-token>@<paperless-domain>`
and the proxy will forward the attached scans to the Paperless API's document post endpoint of the chosen paperless instance.

The proxy is stateless,
it simply looks at the recipient of the received message to determine where to post the document to.
The paperless domain must be in a whitelist to be the target of the proxy
(this is to stop anyone from abusing the proxy to send post requests to arbitrary domains,
since there is no additional authentication happening).

The proxy must be hosted with TLS to avoid leaking the Paperless API tokens send in the recipient fields.


## Why?

I wanted a document scanner that could scan directly to the Paperless API's document post endpoint,
but apparently there is none (some Doxie scanner can allegedly do this,
but as far as I know it is not officially supported).
Since many scanners can send scans by email SMTP sounded like the next best thing.
I didn't want to add a mailbox as a "man-in-the-middle" though
(and use paperless' IMAP feature),
since I would either have to self-host that or be fine with a third-party receiving all of my physical mail
and other scans on top of my normal email.
That seemed a bit unnecessary.
So I built a simple "SMTP to Paperless API" proxy instead.


## How?

```
smtp2paperless --host <host> --port <port> --cert <cert-file> --key <key-file> --allowed_domains <paperless-domain>
```

Make it a systemd service
or do whatever else you do to run your services.

Then configure your scanner to send mails via the SMTP proxy at your IP and chosen port.
No authentication required.

Last,
add a recipient address in the format `<paperless-token>@<paperless-domain>` to your scanners address book
and send a scan to that address.
It should now show up on your paperless instance.
