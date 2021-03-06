# Documentation - quick CLI
## Content
* [`context`](#quick-context)
  * [`create`](#quick-context-create)
  * [`describe`](#quick-context-describe)
  * [`list`](#quick-context-list)
  * [`activate`](#quick-context-activate)
* [`topic`](#quick-topic)
  * [`create`](#quick-topic-create)
  * [`delete`](#quick-topic-delete)
  * [`list`](#quick-topic-list)
  * [`describe`](#quick-topic-describe)
* [`gateway`](#quick-gateway)
  * [`create`](#quick-gateway-create)
  * [`delete`](#quick-gateway-delete)
  * [`apply`](#quick-gateway-apply)
  * [`list`](#quick-gateway-list)
  * [`describe`](#quick-gateway-describe)
  * [`schema`](#quick-gateway-schema)
* [`mirror`](#quick-mirror)
  * [`create`](#quick-mirror-create)
  * [`delete`](#quick-mirror-delete)
* [`app`](#quick-app)
  * [`deploy`](#quick-app-deploy)
  * [`delete`](#quick-app-delete)
## Commands
### `quick`
Control your quick deployment

**Usage:**

```
quick [-h] command [options ...] ...
```
**Available commands:**

* [`context`](#quick-context): Manage quick configuration
* [`topic`](#quick-topic): Manage topics
* [`gateway`](#quick-gateway): Manage gateways
* [`mirror`](#quick-mirror): Manage mirrors
* [`app`](#quick-app): Manage streams applications

---
### `quick context`
Manage quick configuration

**Usage:**

```
quick context [-h] command [options ...] ...
```
**Available commands:**

* [`create`](#quick-context-create): Create a new context
* [`describe`](#quick-context-describe): Display a context configuration
* [`list`](#quick-context-list): List all context configurations
* [`activate`](#quick-context-activate): Activate context

### `quick context create`
Create a new context

**Usage:**

```
quick context create [-h] [--host HOST] [--key API-KEY] [--context CONTEXT] [--debug]
```
**Optional:**

* `--host`: Name of the host (prompted if not given)
* `--key`: API key of this quick instance (prompted if not given)
* `--context`: Name of the context (defaults to host)
* `--debug`: Enable debug output

### `quick context describe`
Display a context configuration

**Usage:**

```
quick context describe [-h] [--context CONTEXT] [--debug]
```
**Optional:**

* `--context`: Select context (defaults to current one)
* `--debug`: Enable debug output

### `quick context list`
List all context configurations

**Usage:**

```
quick context list [-h] [--debug]
```
**Optional:**

* `--debug`: Enable debug output

### `quick context activate`
Activate context

**Usage:**

```
quick context activate [-h] [--debug] NAME
```
**Required:**

* `name`: Name of the context to activate

**Optional:**

* `--debug`: Enable debug output

---
### `quick topic`
Manage topics

**Usage:**

```
quick topic [-h] command [options ...] ...
```
**Available commands:**

* [`create`](#quick-topic-create): Create a new topic
* [`delete`](#quick-topic-delete): Delete a topic
* [`list`](#quick-topic-list): List all topics
* [`describe`](#quick-topic-describe): Display information for a topic

### `quick topic create`
Create a new topic

**Usage:**

```
quick topic create [-h] -k TYPE -v TYPE [-s SCHEMA] [--immutable] [--retention-time RETENTION_TIME]
                          [--context CONTEXT] [--debug]
                          NAME
```
**Required:**

* `topic_name`: The name of the topic
* `-k, --key-type`: The key type of the topic
* `-v, --value-type`: The value type of the topic

**Optional:**

* `-s, --schema`: The schema of the topic defined by gateway's GraphQL type: gateway.type
* `--immutable`: An immutable topic does not allow ingesting the same key twice (default: False)
* `--retention-time`: Retention time of data in the topic in (if not given, the data is kept indefinitely)
* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick topic delete`
Delete a topic

**Usage:**

```
quick topic delete [-h] [--context CONTEXT] [--debug] NAME
```
**Required:**

* `topic_name`: Topic to delete

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick topic list`
List all topics

**Usage:**

```
quick topic list [-h] [--context CONTEXT] [--debug]
```
**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick topic describe`
Display information for a topic

**Usage:**

```
quick topic describe [-h] [--context CONTEXT] [--debug] NAME
```
**Required:**

* `topic_name`: The name of the topic.

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

---
### `quick gateway`
Manage gateways

**Usage:**

```
quick gateway [-h] command [options ...] ...
```
**Available commands:**

* [`create`](#quick-gateway-create): Create a gateway
* [`delete`](#quick-gateway-delete): Delete a gateway
* [`apply`](#quick-gateway-apply): Apply a new schema to a gateway
* [`list`](#quick-gateway-list): List all gateways
* [`describe`](#quick-gateway-describe): Display information about a gateway
* [`schema`](#quick-gateway-schema): Display the schema of a gateway in Avro or GraphQL format

### `quick gateway create`
Create a gateway

**Usage:**

```
quick gateway create [-h] [--replicas REPLICAS] [--tag TAG] [-s SCHEMA_FILE] [--context CONTEXT] [--debug] NAME
```
**Required:**

* `gateway_name`: Name of the gateway
* `-s, --schema`: Location of the schema file or std in

**Optional:**

* `--replicas`: Number of replicas
* `--tag`: Docker image tag (defaults to currently installed tag)
* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick gateway delete`
Delete a gateway

**Usage:**

```
quick gateway delete [-h] [--context CONTEXT] [--debug] NAME
```
**Required:**

* `gateway_name`: Name of the gateway

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick gateway apply`
Apply a new schema to a gateway

**Usage:**

```
quick gateway apply [-h] -f FILE [--context CONTEXT] [--debug] NAME
```
**Required:**

* `gateway_name`: Name of the gateway
* `-f, --file`: Location of the schema file or std in

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick gateway list`
List all gateways

**Usage:**

```
quick gateway list [-h] [--context CONTEXT] [--debug]
```
**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick gateway describe`
Display information about a gateway

**Usage:**

```
quick gateway describe [-h] [--context CONTEXT] [--debug] NAME
```
**Required:**

* `gateway_name`: The name of the gateway.

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick gateway schema`
Display the schema of a gateway in Avro or GraphQL format

**Usage:**

```
quick gateway schema [-h] [--avro] [--context CONTEXT] [--debug] NAME TYPE
```
**Required:**

* `gateway_name`: The name of the gateway.
* `gateway_schema_type`: The type name used in the gateway schema.
* `--avro`: Determines if the returned format should be in Avro (If not set GraphQL format is returned).

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

---
### `quick mirror`
Mirrors make topics queryable. With these commands, you can control which topic can be queried through gateway.

**Usage:**

```
quick mirror [-h] command [options ...] ...
```
**Available commands:**

* [`create`](#quick-mirror-create): Mirror a Kafka topic
* [`delete`](#quick-mirror-delete): Delete a mirror

### `quick mirror create`
Create a mirror for a topic and make it queryable through a gateway

**Usage:**

```
quick mirror create [-h] [--tag TAG] [--replicas REPLICAS] [--context CONTEXT] [--debug] TOPIC
```
**Required:**

* `topic`: Topic to mirror

**Optional:**

* `--tag`: Docker image tag (defaults to currently installed tag)
* `--replicas`: Number of replicas (default: 1)
* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick mirror delete`
Delete a mirror

**Usage:**

```
quick mirror delete [-h] [--context CONTEXT] [--debug] TOPIC
```
**Required:**

* `mirror`: Topic to delete mirror from

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output

---
### `quick app`
Streams applications are Kafka Streams applications processing your data stream. You can deploy them to the quick cluster.

**Usage:**

```
quick app [-h] command [options ...] ...
```
**Available commands:**

* [`deploy`](#quick-app-deploy): Deploy a new application
* [`delete`](#quick-app-delete): Delete an application

### `quick app deploy`
Deploy a new application.
The application must be provided as a Docker image. You can specify the registry.

**Usage:**

```
quick app deploy [-h] --registry REGISTRY_URL --image IMAGE --tag TAG [--replicas REPLICAS]
                        [--args [ARG=VALUE [ARG=VALUE ...]]] [--context CONTEXT] [--debug]
                        NAME
```
**Required:**

* `application_name`: Name of the application (must be unique)
* `--registry`: URL to container registry
* `--image`: Name of the image
* `--tag`: Docker image tag

**Optional:**

* `--replicas`: Number of replicas
* `--args`: CLI arguments of the application (broker and schema registry not required)
* `--context`: Context of quick
* `--debug`: Enable debug output

### `quick app delete`
Delete an application. This stops the running Streams application and removes all its state.

**Usage:**

```
quick app delete [-h] [--context CONTEXT] [--debug] NAME
```
**Required:**

* `application_name`: Name of the application

**Optional:**

* `--context`: Context of quick
* `--debug`: Enable debug output
