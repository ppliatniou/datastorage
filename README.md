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

* optimistic locking


# Implementation



# API


# Run example


# development environment


# src structure


# testing
