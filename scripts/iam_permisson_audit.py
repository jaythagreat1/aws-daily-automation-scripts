from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from scripts.utils import timestamp, write_csv


def main() -> None:
    iam = boto3.client("iam")
    rows: list[dict] = []

    try:
        users = iam.list_users().get("Users", [])

        for user in users:
            username = user.get("UserName", "unknown")

            # MFA check
            mfa_devices = iam.list_mfa_devices(UserName=username).get("MFADevices", [])
            if not mfa_devices:
                rows.append(
                    {
                        "identity_type": "User",
                        "identity_name": username,
                        "issue": "No MFA enabled",
                        "severity": "HIGH",
                    }
                )

            # Access key age
            access_keys = iam.list_access_keys(UserName=username).get("AccessKeyMetadata", [])
            for key in access_keys:
                created = key.get("CreateDate")
                if created:
                    age_days = (datetime.now(timezone.utc) - created).days
                    if age_days > 90:
                        rows.append(
                            {
                                "identity_type": "User",
                                "identity_name": username,
                                "issue": f"Access key older than 90 days ({age_days} days)",
                                "severity": "MEDIUM",
                            }
                        )

            # Inline policies
            inline_policies = iam.list_user_policies(UserName=username).get("PolicyNames", [])
            for policy_name in inline_policies:
                rows.append(
                    {
                        "identity_type": "User",
                        "identity_name": username,
                        "issue": f"Inline policy attached: {policy_name}",
                        "severity": "REVIEW",
                    }
                )

            # Attached managed policies
            attached_policies = iam.list_attached_user_policies(UserName=username).get("AttachedPolicies", [])
            for policy in attached_policies:
                policy_name = policy.get("PolicyName", "")
                if policy_name == "AdministratorAccess":
                    rows.append(
                        {
                            "identity_type": "User",
                            "identity_name": username,
                            "issue": "AdministratorAccess policy attached",
                            "severity": "HIGH",
                        }
                    )

    except (ClientError, BotoCoreError) as error:
        print(f"AWS error while auditing IAM: {error}")
        return

    filename = f"iam_audit_{timestamp()}.csv"
    fieldnames = ["identity_type", "identity_name", "issue", "severity"]
    write_csv(filename, fieldnames, rows)

    print(f"Found {len(rows)} IAM audit findings.")


if __name__ == "__main__":
    main()