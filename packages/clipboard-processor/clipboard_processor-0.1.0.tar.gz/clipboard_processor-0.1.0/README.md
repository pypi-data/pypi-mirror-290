# clipboard-processor

![CI Build](https://github.com/tom-mi/clipboard-processor/actions/workflows/ci.yml/badge.svg)

Process clipboard content and show helpful overlays or notifications based on the content,
e.g. parse UNIX timestamps, AWS account IDs, VINs, base64 strings and more.

All parsing & decoding is done locally. The clipboard content is not sent to any external service.

## Installation

Some features require additional libraries to be installed (see below).

Install with required dependencies only:

```bash
pip install clipboard-processor
```

Install with all optional dependencies (recommended):

```bash
pip install clipboard-processor[all]
```

## Usage

```bash
clipboard-processor
```

Show help:

```bash
clipboard-processor --help
```

Run with xclip-primary input mode:

```bash
clipboard-processor --input xclip-primary
```

## Functionality

### Input

There are different input modes available:

| Mode            | Description                                                                                                                                                                                              |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `auto`          | Use [pyperclip](https://github.com/asweigart/pyperclip) for cross-platform clipboard access. This is the default.                                                                                        |
| `xclip-primary` | Use the primary selection on linux via `xclip`. No explicit copy operation is needed – selecting the text is sufficient. Requires [xclip](https://linux.die.net/man/1/xclip) command in the search path. |

### Plugins

All decoding functionality is provided via plugins. Per default, all available plugins are enabled.

| Plugin           | Description                                                                                                 | External library                                     |
|------------------|-------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| `aws_account_id` | Show AWS account name for given AWS account ID by parsing `~/.aws/config`                                   | -                                                    |
| `base64`         | Decode base64 strings                                                                                       | -                                                    |
| `jwt`            | Decode JSON web tokens (JWTs)                                                                               | [PyJWT](https://github.com/jpadilla/pyjwt)           |
| `ulid`           | Parse [ULIDs](https://github.com/ulid/spec) and show the encoded timestamp                                  | [python-ulid](https://github.com/mdomke/python-ulid) |
| `unixtime`       | Parse UNIX timestamps and show the human-readable (ISO 8601) time                                           | -                                                    |
| `vin`            | Decode [Vehicle Identification Numbers](https://en.wikipedia.org/wiki/Vehicle_identification_number) (VINs) | [vininfo](https://github.com/idlesign/vininfo)       |

### Output

There are different output modes available:

| Mode     | Description                                                                                                         |
|----------|---------------------------------------------------------------------------------------------------------------------|
| `ui`     | Use tkinter overlay near the current mouse position to show the output. This is the default.                        |
| `notify` | Use [desktop-notifier](https://github.com/SamSchott/desktop-notifier) to show the output in a desktop notification. |
| `stdout` | Print the result of the processing to the standard output. This is mostly intended for debugging and testing.       |

