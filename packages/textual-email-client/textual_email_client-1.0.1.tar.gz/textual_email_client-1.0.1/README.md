# textual email client

[![PyPI - Version](https://img.shields.io/pypi/v/textual-email-client.svg)](https://pypi.org/project/textual-email-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/textual-email-client.svg)](https://pypi.org/project/textual-email-client)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install textual-email-client
```

Once installed, you will need to create an .env where the package was installed, for this you can use:

```bash
pip show text-email-client
```

Copy the location and then do:

```
nano /opt/homebrew/lib/python3.12/site-packages/.env
```

Using the the following values (Fill them with your Nylas information):

```text
NYLAS_API_KEY =
NYLAS_API_URI =
GRANT_ID =
```

Once installed you can call it straight from your terminal as:

```
emailClient
```

## License

`textual-email-client` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
