from dw_shared_kernel import MessageDestination


class RabbitMQEventDestination(MessageDestination):
    routing_key: str
    exchange: str
