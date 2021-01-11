# nornir_grimlock

## Getting Started

To get started without a configuration file:

```python
    nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 1,}},
        inventory={
            "plugin": "GrimlockInventory",
            "options": {
                "grimlock_url": "http://netbox_url",
                "grimlock_token": "1231141471263498673791",
                "ssl_verify": False,
                "filter_parameters": {},
            },
        },
    )
```

1. As part of the initialization of the Nornir object, include the inventory key
2. Set the plugin to the name of `GrimlockInventory`
3. Set the required options (if not already set via environment variables)

Accepted options include:

| Option            | Parameter         | Value                                                                                 | Default             |
| ----------------- | ----------------- | ------------------------------------------------------------------------------------- | ------------------- |
| Grimlock URL      | grimlock_url      | String - The base url of Grimlock (`http://localhost:8000` or `https://grimlock_url`) | env(GRIMLOCK_URL)   |
| Grimlock Token    | grimlock_token    | String - The token to authenticate to Grimlock API                                    | env(GRIMLOCK_TOKEN) |
| SSL Verify        | ssl_verify        | Boolean - True or False to verify SSL                                                 | True                |
| Filter Parameters | filter_parameters | Dictionary - Key/value pairs corresponding to Grimlock API searches                   | {}                  |


## Testing

In the early stages of testing since pygrimlock is not available in a public state yet, it will be included via the `tests/packages` directory. This is **not** intended to be part of the actual packaging when things go live.

## Construct

Pygrimlock will provide for the basic information that is required for Nornir to be able to leverage the inventory. The pygrimlock object will also be made available at `host.data.pygrimlock_object` to be able to access information provided from the _dcim_ endpoint.
