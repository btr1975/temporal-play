# Activities

Activities in temporal can be thought of as one step or task in a full workflow.  To get the best re-use and 
granularity of steps it is best to have your activities do one thing.  That way you can re-use them in multiple 
workflows.

* [Activities](../activities/activities.py)
* [Workflows](../workflows/workflows.py)

Activities **SHOULD** to your best ability be asynchronous.  There are ways to create synchronous things for temporal,
refer to the following [sync vs async](https://docs.temporal.io/develop/python/python-sdk-sync-vs-async) 
but your best bet is to just write in async.

```python
import temporalio.workflow

with temporalio.workflow.unsafe.imports_passed_through():
    from temporal_play.nautobot_gql_client.nautobot_gql_client import NautobotGqlClient
```

Pay attention to the above stanza in my activities.  Refer to 
[Temporal Python SDK sandbox environment](https://docs.temporal.io/develop/python/python-sdk-sandbox) to understand
why it is used.  This is **VERY** important.

```python
from temporalio.exceptions import ApplicationError
from temporalio import activity

@activity.defn(name="say-hello-activity")
async def say_hello_activity(input_data: InputData) -> str:
    """A Hello World activity

    :param input_data: input data
    :type input_data: InputData

    :rtype: str
    :return: Hello
    """
    try:
        activity.logger.info(f"Hello {input_data.name}")

    except Exception as e:
        raise ApplicationError(
            message=f"Hello {input_data.name}",
            non_retryable=False,
        ) from e

    return f"Hello {input_data.other}"
```

In your activities it is a great idea to use the temporal built-in "ApplicationError".  That way you can control
how temporal acts in an exception situation.  Se above for an example.
