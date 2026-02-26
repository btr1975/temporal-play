# Nexus

This folder contains example implementations of Temporal Nexus 
Services, Handlers, and Workers.

# Nexus Services

Nexus services define operations available from the nexus endpoint, and
the operations input, and output data models.

* [Services](./services/services.py)

If you look at the class definition you will notice
it is decorated with '@nexusrpc.service(name="nexus-my-nexus-services")'.
This is what makes it a "named" nexus service.  You use that name when
creating a nexus client in a workflow.

```python
self.nexus_client = workflow.create_nexus_client(
    service="nexus-my-nexus-services",
    endpoint="default-nexus-service",
)
```

* [Workflows](../workflows/workflows.py)

Notice in the above client creation, the service name is the name of our service, also
notice that the endpoint name will be whatever name was given to the
nexus endpoint in the cluster.

Operations in the service are created using class variables, with a type
hint of the operations input type, and output type.

Look through the workflows and find a nexus workflow.  You will see the client being used
like this.

```python
result = await self.nexus_client.execute_operation(
    operation="render_config",
    input=input_data,
)
```

Notice the usage is the operation name, and the input data needed.
