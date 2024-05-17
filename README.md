# loan_amortization

This is my submission for the loadn amortization backend coding challenge.

Run instructions:

After you've cloned the repo, please open the terminal and navigate to loan-amortization-api. Then, install poetry (the dependency manager I used), and install the project dependecies using the following commands:

```
pip install poetry
poetry install
```

Now, intialize your python env by running the following command:

```
poetry run uvicorn loan_amortization_api.main:app --reload
```

Now, in a different terminal window, navigate to loan-amortization-api and run this command to run our tests:

```
poetry run pytest
```

Thank you!
