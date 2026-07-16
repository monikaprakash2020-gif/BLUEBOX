# OxGPT

OxGPT is a lightweight, open-source terminal AI assistant that runs entirely
locally through [Ollama](https://ollama.com). It needs no API key, cloud
account, or remote service.

## Requirements

- Python 3.9+
- Linux or Termux
- Ollama installed and running
- The default model: `deepseek-r1:1.5b`

Install Ollama from <https://ollama.com/download>, then prepare the model:

```sh
ollama serve
ollama pull deepseek-r1:1.5b
```

## Install

### Linux

Install Python, Git, and Ollama using your distribution's package manager and
the [Ollama installation guide](https://ollama.com/download). Then clone and
install OxGPT:

```sh
mkdir OxGPT
cd OxGPT
git clone https://github.com/monikaprakash2020-gif/OxGPT.git OxGPT_v1.0
cd OxGPT_v1.0
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install .
```

### Termux

Install the base tools from F-Droid or the official Termux source, then clone
and install OxGPT:

```sh
pkg update
pkg install git python
mkdir OxGPT
cd OxGPT
git clone https://github.com/monikaprakash2020-gif/OxGPT.git OxGPT_v1.0
cd OxGPT_v1.0
python3 -m pip install --user .
```

Ollama must also be installed and running locally before starting OxGPT. If
your Termux setup does not provide an `ollama` executable, use a Linux
environment on the same device that does and make that executable available
on your `PATH`.

Verify the installation:

```sh
oxgpt --version
```

## Usage

```sh
oxgpt start
oxgpt chat
oxgpt stop
```

`chat` is interactive; type `exit` to close it. `start` validates Ollama and
the model, starts the local OxGPT service in the background, and performs a
health check. The service listens only on `127.0.0.1` by default.

## Configuration

All settings are optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OXGPT_MODEL` | `deepseek-r1:1.5b` | Ollama model name |
| `OXGPT_HOST` | `127.0.0.1` | Local bind address |
| `OXGPT_PORT` | `8765` | Local service port |
| `OXGPT_STATE_DIR` | `$XDG_STATE_HOME/oxgpt` or `~/.local/state/oxgpt` | PID and log directory |
| `NO_COLOR` | unset | Disable colored output |

The background service log is stored at `oxgpt.log` inside the state directory.

## Development

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall oxgpt
```

OxGPT is released under the MIT license.
