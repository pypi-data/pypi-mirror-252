
###########
# Imports #
###########

# Prism infrastructure imports
from prism.decorators import (
    task,
)

# Other imports
import requests
import json


###################
# Task definition #
###################

@task()
def extract(tasks, hooks):
    api_url = "https://restcountries.com/v3.1/all"
    resp = requests.get(api_url)
    data = json.loads(resp.text)
    return data
