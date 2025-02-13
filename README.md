# [Pastforward](https://ethanthatonekid--pastforward-main.modal.run/)

## Develop

Install the dependencies.

```sh
python -m pip install -r requirements.txt
```

Set up the [Modal](https://modal.com/) project.

```sh
python -m modal setup
```

Run the development server. Live-reload might be supported on your system.

```sh
python -m modal serve main.py
```

Retrieve and store your environment variables:

- [Google Maps Platform](https://console.cloud.google.com/google/maps-apis/onboard;flow=gmp-api-key-flow)

## Deployment

[![Deploy to Modal](https://github.com/EthanThatOneKid/pastforward/actions/workflows/deploy.yaml/badge.svg)](https://github.com/EthanThatOneKid/pastforward/actions/workflows/deploy.yaml)

Retrieve your Modal API token:

```
https://modal.com/settings/{workspace}/tokens
```

Add the Modal Token to GitHub Secrets:

- Navigate to your GitHub repository.
- Go to Settings > Secrets and variables > Actions.
- Click on New repository secret.
- Name the secret `MODAL_TOKEN_ID` and paste the Modal token ID you generated.
- Name the secret `MODAL_TOKEN_SECRET` and paste the Modal token secret you generated.

Push a commit to the main branch of your GitHub repository to trigger a deployment.
