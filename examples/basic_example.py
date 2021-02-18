"""Testing file."""
import os
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result

def hello_world(task: Task, inv=None) -> Result:
    return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
    )

def main():
    """Nornir testing."""
    my_nornir = InitNornir(
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": os.getenv("NAUTOBOT_URL"),
                "nautobot_token": os.getenv("NAUTBOT_TOKEN"),
                "ssl_verify": False,
            },
        },
    )

    print(f"Hosts found: {len(my_nornir.inventory.hosts)}")
    # Print out the keys for the inventory
    print(my_nornir.inventory.hosts.keys())

    result = my_nornir.run(task=hello_world, inv=my_nornir.inventory)
    print_result(result)


if __name__ == "__main__":
    main()
