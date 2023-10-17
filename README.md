### Initializing the project on a new machine

After cloning the repository in your desired location, please follow the following instructions to make sure you are able to run the project on your machine.

- Open a terminal in the root of the project directory\
  Run the following commands on your terminal:\
  `$ cd api && python -m venv venv`\
  `$ cd venv/Scripts && ./activate && cd ../../`\
  `$ pip install -r requirements.txt`

- All the requirements for the API should now be installed.\
  To run the API on localhost, run the following commands in the project's **root** directory:\
  `$ cd api/venv/Scripts && ./activate && cd ../../`\
  `$ cd src && python main.py`\
  This should launch the uvicorn server on port 8000 (default).
- To test if it is running correctly, launch
  [Postman](https://www.postman.com/downloads/).\
  Create a new HTTP request. Set the method to `GET` and the url to
  [http://localhost:8000](http://localhost:8000).\
  Go to the headers tab and add a new header with the name `x-api-key`, and the value as the value of the `test` key in the `api-keys` object inside the `api-config.json` file, present in the `/api` folder of the project root directory.\
  Send the request. You should get the following response:\
  `{"message": "hello world"}`

### Pulling new changes from the repository

Please note that any time you pull new changes from the repository,
please run the following commands in the project's root directory to update the requirements:\
`$ cd api/venv/Scripts && ./activate && cd ../../`\
`$ pip install -r requirements.txt`
