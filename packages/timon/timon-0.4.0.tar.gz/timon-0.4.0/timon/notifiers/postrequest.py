import asyncio
import logging
import ssl

import httpx

logger = logging.getLogger()


class PostRequestNotifier:
    def __init__(self, cls, name, url, cert):
        self.cls = cls
        self.name = name
        self.url = url
        self.cert = cert
        self.data = []

    def shall_notify(self, probe, probe_state):
        return True if probe.status in [
            "WARNING", "ERROR", "CRITICAL"] else False

    def add_probe_info(self, probe, probe_state):
        hostname, probename = probe.name.split("rls_")
        self.data.append({
            "host": hostname,
            "probe": probename,
            "probe_url": getattr(probe, "url", "unknown"),
            "info": probe_state[-1]
        })

    async def notify(self):
        sslcontext = ssl.create_default_context()
        sslcontext.load_cert_chain(
            self.cert, self.cert.replace(".crt", ".key"))
        try:
            for attempt in range(3):  # TODO add attempt config param
                async with httpx.AsyncClient(verify=sslcontext) as client:
                    resp = await client.post(
                        self.url, json=self.data, timeout=10)
                    status_code = resp.status_code
                    msg = resp.text
                    if status_code == 202:
                        break
                    else:
                        logger.error(msg)
                        await asyncio.sleep(10)  # TODO add param for duration
        except Exception:
            logger.exception(
                "Notification Error: %s cannot send notif to url %s",
                self.name, self.url)


def main():
    pass


if __name__ == "__main__":
    main()
