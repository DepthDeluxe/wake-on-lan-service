# Wake on Lan Service
This service will make it easy to wake computers over distant network connections by leveraging HTTP.

## Developing
1. Create a new virtual environment in the top-level directory and source the environment.
2. `python setup.py develop` will install all packages in development mode.
3. Create a `config.ini` file in the root project directory and place the following configuration in it
   ```ini
   [database]
   path = :memory:
   ```
   This will tell the service to use an in-memory SQLite database that will clear on app restart.

4. `python -m wolservice.wsgi` will launch the service in the local development mode.

## Onboarding a Host
In powershell, run the following command.  This will only work if the host `<your host>` is active on the network and registered in DNS.

```powershell
curl -XPUT 'http://localhost:5000/<your hostname>'
```

## Dockerfile
This project is set to build a Docker version as well.  By default, it uses the config file located in `extra/config.ini`.