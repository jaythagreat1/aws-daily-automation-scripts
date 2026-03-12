import boto3
from botocore.exceptions import BotoCoreError, ClientError

from scripts.utils import timestamp, write_csv


def main() -> None:
    ec2 = boto3.client("ec2")
    rows: list[dict] = []

    try:
        # Stopped EC2 instances
        reservations = ec2.describe_instances().get("Reservations", [])
        for reservation in reservations:
            for instance in reservation.get("Instances", []):
                instance_id = instance.get("InstanceId", "unknown")
                instance_type = instance.get("InstanceType", "unknown")
                state = instance.get("State", {}).get("Name", "unknown")

                if state == "stopped":
                    rows.append(
                        {
                            "resource_type": "EC2",
                            "resource_id": instance_id,
                            "resource_name": instance_type,
                            "issue": "Stopped instance may still incur EBS charges",
                            "state": state,
                        }
                    )

        # Unattached EBS volumes
        volumes = ec2.describe_volumes(
            Filters=[{"Name": "status", "Values": ["available"]}]
        ).get("Volumes", [])

        for volume in volumes:
            rows.append(
                {
                    "resource_type": "EBS",
                    "resource_id": volume.get("VolumeId", "unknown"),
                    "resource_name": volume.get("Size", "unknown"),
                    "issue": "Unattached EBS volume",
                    "state": volume.get("State", "unknown"),
                }
            )

        # Unassociated Elastic IPs
        addresses = ec2.describe_addresses().get("Addresses", [])
        for address in addresses:
            if "AssociationId" not in address and "NetworkInterfaceId" not in address:
                rows.append(
                    {
                        "resource_type": "ElasticIP",
                        "resource_id": address.get("AllocationId", address.get("PublicIp", "unknown")),
                        "resource_name": address.get("PublicIp", "unknown"),
                        "issue": "Unassociated Elastic IP",
                        "state": "unused",
                    }
                )

        # NAT Gateways
        nat_gateways = ec2.describe_nat_gateways().get("NatGateways", [])
        for nat in nat_gateways:
            rows.append(
                {
                    "resource_type": "NATGateway",
                    "resource_id": nat.get("NatGatewayId", "unknown"),
                    "resource_name": nat.get("VpcId", "unknown"),
                    "issue": "Review NAT Gateway cost",
                    "state": nat.get("State", "unknown"),
                }
            )

    except (ClientError, BotoCoreError) as error:
        print(f"AWS error while scanning cost anomalies: {error}")
        return

    filename = f"cost_anomaly_report_{timestamp()}.csv"
    fieldnames = ["resource_type", "resource_id", "resource_name", "issue", "state"]
    write_csv(filename, fieldnames, rows)

    print(f"Found {len(rows)} possible cost-related items.")


if __name__ == "__main__":
    main()