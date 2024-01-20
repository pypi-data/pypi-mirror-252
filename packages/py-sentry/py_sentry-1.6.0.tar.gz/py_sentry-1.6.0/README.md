[py-sentry](https://gitlab.com/nest.lbl.gov/py-sentry) contains the python package that provides a foundation for a micro-service that can either be run once or at a regular interval.

This document outlines how this project can be used. The purpose of this project is described [elsewhere](raison_d_être.md), as are the [details](details.md)

# Foundational Elements

## The `IntervalService`

A standard `py_sentry` executable take the following as demonstrated by the `command_service.py` example:

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

The `IntervalService` is designed to execute a named Task. The task itself is declared as a [Python entry point](https://packaging.python.org/en/latest/specifications/entry-points/). When using a [`pyproject.toml` file](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) for packaging the task can be declared as follows:

    [project.entry-points.sentry]
    command_task = "sentry.command_task:CommandTask"

## A `Task`

A `Task` is a python class that provide the implementation the behaviour of a micro-service as managed by an `IntervalService`. The complete information about how a `Task` does this is provided [elsewhere](task.md)

The main concept is that a minimal task must implement the following function:

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """

and in most other cases, also implement  this other function:

    def execute(self) -> None:
        """
        Executes the responsibilities of this executable
        """


