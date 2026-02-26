# Workers

Workers in temporal are what actually process your workflows and activities.  The temporal server in the end really
just receives requests to run workflows and activities, and then makes sure they are run, saves the inputs and 
outputs, and if something fails tells a worker to run it again from some point in the workflow.  Obviously it
is way more awesome than that, but at a base level it's easier to think of that way.

* [Simple Worker Creator](./worker_creator.py)

In the above worker creator it is just a simple way to create a worker, and have it decide if it should run as a
regular async worker, or as a threadpool executor worker.  It takes in an instantiated client, with the options
you wanted, the task queue name the workflows you want to give it access to, and the activities it needs access to.
It then looks at all the activities, and if **ANY** of them are synchronous it uses a threadpool executor.  Obviously
make better decisions in your real code.

* [Worker](./worker_1.py)

In the above worker it loads all **NON-NEXUS** workflows and all activities.

* [Worker that Only Consumes Nexus Enabled WorkFlows](./worker_consume_only_nexus.py)

In the above worker it loads all **ONLY NEXUS** workflows and all activities.
