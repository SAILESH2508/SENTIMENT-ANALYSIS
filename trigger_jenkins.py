#!/usr/bin/env python3
"""
Jenkins REST API Client Utility for Sentiment Analyzer CI/CD.
Triggers builds, polls job status, streams logs, and handles CSRF crumbs.
"""

import argparse
import sys
import time
import os
import requests
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def get_crumb(jenkins_url, auth):
    """Retrieve CSRF Crumb token from Jenkins server."""
    crumb_url = f"{jenkins_url.rstrip('/')}/crumbIssuer/api/json"
    try:
        resp = requests.get(crumb_url, auth=auth, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {data["crumbRequestField"]: data["crumb"]}
    except Exception:
        pass
    return {}


def trigger_job(jenkins_url, job_name, username, token):
    """Trigger a Jenkins job build."""
    url = f"{jenkins_url.rstrip('/')}/job/{job_name}/build"
    auth = HTTPBasicAuth(username, token) if username and token else None

    try:
        print(f"🚀 Triggering build for job: '{job_name}' at {url}...")
        headers = get_crumb(jenkins_url, auth)

        response = requests.post(url, auth=auth, headers=headers, timeout=10)

        if response.status_code in [200, 201, 202]:
            print("✅ Build successfully scheduled in Jenkins build queue!")
            queue_url = response.headers.get("Location")
            if queue_url:
                print(f"📍 Queue location: {queue_url}")
            return True
        elif response.status_code == 403:
            print(
                "❌ Authentication failed (403 Forbidden). Check user credentials and API token."
            )
            return False
        else:
            print(f"❌ Failed to trigger build. Status Code: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error triggering build: {e}")
        return False


def check_build_status(jenkins_url, job_name, username, token):
    """Retrieve status details of the latest Jenkins build."""
    url = f"{jenkins_url.rstrip('/')}/job/{job_name}/lastBuild/api/json"
    auth = HTTPBasicAuth(username, token) if username and token else None

    try:
        response = requests.get(url, auth=auth, timeout=10)
        if response.status_code == 200:
            data = response.json()
            build_num = data.get("number")
            result = data.get("result")
            building = data.get("building", False)
            duration = data.get("duration", 0) / 1000.0

            status = "BUILDING 🔄" if building else (result or "UNKNOWN ❓")
            print(f"\n📊 --- Last Build Details (Build #{build_num}) ---")
            print(f"Status:      {status}")
            print(f"Building:    {building}")
            print(f"Duration:    {duration:.2f} seconds")
            print(f"URL:         {data.get('url')}")
            return build_num, result, building
        elif response.status_code == 404:
            print(f"⚠️ Job '{job_name}' found, but no builds have executed yet.")
            return None, None, False
        elif response.status_code == 403:
            print(
                f"❌ Access denied (403 Forbidden). Jenkins requires authentication (`--user` and `--token`)."
            )
            return None, None, False
        else:
            print(
                f"❌ Failed to query build status. Status Code: {response.status_code}"
            )
            return None, None, False

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error checking build status: {e}")
        return None, None, False


def get_console_output(jenkins_url, job_name, build_number, username, token):
    """Fetch and display console output logs for a build."""
    url = f"{jenkins_url.rstrip('/')}/job/{job_name}/{build_number}/consoleText"
    auth = HTTPBasicAuth(username, token) if username and token else None

    try:
        print(f"\n📖 Fetching console output logs for build #{build_number}...")
        response = requests.get(url, auth=auth, timeout=15)
        if response.status_code == 200:
            print("=" * 60)
            print(response.text)
            print("=" * 60)
            return True
        else:
            print(f"❌ Failed to fetch build logs. Status Code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error fetching logs: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Jenkins REST API integration client.")
    parser.add_argument(
        "--url",
        default=os.getenv("JENKINS_URL", "http://localhost:8080"),
        help="Jenkins base server URL (or JENKINS_URL env)",
    )
    parser.add_argument(
        "--job",
        default=os.getenv("JENKINS_JOB", "sentiment-analyzer"),
        help="Jenkins job/pipeline name (or JENKINS_JOB env)",
    )
    parser.add_argument(
        "--user",
        default=os.getenv("JENKINS_USER", None),
        help="Jenkins username (or JENKINS_USER env)",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("JENKINS_TOKEN", None),
        help="Jenkins API token or password (or JENKINS_TOKEN env)",
    )
    parser.add_argument(
        "--action",
        choices=["trigger", "status", "logs", "monitor"],
        default="status",
        help="Action: trigger, status, logs, or monitor",
    )
    parser.add_argument(
        "--build",
        type=int,
        help="Specific build number for log inspection",
    )

    args = parser.parse_args()

    if args.action == "trigger":
        trigger_job(args.url, args.job, args.user, args.token)

    elif args.action == "status":
        check_build_status(args.url, args.job, args.user, args.token)

    elif args.action == "logs":
        build_num = args.build
        if not build_num:
            res = check_build_status(args.url, args.job, args.user, args.token)
            build_num = res[0]

        if build_num:
            get_console_output(args.url, args.job, build_num, args.user, args.token)

    elif args.action == "monitor":
        if trigger_job(args.url, args.job, args.user, args.token):
            print("⏳ Waiting for build to start...")
            time.sleep(5)

            while True:
                build_num, result, building = check_build_status(
                    args.url, args.job, args.user, args.token
                )
                if not building and result is not None:
                    print(f"\n🏁 Build completed with outcome: {result}")
                    get_console_output(
                        args.url, args.job, build_num, args.user, args.token
                    )
                    break
                print(
                    "⏳ Pipeline running in Jenkins. Checking status again in 10 seconds..."
                )
                time.sleep(10)


if __name__ == "__main__":
    main()
