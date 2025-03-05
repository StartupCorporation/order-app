from fastapi import Request

from dw_shared_kernel.infrastructure.di.container import Container


def get_di_container(request: Request) -> Container:
    return request.state.container
