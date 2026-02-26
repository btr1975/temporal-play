# Nexus

This folder contains example implementations of Temporal Nexus 
Services, Handlers, and Workers.

# Nexus Services

Nexus services define operations available from the nexus endpoint, and
the operations input, and output data models.  They are used in nexus service
handlers.

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


# Nexus Service Handlers

Nexus service handlers implement the nexus service operations.

* [Service Handlers](./handlers/handlers.py)

If you look at the class definition you will notice
it is decorated with '@nexusrpc.handler.service_handler(service=MyNexusServices)'.
This is what associates the service handler with the service itself.

The methods are decorated with this '@nexus.workflow_run_operation' there are other
but this means we are going to start a workflow from this method.  The method itself
is named by the operation in the service.

# Nexus Workers

Nexus workers are really just created like any other temporal worker.

* [Workers](./workers/workers.py)
* [A Nexus Worker Creator](./workers/nexus_worker_creator.py)

The only things that make it "special" is adding "nexus_service_handlers" this option to the worker.  Other
than that not much else is special.
