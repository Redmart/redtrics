RedMart Github Metrics
======================

Redtrics generates metrics about the use of Github by developers.

Contributors
------------
- Aniceto Garcia (Concept & Developer)
- Alberto Resco (Developer & Main Contributor)
- Benjos Antony (Developer)
- Mick Jermsack (Developer)
- Sonia Fabre (UI Design)

External Dependencies
---------------------
- InfluxDB
- Github

Setup
-----

### Install InfluxDB

Please follow instructions in https://docs.influxdata.com/influxdb/

### Install binary

You can install the stable build by running:

```bash
$ pip install redtrics
```

or install the latest build:

```bash
$ curl -o redtrics.zip https://github.com/RedMart/redtrics/archive/master.zip
$ unzip redtrics.zip
$ cd redtrics
$ python setup.py install
```

### Setup settings

Some settings set with default values but we encourage you to setup properly for your current needs.
You must create the file `/opt/redtrics/etc/settings.py`

```python
github_token = 'your_github_token'
github_organization = 'Your Organization'
```

```python
influxdb_settings = {
    'host': 'localhost',
    'database': 'redtrics',
    'username': 'redtrics',
    'password': 'redtrics'
}
```

```python
email = {
    'from_email': 'change@me.com',
    'from_name': 'Tech Weekly Metrics',
    'to': ['change@me.com'],
    'smtp_host': 'smtp.example.com',
    'smtp_port': '25',
}
```

### Overwrite mail template

If you want to create your own template you must create your own in the file `/opt/redtrics/templates/mail.html` providing the [metrics](#metrics) you want to show.

<a name="metrics"></a>Metrics provided
------------------------------------

### Branch Build Status

```
    {
        'build_status': {
            'success': 10,  # number of travis builds succeded
            'failure': 2   # number of travis builds failed
        }
    }
```


### Commits on the last week (7 previous days)

```
	{
        'commits_last_week': {
            'commits': 15,  # number of commits
            'additions': 100,  # lines added
            'deletions': 50,  # lines deleted
            'biggest': 20  # biggest commit (lines added + deleted)
        }
    }
```

### Pull Requests stats

``` 
    {
        'pr_stats': {
            'closed': {
                'age': {
                    'max': 1000,  # in seconds
                    'min': 200,  # in seconds
                    'avg': 450, # in seconds
                },
                'commits': {
                    'pr_count': 4,  # number of Pull Requests
                    'commits_count': 14,  # total number of commits in all Pull Requests
                    'additions': 1000,  # total lines added
                    'deletions': 1000,  # total lines deleted
                    'biggest': 1000  # biggest Pull Request (lines added + deleted)
                }
            },
            'open': []  # List of PullRequest objects
        }
    }
```


_Handcrafted with ♥ at RedMart._

All Rights Reserved.
