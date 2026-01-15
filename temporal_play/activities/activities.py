"""
activities
"""

from temporalio import activity


@activity.defn(name="say-hello-activity")
async def say_hello_activity(name: str) -> str:
    activity.logger.info("Hello {}".format(name))
    return f"Hello {name}"


ALL_ACTIVITIES = [
    say_hello_activity,
]
