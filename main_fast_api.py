import uvicorn
import os

FALLBACK_URL = os.getenv("FALLBACK_URL", "").rstrip("/")

UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")

UVICORN_RELOAD = os.getenv("UVICORN_RELOAD") == "true"


def main() -> None:
    uvicorn.run(
        "pysae.main:app",
        host=UVICORN_HOST,
        reload=UVICORN_RELOAD,
    )


if __name__ == "__main__":
    main()
