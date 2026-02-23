import time as tm
from loguru import logger


class LoguruRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = tm.time()
        client_ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "unknown"))

        with logger.contextualize(
            ip=client_ip,
            method=request.method,
            path=request.path,
            user=str(request.user) if not request.user.is_anonymous else "anonymous",
        ):
            response = self.get_response(request)

            duration = tm.time() - start
            logger.info(
                "{method} {path} → {status} ({duration:.2f}s)",
                method=request.method,
                path=request.path,
                status=response.status_code,
                duration=duration,
            )

            return response
