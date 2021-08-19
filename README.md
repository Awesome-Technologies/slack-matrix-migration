# slak-matrix-migration

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
new_project_name=slak-matrix-migration
new_project_name_constant=$(echo ${new_project_name^^}| tr "-" "_")
new_project_name_snake=$(echo ${new_project_name}| tr "-" "_")
find . -path ./.git -prune -false -o -type f -exec sed -i "s/slak-matrix-migration/${new_project_name}/g" {} \;
find . -path ./.git -prune -false -o -type f -exec sed -i "s/SLAK_MATRIX_MIGRATION/${new_project_name_constant}/g" {} \;
find . -path ./.git -prune -false -o -type f -exec sed -i "s/slak_matrix_migration/${new_project_name_snake}/g" {} \;
mv slak-matrix-migration/slak-matrix-migration slak-matrix-migration/${new_project_name}
mv slak-matrix-migration ${new_project_name}
```
# Build And Push to docker registry

``` bash
version=0.1.1
docker build --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --build-arg VCS_REF=$(git rev-parse --short HEAD)  -t sapian/slak-matrix-migration:latest -t sapian/slak-matrix-migration:${version} --build-arg VERSION=${version} .
```

# build multiarch and push

``` bash
version=0.1.1
docker buildx build --push \
    --platform linux/arm64/v8,linux/amd64,linux/arm/v7 \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg VCS_REF=$(git rev-parse --short HEAD) \
    --tag custom/slak-matrix-migration:latest \
    --tag quay.io/custom/slak-matrix-migration:latest \
    --tag custom/slak-matrix-migration:${version} \
    --tag quay.io/custom/slak-matrix-migration:${version} \
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
docker run --env-file .env --rm -it sapian/slak-matrix-migration:latest
```

# Set developing enviroment

``` bash
conda create -n slak-matrix-migration python=3.9
/opt/$USER/anaconda3/envs/slak-matrix-migration/bin/pip install pipenv
/opt/$USER/anaconda3/envs/slak-matrix-migration/bin/pipenv --python=/opt/$USER/anaconda3/envs/slak-matrix-migration/bin/python install
/opt/$USER/anaconda3/envs/slak-matrix-migration/bin/pipenv --python=/opt/$USER/anaconda3/envs/slak-matrix-migration/bin/python install --dev
```

## Ipyhon

``` bash
cd ~/Workspace/slak-matrix-migration/
conda activate slak-matrix-migration
/opt/$USER/anaconda3/envs/slak-matrix-migration/bin/pipenv run ipython
```
