# DispimDB

DispimDB is a database use to track specimens and imaging acquisitions for projects that use iSPIM (inverted selective plane illumination microscopy). The database software consists of an API, a client for the API, and a web UI for the API.

## Installing the Client

Currently, ddbclient is still being tested on TestPyPi, so the following command can be used to install it:

```
pip install -i https://test.pypi.org/simple/ ddbclient
```

An example of getting an acquisition is as follows:

```
from ddbclient import acquisition

my_acquisition = acquisition.Acquisition()
my_acquisition.get_from_db('H17', 'acq2')
```

## Installing the API and webapp

Coming soon...
