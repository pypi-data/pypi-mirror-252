"""
This shows how to create an executeable to run a Task using the
sentry.service module.
"""

from .service import IntervalService


def main() -> int:
    """
    Runs the nop_task as a sentry.
    """
    service = IntervalService("nop_task")
    return service.run()


if __name__ == "__main__":
    main()
