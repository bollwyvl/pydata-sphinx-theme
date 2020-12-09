""" use pa11y-ci to generate an accessibility report
"""
import json
import subprocess
import sys
from pathlib import Path
import shutil
import time
from urllib.request import urlopen

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent
BUILD = HERE / "_build"
PA11Y_BUILD = BUILD / "pa11y"
PA11Y_JSON = PA11Y_BUILD / "pa11y-ci-results.json"
YARN = [shutil.which("yarn"), "--silent"]
SITEMAP = "http://localhost:8080/sitemap.xml"
REPORT_INDEX_URL = (PA11Y_BUILD / "index.html").as_uri()


def clean():
    if PA11Y_BUILD.exists():
        shutil.rmtree(PA11Y_BUILD)
    PA11Y_BUILD.mkdir(parents=True)


def serve():
    """start the local server"""
    server = subprocess.Popen([sys.executable, HERE / "serve.py"])
    ready = 0
    retries = 10
    while retries and not ready:
        try:
            time.sleep(1)
            ready = urlopen(SITEMAP)
        except:
            retries -= 1

    assert ready, "server did not start in 10 seconds"

    return server


def audit():
    """run audit, generating a raw JSON report"""
    audit_rc = subprocess.call(
        f"yarn --silent pa11y-ci --json --sitemap {SITEMAP} > {PA11Y_JSON}",
        shell=True,
        cwd=ROOT,
    )

    return audit_rc


def report():
    """generate HTML report from raw JSON"""
    subprocess.call(
        [
            *YARN,
            "pa11y-ci-reporter-html",
            "--source",
            PA11Y_JSON,
            "--destination",
            PA11Y_BUILD,
        ],
        cwd=ROOT,
    )


def main(no_serve=False):
    """start the server (if needed), then audit, report, and clean up"""
    clean()
    audit_rc = -1
    server = None
    try:
        if not no_serve:
            server = serve()
        audit_rc = audit()
        report()
    finally:
        server and server.terminate()

    pa11y_json = json.loads(PA11Y_JSON.read_text())

    print(
        """
    JSON:\t{json}
    HTML:\t{html}
    pages:\t{total}
    passes:\t{passes}
    errors:\t{errors}
    """.format(
            html=REPORT_INDEX_URL, json=PA11Y_JSON, **pa11y_json
        )
    )

    return pa11y_json["errors"]


if __name__ == "__main__":
    sys.exit(main(no_serve="--no-serve" in sys.argv))
