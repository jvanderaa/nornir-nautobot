# nornir_nautobot

## Getting Started

To get started without a configuration file:

```python
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
```

1. As part of the initialization of the Nornir object, include the inventory key
2. Set the plugin to the name of `NautobotInventory`
3. Set the required options (if not already set via environment variables)

Accepted options include:

| Option            | Parameter         | Value                                                                                 | Default             |
| ----------------- | ----------------- | ------------------------------------------------------------------------------------- | ------------------- |
| Nautobot URL      | nautobot_url      | String - The base url of Nautobot (`http://localhost:8000` or `https://nautobot_url`) | env(NAUTOBOT_URL)   |
| Nautobot Token    | nautobot_token    | String - The token to authenticate to Nautobot API                                    | env(NAUTOBOT_TOKEN) |
| SSL Verify        | ssl_verify        | Boolean - True or False to verify SSL                                                 | True                |
| Filter Parameters | filter_parameters | Dictionary - Key/value pairs corresponding to Nautobot API searches                   | {}                  |


## Testing

In the early stages of testing since pynautobot is not available in a public state yet, it will be included via the `tests/packages` directory. This is **not** intended to be part of the actual packaging when things go live.

## Construct

Pynautobot will provide for the basic information that is required for Nornir to be able to leverage the inventory. The pynautobot object will also be made available at `host.data.pynautobot_object` to be able to access information provided from the _dcim_ endpoint.
