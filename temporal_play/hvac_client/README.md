# HashicorpVault Usage

This is just some important information about using HashicorpVault or really any other secrets manger in Temporal.  
The **MOST IMPORTANT RULE** is **NEVER** pass a secret as an input **OR** output of a workflow **OR** activity.  
Remember how temporal works.  The temporal system durably stores inputs **AND** outputs, but **ALL** code execution 
happens in your workers.  If you must pass PI (Personal Information) or PII (Personally Identifiable Information) in 
inputs **OR** outputs you **MUST** use a [data converter](https://docs.temporal.io/dataconversion) to encrypt and 
decrypt the data.  That way when temporal stores it, it is stored encrypted, and hopefully only you have the keys.

## Recommend Practice

1) **Security Principle of Least Privilege**: Secrets should only exist when and where they are needed, which is at 
   runtime within the activity execution environment, not the workflow definition itself.

2) **Auditability**: Accessing secrets within an activity allows HashiCorp Vault's robust audit logging to record the 
   specific activity execution and workload identity that accessed the secret, creating a strong audit trail for 
   each action.

3) **Reduced Exposure**: By fetching secrets at runtime and using short-lived credentials issued by Vault, you 
   avoid passing sensitive data through the entire workflow history, which is stored by the Temporal service.

4) **Durability and Replay Safety**: Workflow logic must be deterministic and cannot have side effects like making 
   network calls to a secrets manager. Activities, however, are designed to execute non-deterministic business logic 
   and interact with external systems. 

## Key Considerations

1) **Do not pass secrets as workflow or activity inputs/outputs**: The entire workflow history, including inputs and 
   outputs, is recorded and stored by the Temporal service for durability and replay purposes. This history is capped at 
   50MB and can be visible in the Web UI/CLI unless client-side encryption is implemented. Retrieving secrets in 
   the activity prevents them from being persisted in the workflow history.

2) **Use appropriate authentication**: Configure your Temporal workers with an appropriate Vault authentication method 
   (like Kubernetes Auth or AppRole with a secure secret delivery mechanism) to obtain short-lived, role-based 
   credentials just-in-time.

3) **Principle of Least Privilege**: Ensure the Vault policy associated with the worker's identity only grants read 
   access to the specific secrets required for that particular activity.

4) **Use a Data Converter for PI/PII/sensitive data**: If you need to pass any sensitive information (not necessarily API 
   keys/passwords, but PII) as input to the activity or return value, use a custom Data Converter to encrypt the 
   payloads before they are sent to the Temporal service. 
