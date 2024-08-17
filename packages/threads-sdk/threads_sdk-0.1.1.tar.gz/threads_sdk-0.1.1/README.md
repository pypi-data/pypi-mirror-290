# Threads SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/louis70109/line-notify#contributing)
[![pypi package](https://badge.fury.io/py/lotify.svg)](https://badge.fury.io/py/lotify)
[![Python Version](https://img.shields.io/badge/Python-%3E%3D%203.5-blue.svg)](https://badge.fury.io/py/lotify)
[![GitHub latest commit](https://badgen.net/github/last-commit/Naereen/Strapdown.js)](https://GitHub.com/Naereen/StrapDown.js/commit/)
[![GitHub stars](https://img.shields.io/github/stars/Naereen/StrapDown.js.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/Naereen/StrapDown.js/stargazers/)


# Usage


## Install package

```
pip install threads_sdk
```


## Environment variables

Input those variables in your `.env` file or OS environment (or using `export`).

Then you don't need to input any parameters in `initialize step`.

```
USER_ID
ACCESS_TOKEN
APP_SECRET
```

## Initialize instance

- If you already have Notify environment variables:

```python
from lotify.client import Client

client = Client()
```

- else:

```python
from lotify.client import Client

client = Client(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirect_uri='YOUR_URI'
)
```

## Get authorizer link

```python
link = client.get_auth_link(state='RANDOM_STRING')
print(link)
# https://notify-bot.line.me/oauth/authorize?scope=notify&response_type=code&client_id=QxUxF..........i51eITH&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fnotify&state=foo
```

## Get access token

```python
access_token = client.get_access_token(code='NOTIFY_RESPONSE_CODE')
print(access_token)
# N6g50DiQZk5Xh...25FoFzrs2npkU3z
```

## Get Status

```python
status = client.status(access_token='YOUR_ACCESS_TOKEN')
print(status)
# {'status': 200, 'message': 'ok', 'targetType': 'USER', 'target': 'NiJia Lin'}
```

## Send message

![push-notify](https://i.imgur.com/RhvwZVm.png)

```python
response = client.send_message(access_token='YOUR_ACCESS_TOKEN', message='This is notify message')
print(response)
# {'status': 200, 'message': 'ok'}
```

## Send message with Sticker

![push-notify-with-sticker](https://i.imgur.com/EWpZahk.png)

#### You can find stickerId and stickerPackageId [here](https://developers.line.biz/media/messaging-api/sticker_list.pdf).

```python
response = client.send_message_with_sticker(
    access_token='YOUR_ACCESS_TOKEN',
    message='This is notify message',
    sticker_id=1,
    sticker_package_id=1)
print(response)
# {'status': 200, 'message': 'ok'}
```

## Send message with Files

![send-message-with-image-path](https://i.imgur.com/ESCrk8b.png)

```python
image = client.send_message_with_image_file(
    access_token='YOUR_ACCESS_TOKEN',
    message='This is notify message',
    file=open('./test_image.png', 'rb')
)
print(image)
# {'status': 200, 'message': 'ok'}
```

## Send message with Image url

![send-message-with-image-url](https://i.imgur.com/0Lxatu9.png)

```python
image = client.send_message_with_image_url(
    access_token='YOUR_ACCESS_TOKEN',
    message='This is notify message',
    image_thumbnail='https://i.imgur.com/RhvwZVm.png',
    image_fullsize='https://i.imgur.com/RhvwZVm.png',
)
print(image)
# {'status': 200, 'message': 'ok'}
```

## Revoke access token

![revoke-line-notify-token](https://i.imgur.com/7GAAzOi.png)

```python
revoke = client.revoke(access_token='YOUR_ACCESS_TOKEN')
print(revoke)
# {'status': 200, 'message': 'ok'}
```

## Command Line Interface
```commandline
lotify --help
-t, --access_token TEXT  access token  [required]
-m, --message TEXT       message to send  [required]
-u, --image-url TEXT     image url to send
-f, --image-file TEXT    image file path to send
```

# Contributing

Fork before Clone the repository:

```
git clone git@github.com:your-username/line-notify.git
```

First install for development.

```
pip install -r requirements-dev.txt
```

Run `pytest` to make sure the tests pass:

```
cd line-notify/
python -m tox
python -m pytest --flake8 tests/
```

# Command Line Debug
If you met following logs.

```shell
Traceback (most recent call last):
  File "/usr/local/bin/lotify", line 33, in <module>
    sys.exit(load_entry_point('lotify==2.3.2', 'console_scripts', 'lotify')())
  File "/usr/local/bin/lotify", line 25, in importlib_load_entry_point
    return next(matches).load()
StopIteration
```

Uninstall old package and reinstall.

```shell
pip uninstall lotify
pip install lotify
```

Then `StopIteration` would go away.

# Contributors

<a href="https://github.com/louis70109/lotify/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=louis70109/lotify" />
</a>

# License

[MIT](https://github.com/louis70109/line-notify/blob/master/LICENSE) © [NiJia Lin](https://nijialin.com/about/) & [Duncan Huang](https://github.com/ragnaok)
