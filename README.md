# datastorage
Test project of data storage on django/python

# Problem

There are needs to store many different entities that can be got by some unique key. Data structure of those entities are 
 various. Entity should support indexes for fast searching and also should store various data structure. Data structure 
 can be updated and in this case should support backward compatibility. Each storage should provide validation by their
 structure and have protection against concurrent access.
 
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
