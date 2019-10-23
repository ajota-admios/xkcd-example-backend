# xkcd-example-backend

Once located in the repo folder, run:
```
docker image build --tag xkcd-backend .
docker container run --rm --volume "$(pwd)":/var/app xkcd-backend
```
