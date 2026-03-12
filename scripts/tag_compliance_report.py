import boto3
from botocore.exceptions import BotoCoreError, ClientError

from scripts.utils import safe_get_tags, timestamp, write_csv


REQUIRED_TAGS = {"Name", "Environment", "Owner"}


def missing_tags(tag_dict: dict[str, str]) -> str:
    missing = REQUIRED_TAGS - set(tag_dict.keys())
    return ", ".join(sorted(missing))


def main() -> None:
    ec2 = boto3.client("ec2")
    rows: list[dict] = []

    try:
        # EC2 instances
        reservations = ec2.describe_instances().get("Reservations", [])
        for reservation in reservations:
            for instance in reservation.get("Instances", []):
                tags = safe_get_tags(instance.get("Tags", []))
                missing = missing_tags(tags)
                if missing:
                    rows.append(
                        {
                            "resource_type": "EC2",
                            "resource_id": instance.get("InstanceId", "unknown"),
                            "missing_tags": missing,
                        }
                    )

        # EBS volumes
        volumes = ec2.describe_volumes().get("Volumes", [])
        for volume in volumes:
            tags = safe_get_tags(volume.get("Tags", []))
            missing = missing_tags(tags)
            if missing:
                rows.append(
                    {
                        "resource_type": "EBS",
                        "resource_id": volume.get("VolumeId", "unknown"),
                        "missing_tags": missing,
                    }
                )

    except (ClientError, BotoCoreError) as error:
        print(f"AWS error while checking tag compliance: {error}")
        return

    filename = f"tag_compliance_report_{timestamp()}.csv"
    fieldnames = ["resource_type", "resource_id", "missing_tags"]
    write_csv(filename, fieldnames, rows)

    print(f"Found {len(rows)} resources missing required tags.")


if __name__ == "__main__":
    main()