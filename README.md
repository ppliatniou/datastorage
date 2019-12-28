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
 
This diagram shows how some huge event about new animal that contains thousand of fields goes to central storage, let say that's central animal ministry :D And after some pipeline-process is connected to this worker and filtering and preparing the data by two types of animal - dogs and cats and selects important attributes for those animal species. After filtration this worker stores the prepared data to separated storages for this two types. And this project helps to operate such storages.

# Requirements

* api for creation storages
  
    * primary key type
    * indexes type
    * data fields
    
* each storage should be implemented in separated table

* migrations with backward compatibility, versions of changes

* automatic validation of data by storage structure

* Protection against concurrent changing of data


# Implementation

## Solution overview

This solution solves the problem when some processes require certain storage to save data with defined schema. Each 
storage can validate incoming data and store it to database. Any recipients can get the data from those storages and operate
with this somehow. The storage support changing schemas, but new schema should have backward compatibility with previous one.
That means you can only add new fields with default value. All the old data will be updated with this new field and value. 
Of cource, for test project it doesn't support various types, for first version it's integer and text types.

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
