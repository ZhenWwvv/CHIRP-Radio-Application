# CHIRP Radio Command Center

Web interface for running commands in [chirpradio-machine](https://github.com/chirpradio/chirpradio-machine/).

## Requirements

- Python 2.7
- Latest version of chirpradio-machine

## Installation

You may wish to [create a virtualenv](https://virtualenv.pypa.io/en/stable/) first.
Install all dependencies like this:

```
pip install -r requirements.txt
```

Make sure to follow the instructions in the
[Installation section of the chirpradio-machine README](https://github.com/chirpradio/chirpradio-machine/#installation)
so that you install the `chirp` module within the same virtualenv you used for `command-center`.

## Running

To run the service on the chirpradio musiclib server, type this:
```
sudo service chirpradio-command-center start
```

This will execute the [upstart](http://upstart.ubuntu.com/)
script configured at `/etc/init.d/chirpradio-command-center.conf`.

To view the site open [localhost:8000](http://localhost:8000)
in your browser.

You can also restart the site like this:
```
sudo service chirpradio-command-center restart
```

The log is located at `/home/musiclib/log/command-center.log`.

## Running locally

Here's how to run it manually, say, for local development.
Inside the command-center source directory, type:

```
python main.py
```

If you want to use mock commands instead of real commands, start the
app like this:

````
MOCK=1 python main.py
````

This may be useful for testing the web UI. The definitions for these
commands live in `commandcenter.mock_commands`.

## Testing

```
nosetests -v
```
