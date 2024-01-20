"""
This shows how to create an executeable to run a Task using the
sentry.service module.
"""

from .service import IntervalService


def main() -> int:
    """
    Runs the "task" as a sentry.
    """
    service = IntervalService("task")
    return service.run()


if __name__ == "__main__":
    main()
