import mygeotab
from collections import namedtuple

def from_credentials(credentials):
    creds = {
        'username': credentials['username'],
        'password': credentials['password'] if 'password' in credentials else None,
        'database': credentials['database'],
        'session_id': credentials['session_id'] if 'session_id' in credentials else None,
        'server': credentials['server'] if 'server' in credentials else 'my.geotab.com'
    }

    nt = namedtuple('credentials', creds.keys())(*creds.values())
    return mygeotab.API.from_credentials(nt)

def authenticate(username, password, database, server=None):
    client = mygeotab.API(username=username, password=password, database=database) if server == None else mygeotab.API(username=username, password=password, database=database, server=server)
    client.authenticate()
    return client