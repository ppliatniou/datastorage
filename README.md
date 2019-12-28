# datastorage
Provides API-service for arranging data storages with various structure and supports CRUD-operation for those storages.
Each storage is created by declarative structure and has endpoint for all operations. Endpoint for accessint storage supports 
pagination, filtering and protection agains concturrent updating (optimistic locking).
This projects has been built on:
* Django
* rest_framework
* Postgres

As demo project too many things are simplified :) But it doesn't matter it could be made better.

# Problem

In the situations when something generates big and unstructured events the endpoint data can be a pain for receivers that need to 
 work with objects that have certain and defined structure. For example process of selling products on onlain shops can have too much data, and certain consumer needs only data about product and when it has been sold. And other data about price, customer and etc is not important for this consumer. But let's see another process:
 
![Process diagram](docs/img/animal_process.JPG)
 
This diagram shows how some data broker is getting too many unstructured items about new animal that contain thousand of fields. Let say that's central animal ministry :D And after some worker is reading all those items and filtering and preparing the data by two types of animal - dogs and cats and selects important attributes for those animal species. After filtration this worker stores the prepared data to separated storages for this two types. **And this project helps to operate such storages.** All those two storages can get new or updated information from other sources, and also have too many consumers.

# Requirements

* api for creation storages
  
    * primary key type
    * indexes type
    * data fields
    
* each storage should be implemented in separated table

* migrations with backward compatibility, versions of changes

* automatic validation of data by storage structure

* Protection against concurrent changing of data

As demo project some functionality is simplified: it will support only few types: int, long, string and text, all the fields should be required, supports only backward compatibility and doesn't support changing of previous data structure.


# Implementation

## Solution overview

This solution solves the problem when some processes require certain storage to save data with defined schema. Each 
storage can validate incoming data and store it to database. Any recipients can get the data from those storages and operate
with this somehow. The storage support changing schemas, but new schema should have backward compatibility with previous one.
That means you can only add new fields with default value. All the old data will be updated with this new field and value. 
Of cource, for test project it doesn't support various types, for first version it's integer and text types.

In our example with animals we need to create two storages for dogs and cats.

Storage for dogs can have the next atributes:

* chip_id - unique identifier

* color - string describes the color, need to filter by this field

* collar_size - integer describes collar size in cm

for cats:

* chip_id - unique identifier

* color - string describes the color, need to filter by this field

* description - text describes a cat shape

For application declaration such entities have the next definitions:

dog 

```
{
    "name": "dog",
    "key": {"name": "chip_id", "type": "string", "max_length": 16},
    "fields": [
        {"name": "color", "type": "string", "max_length": 32, "db_index": true},
        {"name": "collar_size", "type": "integer"}        
    ]
}
```

cat

```
{
    "name": "cat",
    "key": {"name": "chip_id", "type": "string", "max_length": 16},
    "fields": [
        {"name": "color", "type": "string", "max_length": 32, "db_index": true},
        {"name": "description", "type": "text"}        
    ]
}
```
Storages can be created with the next endpoint of storage factory:

```
curl -X POST http://127.0.0.1:8010/api/v1/factory/storage/ -H "Content-Type: application/json" -d '<cat and/or dog definition>'
```

Storages have been created! To operate this storage there are new endpoints appeared:

http://127.0.0.1:8010/api/v1/storage/dog/

Data example:

```
{
    "chip_id": "CHIP1",
    "color": "red",
    "collar_size": 40
}
```

* http://127.0.0.1:8010/api/v1/storage/cat/

Data example:

```
{
    "chip_id": "CHIP2",
    "color": "red",
    "collar_size": 40
}
```

All such endpoints support GET, POST methods for list and create fields. If field defined as db_index it is available as filter field 
as query argument (also list can be filtered by key field). To access item by id you can use http://127.0.0.1:8010/api/v1/storage/god/<chip_id>/ and there are methods PUT, GET and DELETE allowed.

# API

### GET /api/v1/factory/storage/

List of all storage items. 

### POST /api/v1/factory/storage/

### GET /api/v1/factory/storage/{storage_name}/

### GET /api/v1/factory/ready_status/{storage_name}/

### GET /api/v1/storage/{storage_name}/

### POST /api/v1/storage/{storage_name}/

### GET /api/v1/storage/{storage_name}/{key}/

### DELETE /api/v1/storage/{storage_name}/{key}/

# Run example

To run application simply you can use built in docker settings. From the root of repo directory run the next command:

> docker-compose build

> docker-compose up

The project will be available on address 

# development environment

Project settings can be redefined with file settings_local.py in directory src/datastorage.

Before attempts to run the project the next steps can help:

>cd dev

>docker-compose up

Thhis docker setting run database and other environment for the project.

For running application there are the next steps:

Build environment on python3.6

> virtualenv dsenv --no-site-packages

Apply environment

> . dsenv/bin/activate

Install python packages

> pip install -r src/requirements.txt

Go to app directory 

>cd src/datastorage

Run migrations

> python manage.py migrate

Start application

> python manage.py runserver

In other terminal window activate environment and run celery worker:

> celery -A sandboxpy worker -l debug

# testing

In your applied dev environment install tox

> pip install tox

Run tox

> tox

# src structure

