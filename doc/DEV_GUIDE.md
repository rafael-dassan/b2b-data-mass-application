# Dev Guide
This document describes some Data Mass usage guides.

## Contents:
  - [Contents:](#contents)
    - [Data Mass Architecture](#data-mass-architecture)

### [Data Mass Architecture](#architecture)
Most Data Mass service packages are separated between two important modules: relay and service. We use `relay.py` for data manipulation (POST, PUT and DELETE), and `service.py` for data retrieval (query).

There are some exceptions for packge services that follow a different rule because they are mostly used in the project, such as `data_mass.accounts`, `data_mass.supplier` and `data_mass.user`.
