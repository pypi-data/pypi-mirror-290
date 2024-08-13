<h1>PyRFC</h1>

Asynchronous, non-blocking [SAP NetWeaver RFC SDK](https://support.sap.com/en/product/connectors/nwrfcsdk.html) bindings for Python.

[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyrfc)](https://pypi.org/project/pyrfc/)
[![PyPI - Version](https://img.shields.io/pypi/v/pyrfc)](https://pypi.org/project/pyrfc/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyrfc)](https://pypi.org/project/pyrfc/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyrfc)](https://pypistats.org/packages/pyrfc)
[![REUSE status](https://api.reuse.software/badge/github.com/SAP/PyRFC)](https://api.reuse.software/info/github.com/SAP/PyRFC)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4349/badge)](https://bestpractices.coreinfrastructure.org/projects/4349)

- [Features](#features)
- [Supported platforms](#supported-platforms)
- [Requirements](#requirements)
  - [SAP NW RFC SDK 7.50 Patch Level 12](#sap-nw-rfc-sdk-750-patch-level-12)
  - [Linux](#linux)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Docker](#docker)
- [Download and installation](#download-and-installation)
- [Getting started](#getting-started)
  - [Call ABAP Function Module from Python](#call-abap-function-module-from-python)
  - [Call Python function from ABAP](#call-python-function-from-abap)
- [SPJ articles](#spj-articles)
- [How to obtain support](#how-to-obtain-support)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)


## Call for Maintainers

This project is currently looking for new maintainers. Please see [this issue](https://github.com/SAP/PyRFC/issues/372) for details.

## Features

- Client and Server bindings
- Automatic conversion between Python and ABAP datatypes
- Stateless and stateful connections (multiple function calls in the same ABAP session / same context)
- Sequential and parallel calls, using one or more clients
- Throughput monitoring

## Supported platforms

- All [platforms supported by SAP NWRFC SDK](https://launchpad.support.sap.com/#/notes/2573790) are supported by build from source installation ([build instructions](http://sap.github.io/PyRFC/build.html))

- In addition, pre-built wheels are provided for Windows, Darwin and Ubuntu Linux, attached to PyRFC GitHub [release](https://github.com/SAP/PyRFC/releases/latest)

- Docker containers: [SAP fundamental-tools/docker](https://github.com/SAP/fundamental-tools/tree/main/docker)

- Linux wheels supported by build from source installation only

- Pre-built [portable Linux wheels](https://www.python.org/dev/peps/pep-0513/)
  - are not supported, neither issues related to portable Linux wheels

  - **must not** be distributed with embedded SAP NWRFC SDK binaries, only private use permitted

- [Ansible Module for use of SAP PyRFC](https://docs.ansible.com/ansible/latest/collections/community/sap_libs/sap_pyrfc_module.html)

- Microsoft IIS, see [#359](https://github.com/SAP/PyRFC/issues/359)

## Requirements

### SAP NW RFC SDK 7.50 Patch Level 12

- see [SAP Note 3337381: SAP NetWeaver RFC SDK 7.50 -- Patch Level 12](https://me.sap.com/notes/3337381) for a list of bug fixes and enhancements made with this patch release.
- **Only the latest patch level is supported by SAP**
- The latest version is fully backwards compatible, from today S4, down to R/3 release 4.6C.
- Can be downloaded from SAP Software Download Center of the SAP Support Portal, like described at https://support.sap.com/nwrfcsdk.
- If you are lacking the required authorization for downloading software from the SAP Service Marketplace, please follow the instructions of [SAP Note 1037575](https://launchpad.support.sap.com/#/notes/1037575) for requesting this authorization.

### Linux

PyRFC is using source distribution (sdist) installation on Linux systems and [Cython](https://cython.readthedocs.io/en/latest/index.html) is required on Linux system to build the PyRFC package from source. See [Installing Cython](https://cython.readthedocs.io/en/latest/src/quickstart/install.html#installing-cython)

### Windows

- [Visual C++ Redistributable Package for Visual Studio 2013](https://www.microsoft.com/en-US/download/details.aspx?id=40784) is required for run-time, see [SAP Note 2573790 - Installation, Support and Availability of the SAP NetWeaver RFC Library 7.50](https://launchpad.support.sap.com/#/notes/2573790)

- Build toolchain for Python requires [Microsoft C++ Build Tools](https://aka.ms/buildtools), the latest version recommended

- Due to a [change introduced with Python 3.8 for Windows](https://docs.python.org/3.8/whatsnew/3.8.html#bpo-36085-whatsnew), PATH directories are no longer searched for DLL. The SAP NWRFC SDK lib path is no longer required on PATH, for Python >= 3.8.

### macOS

- Remote paths must be set in SAP NWRFC SDK for macOS: [documentation](http://sap.github.io/PyRFC/install.html#macos)

- When the PyRFC is started for the first time, the popups may come-up for each NWRFC SDK library, to confirm the usage. If SAP NW RFC SDK is installed in admin folder, the app shall be first time started with admin privileges, eg. `sudo -E`

### Docker

- Docker container examples for Linux, Intel and ARM based Darwin: [SAP/fundamental-tools/docker](https://github.com/SAP/fundamental-tools/tree/main/docker). SAP NWRFC SDK libraries are not included.

## Download and installation

```shell
pip install pyrfc
```

On Windows and macOS platforms pre-built binary wheel is installed, without local compilation. On Linux platform the package is locally built from source distribution.

Build from source distribution can be requested also on other platforms:

```shell
pip install --no-binary pyrfc pyrfc
# or
pip install https://files.pythonhosted.org/packages/.../pyrfc-3.1.0.tar.gz
```

Alternative build from source installation:

```shell
git clone https://github.com/SAP/PyRFC.git
cd PyRFC
# if you use tox
tox -e py311 # for Python 3.11
# or
python -m pip install .
# or
python -m build --wheel --sdist --outdir dist
# or
PYRFC_BUILD_CYTHON=yes python -m build --wheel --sdist --outdir dist
pip install --upgrade --no-index --find-links=dist pyrfc
```

Run ``python`` and type ``from pyrfc import *``. If this finishes silently, without oputput, the installation was successful.

Using virtual environments you can isolate Python/PyRFC projects, working without administrator privileges.

See also the [pyrfc documentation](http://sap.github.io/PyRFC),
complementing _SAP NWRFC SDK_[documentation](https://support.sap.com/nwrfcsdk), especially [SAP NWRFC SDK 7.50 Programming Guide](https://support.sap.com/content/dam/support/en_us/library/ssp/products/connectors/nwrfcsdk/NW_RFC_750_ProgrammingGuide.pdf).

## Getting started

**Note:** The package must be [installed](#download-and-installation) before use.

### Call ABAP Function Module from Python

In order to call remote enabled ABAP function module (ABAP RFM), first a connection must be opened.

```python
from pyrfc import Connection
conn = Connection(ashost='10.0.0.1', sysnr='00', client='100', user='me', passwd='secret')
```

Connection parameters are documented in `sapnwrfc.ini` file, located in the _SAP NWRFC SDK_ `demo` folder. Check also section `4.1.2 Using sapnwrfc.ini` of [SAP NWRFC SDK 7.50 Programming Guide](https://support.sap.com/content/dam/support/en_us/library/ssp/products/connectors/nwrfcsdk/NW_RFC_750_ProgrammingGuide.pdf).

Using an open connection, remote function modules (RFM) can be invoked. More info in [pyrfc documentation](http://sap.github.io/PyRFC/client.html#client-scenariol).

```python
# ABAP variables are mapped to Python variables
result = conn.call('STFC_CONNECTION', REQUTEXT=u'Hello SAP!')
print (result)
{u'ECHOTEXT': u'Hello SAP!',
 u'RESPTEXT': u'SAP R/3 Rel. 702   Sysid: ABC   Date: 20121001   Time: 134524   Logon_Data: 100/ME/E'}

# ABAP structures are mapped to Python dictionaries
IMPORTSTRUCT = { "RFCFLOAT": 1.23456789, "RFCCHAR1": "A" }

# ABAP tables are mapped to Python lists, of dictionaries representing ABAP tables' rows
IMPORTTABLE = []

result = conn.call("STFC_STRUCTURE", IMPORTSTRUCT=IMPORTSTRUCT, RFCTABLE=IMPORTTABLE)

print result["ECHOSTRUCT"]
{ "RFCFLOAT": 1.23456789, "RFCCHAR1": "A" ...}

print result["RFCTABLE"]
[{ "RFCFLOAT": 1.23456789, "RFCCHAR1": "A" ...}]
```

Finally, the connection is closed automatically when the instance is deleted by the garbage collector. As this may take some time, we may either call the close() method explicitly or use the connection as a context manager:

```python
with Connection(user='me', ...) as conn:
    conn.call(...)
# connection automatically closed here
```

Alternatively, connection parameters can be provided as a dictionary:

```python
def get_connection(conn_params):
    """Get connection"""
    print 'Connecting ...', conn_params['ashost']
    return Connection(**conn_param)

from pyrfc import Connection

abap_system = {
    'user'      : 'me',
    'passwd'    : 'secret',
    'ashost'    : '10.0.0.1',
    'saprouter' : '/H/111.22.33.44/S/3299/W/e5ngxs/H/555.66.777.888/H/',
    'sysnr'     : '00',
    'client'    : '100',
    'trace'     : '3', #optional, in case you want to trace
    'lang'      : 'EN'
}

conn = get_connection(**abap_system)
Connecting ... 10.0.0.1

conn.alive
True
```

See also pyrfc documentation for [Client Scenario](http://sap.github.io/PyRFC/client.html)

### Call Python function from ABAP

```python
# create server for ABAP system ABC
server = Server({"dest": "gateway"}, {"dest": "MME"}, {"port": 8081, "server_log": False})

# expose python function my_stfc_connection as ABAP function STFC_CONNECTION, to be called from ABAP system
server.add_function("STFC_CONNECTION", my_stfc_connection)

# start server
server.start()

# get server attributes
print("Server attributes", server.get_server_attributes())

# stop server
input("Press Enter to stop servers...")

server.stop()
print("Server stoped")
```

See also pyrfc documentation for [Server Scenario](http://sap.github.io/PyRFC/server.html) and server example [source code](https://github.com/SAP/PyRFC/blob/main/examples/server).

## SPJ articles

Highly recommended reading about RFC communication and SAP NW RFC Library, published in the SAP Professional Journal (SPJ)

- [Part I RFC Client Programming](https://wiki.scn.sap.com/wiki/x/zz27Gg)

- [Part II RFC Server Programming](https://wiki.scn.sap.com/wiki/x/9z27Gg)

- [Part III Advanced Topics](https://wiki.scn.sap.com/wiki/x/FD67Gg)

## How to obtain support

If you encounter an issue or have a feature request, you can create a [ticket](https://github.com/SAP/PyRFC/issues).

Check out the [SAP Community](https://community.sap.com/) (search for "pyrfc") and stackoverflow (use the tag [pyrfc](https://stackoverflow.com/questions/tagged/pyrfc)), to discuss code-related problems and questions.

## Contributing

We appreciate contributions from the community to **PyRFC**!
See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on our philosophy around extending this module.

## Code of Conduct

See [Code of Conduct](./CODE_OF_CONDUCT.md)
