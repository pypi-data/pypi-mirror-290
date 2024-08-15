# Projektarbeit in Softwareentwicklung 2

- Python package: [ensemble_package](ensemble_package)
  - The package is deployed at pypi
  - The url is the following: (https://pypi.org/project/ensemble-package/)


- Docker commands to operate the [Dockerfile](Dockerfile)
  - docker build -t my-flask-app .
  - docker run -d --name rest_api -p 5000:5000 my-flask-app:latest
  - docker stop rest_api


- Gitlab-pipeline commands for Docker:
  - docker login gcr.web.fh-kufstein.ac.at
  - docker pull gcr.web.fh-kufstein.ac.at/meierflorian/project_software_entwicklung_2
  - docker run -d -p 5000:5000 gcr.web.fh-kufstein.ac.at/meierflorian/project_software_entwicklung_2:latest


- the REST-API file is [rest_api](rest_api.py)
  - It should be deployed via Docker
  - If wished, the file can be run manually

- The requestfile for testing the deployed API is available at [request_api.http](request_api.http)
  - Possible regressors are: ['linear_regressor', 'nearest_neighbor_regressor', 'ridge_regressor']


- The testing is available at [unit_testing.py](ensemble_package/unit_testing.py)
  - command: py -m ensemble_package.unit_testing