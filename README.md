# python-pip-docker-template

<img src="wiki/images/Logo_circular_python_name_bg_600dpi.png" width="600">

Here is a simple repo template for python pip Docker Projects (Sapian Standar)

# Features

- Python
- Docker (Miocroservicios)
- pip (pipenv and pip setup)
- kubernetes (Helm Chart)
- Metrics (Prometheus)
- docker buildx (Multiarch)

# using this template
``` bash
new_project_name=new-name
new_project_name_constant=$(echo ${new_project_name^^}| tr "-" "_")
new_project_name_snake=$(echo ${new_project_name}| tr "-" "_")
find . -type f -exec sed -i "s/python-pip-docker-template/${new_project_name}/g" {} \;
find . -type f -exec sed -i "s/PYTHON_PIP_DOCKER_TEMPLATE/${new_project_name_constant}/g" {} \;
find . -type f -exec sed -i "s/python_pip_docker_template/${new_project_name_snake}/g" {} \;
mv python-pip-docker-template/python-pip-docker-template python-pip-docker-template/${new_project_name}
mv python-pip-docker-template ${new_project_name}
```
# Build And Push to docker registry

``` bash
version=0.1.1
docker build --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --build-arg VCS_REF=$(git rev-parse --short HEAD)  -t sapian/python-pip-docker-template:latest -t sapian/python-pip-docker-template:${version} --build-arg VERSION=${version} .
```

# build multiarch and push

``` bash
version=0.1.1
docker buildx build --push \
    --platform linux/arm64/v8,linux/amd64,linux/arm/v7 \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg VCS_REF=$(git rev-parse --short HEAD) \
    --tag custom/python-pip-docker-template:latest \
    --tag quay.io/custom/python-pip-docker-template:latest \
    --tag custom/python-pip-docker-template:${version} \
    --tag quay.io/custom/python-pip-docker-template:${version} \
    .
```

# Run For Testing

## Set Enviroment variables
Fill de file `.env`

``` ini
LOG_LEVEL=INFO
```

## Run

``` Bash
docker run --env-file .env --rm -it sapian/python-pip-docker-template:latest
```

# Set developing enviroment

``` bash
conda create -n python-pip-docker-template python=3.9
/opt/$USER/anaconda3/envs/python-pip-docker-template/bin/pip install pipenv
/opt/$USER/anaconda3/envs/python-pip-docker-template/bin/pipenv --python=/opt/$USER/anaconda3/envs/python-pip-docker-template/bin/python install
/opt/$USER/anaconda3/envs/python-pip-docker-template/bin/pipenv --python=/opt/$USER/anaconda3/envs/python-pip-docker-template/bin/python install --dev
```

## Ipyhon

``` bash
cd ~/Workspace/python-pip-docker-template/
conda activate python-pip-docker-template
/opt/$USER/anaconda3/envs/python-pip-docker-template/bin/pipenv run ipython
```
