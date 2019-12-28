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

```json
{
    "name": "dog
    "key": {"name": "chip_id", "type": "string", "max_length": 16},
    "fields": [
        {"name": "color", "type": "string", "max_length": 32. "db_index": true},
        {"name": "collar_size", "type": "integer"}        
    ]
}
```

cat

```json
{
    "name": "dog
    "key": {"name": "chip_id", "type": "string", "max_length": 16},
    "fields": [
        {"name": "color", "type": "string", "max_length": 32. "db_index": true},
        {"name": "collar_size", "type": "integer"}        
    ]
}

```

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


# development environment


# src structure


# testing
