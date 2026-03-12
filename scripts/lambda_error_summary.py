import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from scripts.utils import timestamp, write_csv


LOOKBACK_HOURS = 24


def main() -> None:
    logs = boto3.client("logs")
    lambda_client = boto3.client("lambda")
    rows: list[dict] = []

    now_ms = int(time.time() * 1000)
    start_ms = now_ms - (LOOKBACK_HOURS * 60 * 60 * 1000)

    try:
        functions = lambda_client.list_functions().get("Functions", [])

        for function in functions:
            function_name = function.get("FunctionName", "unknown")
            log_group_name = f"/aws/lambda/{function_name}"

            try:
                response = logs.filter_log_events(
                    logGroupName=log_group_name,
                    startTime=start_ms,
                    endTime=now_ms,
                    filterPattern="ERROR",
                )

                events = response.get("events", [])
                if events:
                    latest_message = events[-1].get("message", "").replace("\n", " ")[:200]
                    rows.append(
                        {
                            "function_name": function_name,
                            "error_count_last_24h": len(events),
                            "sample_error": latest_message,
                        }
                    )

            except logs.exceptions.ResourceNotFoundException:
                continue
            except (ClientError, BotoCoreError) as inner_error:
                rows.append(
                    {
                        "function_name": function_name,
                        "error_count_last_24h": "N/A",
                        "sample_error": f"Could not query logs: {inner_error}",
                    }
                )

    except (ClientError, BotoCoreError) as error:
        print(f"AWS error while summarizing Lambda logs: {error}")
        return

    filename = f"lambda_error_summary_{timestamp()}.csv"
    fieldnames = ["function_name", "error_count_last_24h", "sample_error"]
    write_csv(filename, fieldnames, rows)

    print(f"Found {len(rows)} Lambda functions with logged errors.")


if __name__ == "__main__":
    main()