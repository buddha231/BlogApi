# BlogApi
Backend Part of the fullstack blogging app

## Docker
You can build and run the docker image using the following command. Make sure you are in the project root
``` bash
docker build -t blog-app .
```

```bash
docker run --rm -d -p 8002:8000 -t blog-app 
```
* Here the --rm argument deletes the container automatically after closing. This is good when creating a temprorary container
* -d argument specified to detach the container from the shell
* -p host_port:container_port. Here the port 8000 in the docker container is mapped to 8002 of the host
* -t gives tag-name toe the image
* Now the api's can be accessed via http://0.0.0.0:8002/api/

## Stacks Used
* The media file is hosted on **Cloudinary Storage**
* **ElephantSQLs**  free postgres instance is used for database
* The API's are created using **Django-Rest-Framework**
