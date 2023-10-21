##### Please note that you will need to fork this repository and then clone your own version of it on your computer, otherwise you will not be able to contribute.

### Installing Docker on your machine

If you already have Docker installed on your computer, please ignore this section.

- For Windows users: It is recommended that you install WSL 2 from [here](https://learn.microsoft.com/en-us/windows/wsl/install) before installing Docker as it is the preferred way to virtualize your containers.

You can download Docker Desktop from [here](https://www.docker.com/products/docker-desktop/).

Once you go through the installation process, you can verify if Docker has been installed successfully by opening a terminal and running:

```bash
docker --version
```

```bash
docker-compose --version
```

If you get an error, please refer to the documentation [here](https://docs.docker.com/).

### Initializing the project on your machine

Fork the repository and clone it on your computer.

Follow the instructions [here](https://github.com/WADC-IITGN/insiit-db#setting-up-the-database-on-a-new-machine) to initialize the database on your computer.

### Running the API

Every time before starting the API, you will have to start the database, the instructions to which can be found [here](https://github.com/WADC-IITGN/insiit-db#setting-up-the-database-on-a-new-machine)

Then, open a terminal in the root of the repository and run the following command:

```bash
docker-compose up --build
```

You should now see uvicorn logs in your terminal like so:

```console
insiit-api  | INFO:     Will watch for changes in these directories: ['/code']
insiit-api  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
insiit-api  | INFO:     Started reloader process [1] using WatchFiles
insiit-api  | INFO:     Started server process [8]
insiit-api  | INFO:     Waiting for application startup.
insiit-api  | INFO:     Application startup complete.
```

\
To stop a container that is already running in your terminal, press CTRL+C to exit out of the container. Then, run the following command:

```bash
docker-compose down
```

\
If you wish to run commands inside the Docker container, open a new terminal and
run the command:

```bash
docker exec -it insiit-api bash
```

Please note that this will be a Linux environment and any commands you run will be run inside the container. For example:

```console
PS C:\Users\Mayank> docker exec -it insiit-api bash
root@c9b3a93df5e9:/code# whoami
root
root@c9b3a93df5e9:/code# pwd
/code
root@c9b3a93df5e9:/code# ls
__init__.py  __pycache__  app  appTypes  config.py  main.py
```

### Contributing to the repository

Whenever you commit any new changes, make sure to push them to your forked version of the repository. Then, create a new pull request and provide a meaningful summary and description. After review, your commit will be merged to this repository.
