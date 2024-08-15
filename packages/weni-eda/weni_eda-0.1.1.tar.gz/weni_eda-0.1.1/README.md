# Weni EDA

**weni-eda** is a Python library designed to simplify the use of Event-Driven Architecture (EDA). It provides an interface that seamlessly integrates with the Django framework and RabbitMQ messaging service. The design is scalable and intended to support various integrations in the future.

## Features
- Easy integration with Django.
- Support for RabbitMQ.
- Simplified event handling and message dispatching.
- Scalable design to accommodate future integrations with other frameworks and messaging services.


## Installation
To install the library, use pip:

```
pip install weni-eda
```

## Configuration
### Django Integration

1. Add weni-eda to your Django project:  
Add `weni.eda.django.eda_app` to your `INSTALLED_APPS` in `settings.py`:
    ```py
    # settings.py
    INSTALLED_APPS = [
        # ... other installed apps
        'weni.eda.django.eda_app',
    ]
    ```

2. Environment Variables for weni-eda Configuration

    The following environment variables are used to configure the weni-eda library. Here is a detailed explanation of each variable:

    | Variable Name          | Examples                                     | Description                                                     |
    |------------------------|----------------------------------------------|-----------------------------------------------------------------|
    | `EDA_CONSUMERS_HANDLE` | `"example.event_driven.handle.handle_consumers"` | Specifies the handler module for consumer events.               |
    | `EDA_BROKER_HOST`      | `"localhost"`                                | The hostname or IP address of the message broker server.        |
    | `EDA_VIRTUAL_HOST`     | `"/"`                                        | The virtual host to use when connecting to the broker.          |
    | `EDA_BROKER_PORT`      | `5672`                                       | The port number on which the message broker is listening.       |
    | `EDA_BROKER_USER`      | `"guest"`                                    | The username for authenticating with the message broker.        |
    | `EDA_BROKER_PASSWORD`  | `"guest"`                                    | The password for authenticating with the message broker.        |

3. Creating your event consumers  
    We provide an abstract class that facilitates the consumption of messages. To use it, you need to inherit it and declare the `consume` method as follows:
    ```py
    from weni.eda.django.consumers import EDAConsumer


    class ExampleConsumer(EDAConsumer):
        def consume(self, message: Message):
            body = JSONParser.parse(message.body)
            self.ack()
    ```

    - `JSONParser.parse(message.body)` Converts the message arriving from RabbitMQ in JSON format to `dict`
    - `self.ack()` Confirms to RabbitMQ that the message can be removed from the queue, which prevents it from being reprocessed.

4. Registering your event handlers:  
    the `EDA_CONSUMERS_HANDLE` variable indicates the function that will be called when the consumer starts. this function will be responsible for mapping the messages to their respective consumers. The function must be declared as follows:
    ```py
    import amqp

    from .example_consumer import ExampleConsumer


    def handle_consumers(channel: amqp.Channel):
        channel.basic_consume("example-queue", callback=ExampleConsumer().handle)
    ```
    This indicates that any message arriving at the `example-queue` queue will be dispatched to the `ExampleConsumer` consumer and will fall into its `consume` method.

5. Starting to consume the queues  
    To start consuming messages from the queue, you need to run the `edaconsume` command as follows:
    ```sh
    python manage.py edaconsume
    ```

    From then on, all messages that arrive in the queues where your application is written will be dispatched to their respective consumers.
