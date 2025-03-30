from dw_shared_kernel.infrastructure.di.container import Container
from fastapi import Request


def get_di_container(request: Request) -> Container:
    return request.state.container
