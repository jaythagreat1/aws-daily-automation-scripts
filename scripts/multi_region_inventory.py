import boto3
from botocore.exceptions import BotoCoreError, ClientError

from scripts.utils import timestamp, write_csv


def get_enabled_regions() -> list[str]:
    ec2 = boto3.client("ec2", region_name="us-east-1")
    regions = ec2.describe_regions(AllRegions=False).get("Regions", [])
    return [region["RegionName"] for region in regions]


def main() -> None:
    rows: list[dict] = []

    try:
        regions = get_enabled_regions()
    except (ClientError, BotoCoreError) as error:
        print(f"Could not get AWS regions: {error}")
        return

    for region in regions:
        try:
            ec2 = boto3.client("ec2", region_name=region)
            reservations = ec2.describe_instances().get("Reservations", [])

            for reservation in reservations:
                for instance in reservation.get("Instances", []):
                    state = instance.get("State", {}).get("Name", "unknown")
                    instance_id = instance.get("InstanceId", "unknown")
                    instance_type = instance.get("InstanceType", "unknown")

                    name_tag = ""
                    for tag in instance.get("Tags", []):
                        if tag.get("Key") == "Name":
                            name_tag = tag.get("Value", "")
                            break

                    rows.append(
                        {
                            "region": region,
                            "instance_id": instance_id,
                            "name": name_tag,
                            "instance_type": instance_type,
                            "state": state,
                        }
                    )

        except (ClientError, BotoCoreError) as error:
            rows.append(
                {
                    "region": region,
                    "instance_id": "N/A",
                    "name": "N/A",
                    "instance_type": "N/A",
                    "state": f"ERROR: {error}",
                }
            )

    filename = f"multi_region_inventory_{timestamp()}.csv"
    fieldnames = ["region", "instance_id", "name", "instance_type", "state"]
    write_csv(filename, fieldnames, rows)

    print(f"Scanned {len(regions)} regions.")
    print(f"Found {len(rows)} total records.")


if __name__ == "__main__":
    main()