"""
This shows how to create an executeable to run a Task using the
sentry.service module.
"""

from sentry import IntervalService


def main() -> int:
    """
    Runs the command_task as a sentry.
    """
    service = IntervalService("command_task")
    return service.run()


if __name__ == "__main__":
    main()
