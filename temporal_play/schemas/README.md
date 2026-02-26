# Schemas

In temporal schemas are extremely important.  They are used to serialize and deserialize data for inputs,
and outputs.

* [Schemas](./schemas.py)

In the schemas for these examples I am using python dataclasses.  Remember these are examples, and for
production quality schemas you will probably want to add data checking and all that good stuff.

You can also use [Pydantic](https://docs.pydantic.dev/latest/) for your schemas.  In fact, it could be
a better way for most use cases.  It is **IMPORTANT** to note.  If you are going to use 
[Pydantic](https://docs.pydantic.dev/latest/) for your schemas
you **MUST** create your client with the "data_converter" option set to "pydantic_data_converter".

```python
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter

client = await Client.connect(
    target_host="127.0.0.1:8082", 
    namespace="my-namespace", 
    data_converter=pydantic_data_converter
)
```
