# func-az

> Simple tools for Azure Functions

```bash
pip install func-az
```

## Safe Start-up

Sometimes you deploy a function, and it breaks. And you have no idea why.

```python
import azure.functions as func
import func_az as fz

def make() -> func.FunctionApp:
  ...

def handle_err(exc):
  logging.error(f'An error occurred during startup: {exc}')
  return 'An error occurred'

app = fz.startup(make, error_message=handle_err)
```

If it breaks, it sets up a `/health` route that you can use to trigger the handler.


## Scheduled Job

You can set up a timer trigger, and also an HTTP trigger. But not both. This bridges the gap:

```python
import azure.functions as func
import func_az as fz

app = func.FunctionApp()

@fz.job(app, 'greet-users', route='greet', timer='0 */5 * * * *')
async def greet_users():
  ...
```

Runs at the given timer, or can be triggered at `/greet`.