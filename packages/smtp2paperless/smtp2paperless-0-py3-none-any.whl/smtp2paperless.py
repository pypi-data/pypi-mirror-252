# SPDX-FileCopyrightText: 2023 Matthias Riße <matthias.risze@t-online.de>
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import asyncio
import ipaddress
import itertools
import logging
import os
import ssl
from pathlib import Path

import aiosmtpd.controller
import aiosmtpd.handlers
import requests

logger = logging.getLogger(__name__)


class MessageToPaperlessHandler(aiosmtpd.handlers.Message):
    def __init__(self, allowed_domains, *args, **kwargs):
        self.allowed_domains = allowed_domains
        super().__init__(*args, **kwargs)

    def handle_message(self, message):
        # Parse paperless token and domain from the recipient fields TO, CC and BCC and
        # make sure that the domain is allowed
        recipients = set(
            (e_p[2], e_p[0])
            for e in itertools.chain(
                message.get_all("TO"), message.get_all("CC"), message.get_all("BCC")
            )
            if e != "" and (e_p := e.partition("@"))[2] in self.allowed_domains
        )
        logger.debug("recipients (domain, token): %s", recipients)
        for part in message.walk():
            # multipart/* are just containers, skip them
            if part.get_content_maintype() == "multipart":
                continue
            # Any part that does not have a filename is presumably not a scan attachment
            # and should not be sent to paperless
            filename = part.get_filename()
            if not filename:
                continue
            logger.info("found document '%s'", filename)
            # Send the document to all specified recipients
            for domain, token in recipients:
                logger.info("sending document to '%s'", domain)
                resp = requests.post(
                    "https://{}/api/documents/post_document/".format(domain),
                    headers={"Authorization": "Token {}".format(token)},
                    files={"document": part.get_payload(decode=True)},
                )
                if not resp.ok:
                    logger.error("post request to paperless failed: '%s'", resp.text)


def run(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if os.getenv("S2P_DISABLE_TLS") is None:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=args.cert_file, keyfile=args.key_file)
    else:
        ssl_context = None

    controller = aiosmtpd.controller.UnthreadedController(
        MessageToPaperlessHandler(allowed_domains=args.allowed_domains),
        hostname=str(args.host),
        port=args.port,
        ssl_context=ssl_context,
        loop=loop,
    )

    controller.begin()
    loop.run_forever()


def ip_address(s):
    """Parse s into an IP address object"""
    try:
        # Try if the provided string is actually an integer, guess the base
        # (integers are valid ip addresses, try `ping 0` in a shell)
        return ipaddress.ip_address(int(s, base=0))
    except ValueError:
        # The IP was probably provided in a more familiar format, e.g. x.x.x.x for IPv4
        return ipaddress.ip_address(s)


def main():
    parser = argparse.ArgumentParser(description="A proxy from SMTP to Paperless' API")
    parser.add_argument("--host", type=ip_address, required=True, help="IP to bind to")
    parser.add_argument("--port", type=int, required=True, help="port to bind to")
    if os.getenv("S2P_DISABLE_TLS") is None:
        parser.add_argument(
            "--cert", type=Path, required=True, help="cert file to use for TLS"
        )
        parser.add_argument(
            "--key", type=Path, required=True, help="key file to use for TLS"
        )
    else:
        logger.warning(
            "You have disabled TLS. This option is intended for development purposes"
            " only and is otherwise a bad idea: paperless tokens will be transmitted"
            " in plaintext."
        )
    parser.add_argument(
        "--allowed_domains",
        type=lambda x: x.split(","),
        required=True,
        help="comma-separated list of paperless domains that are allowed to be targets",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
