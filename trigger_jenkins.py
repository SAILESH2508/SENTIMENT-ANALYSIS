#!/usr/bin/env python3
"""
Jenkins REST API Integration Client for Sentiment Analyzer CI/CD.
Allows triggering builds, checking build status, and streaming console logs.
"""

import argparse
import time
import requests
from requests.auth import HTTPBasicAuth


def trigger_job(jenkins_url, job_name, username, token):
    """Trigger a Jenkins job build."""
    url = f"{jenkins_url.rstrip('/')}/job/{job_name}/build"
    auth = HTTPBasicAuth(username, token) if username and token else None

    try:
        print(f"🚀 Triggering build for job: '{job_name}' at {url}...")
        # Get crumb token for CSRF protection first (optional, standard in secured Jenkins)
        crumb_url = f"{jenkins_url.rstrip('/')}/crumbIssuer/api/json"
        crumb = None

        try:
            crumb_resp = requests.get(crumb_url, auth=auth, timeout=5)
            if crumb_resp.status_code == 200:
                crumb_data = crumb_resp.json()
                crumb = {crumb_data["crumbRequestField"]: crumb_data["crumb"]}
                print("🔒 CSRF Crumb acquired successfully.")
        except Exception:
            # Continue without crumb if crumb issuer is disabled
            pass

        headers = {}
        if crumb:
            headers.update(crumb)

        response = requests.post(url, auth=auth, headers=headers, timeout=10)

        if response.status_code in [200, 201, 202]:
            print("✅ Build successfully scheduled in Jenkins queue!")
            # Retries queue location headers if available
            queue_url = response.headers.get("Location")
            if queue_url:
                print(f"📍 Queue location: {queue_url}")
            return True
        else:
            print(f"❌ Failed to trigger build. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error during job trigger: {e}")
        return False


def check_build_status(jenkins_url, job_name, username, token):
    """Retrieve details and status of the last build."""
    url = f"{jenkins_url.rstrip('/')}/job/{job_name}/lastBuild/api/json"
    auth = HTTPBasicAuth(username, token) if username and token else None

    try:
        response = requests.get(url, auth=auth, timeout=10)
        if response.status_code == 200:
            data = response.json()
            build_num = data.get("number")
            result = data.get("result")  # SUCCESS, FAILURE, ABORTED, null (if building)
            building = data.get("building", False)
            duration = data.get("duration", 0) / 1000.0  # convert ms to seconds

            status = "BUILDING 🔄" if building else (result or "UNKNOWN ❓")
            print(f"\n📊 --- Last Build Details (Build #{build_num}) ---")
            print(f"Status:      {status}")
            print(f"Building:    {building}")
            print(f"Duration:    {duration:.2f} seconds")
            print(f"URL:         {data.get('url')}")
            return build_num, result, building
        elif response.status_code == 404:
            print(f"⚠️ No builds found for job '{job_name}'.")
            return None, None, False
        else:
            print(
                f"❌ Failed to check build status. Status Code: {response.status_code}"
            )
            return None, None, False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error during status check: {e}")
        return None, None, False


def get_console_output(jenkins_url, job_name, build_number, username, token):
    """Stream or print the console output logs of a specific build."""
    url = f"{jenkins_url.rstrip('/')}/job/{job_name}/{build_number}/consoleText"
    auth = HTTPBasicAuth(username, token) if username and token else None

    try:
        print(f"\n📖 Fetching console output for build #{build_number}...")
        response = requests.get(url, auth=auth, timeout=15)
        if response.status_code == 200:
            print("=" * 60)
            print(response.text)
            print("=" * 60)
            return True
        else:
            print(
                f"❌ Failed to get console output. Status Code: {response.status_code}"
            )
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error during logs streaming: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Jenkins REST API integration CLI.")
    parser.add_argument(
        "--url", default="http://localhost:8080", help="Jenkins base server URL"
    )
    parser.add_argument(
        "--job", default="sentiment-analyzer", help="Jenkins job/pipeline name"
    )
    parser.add_argument("--user", help="Jenkins username")
    parser.add_argument("--token", help="Jenkins API token or password")
    parser.add_argument(
        "--action",
        choices=["trigger", "status", "logs", "monitor"],
        default="status",
        help="Action to perform: trigger a build, get status, fetch logs, or trigger & monitor",
    )
    parser.add_argument(
        "--build",
        type=int,
        help="Build number (required for 'logs' if not querying the last build)",
    )

    args = parser.parse_args()

    if args.action == "trigger":
        trigger_job(args.url, args.job, args.user, args.token)

    elif args.action == "status":
        check_build_status(args.url, args.job, args.user, args.token)

    elif args.action == "logs":
        build_num = args.build
        if not build_num:
            # Query last build number first
            res = check_build_status(args.url, args.job, args.user, args.token)
            build_num = res[0]

        if build_num:
            get_console_output(args.url, args.job, build_num, args.user, args.token)

    elif args.action == "monitor":
        # 1. Trigger job
        if trigger_job(args.url, args.job, args.user, args.token):
            print("⏳ Waiting for build to start in queue...")
            time.sleep(5)  # Wait for Jenkins to transition from queue to active build

            # 2. Poll status
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
                    "⏳ Job is still compiling in Jenkins pipeline. Checking again in 10 seconds..."
                )
                time.sleep(10)


if __name__ == "__main__":
    main()
