# Workflows

Workflows are a basic building block of temporal.  They can run multiple activities.  
They can also receive signals, receiving signals could be something like getting an approval
to move to the next activity.

* [Workflows](../workflows/workflows.py)
* [Activities](../activities/activities.py)

In a workflow you can decide to move single activity to single activity, or even fan out and
us concurrency.  There are examples of both in the workflows.

```python
parse_tasks = []
for device in nbot_data["data"]["devices"]:
    parse_tasks.append(
        asyncio.create_task(
            workflow.execute_activity(
                activity=run_show_command_parse_with_ntc_templates_activity,
                arg=InputNetmikoCommand(
                    command=input_data.command,
                    host=device["primary_ip4"]["host"],
                    device_type=device["platform"]["network_driver_mappings"]["netmiko"],
                ),
                schedule_to_close_timeout=timedelta(minutes=10),
                retry_policy=RetryPolicy(
                    backoff_coefficient=2.0,
                    maximum_attempts=5,
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=2),
                ),
            )
        )
    )

parsed_data = await asyncio.gather(*parse_tasks)
```

Above is an example of concurrency where I am creating a list of asyncio.create_task, and then using asyncio.gather to
run them all concurrently.
