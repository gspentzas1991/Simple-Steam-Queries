Simple-Steam-Queries
=========
A python module that allows you to easily run Steam client `Master Server Query Protocol <https://developer.valvesoftware.com/wiki/Master_Server_Query_Protocol>`_ queries

Install
-------

Install latest release version from PYPI:

.. code:: bash

    pip install Simple-Steam-Queries
    
Usage Guide
-------
Steam server queries are being run through the steam client. Simple-Steam-Queries uses the `ValvePython steam <https://github.com/ValvePython/steam>`_ client module to execute the queries.

* The first step is to login to the steam client by calling the sign_in function with a steam account's username and password credentials. If the account requires 2FA, it will be asked on the commandline. It's recomended to use a secrets.env file for this (`see example <https://github.com/gspentzas1991/GameSnoop-Server/blob/37d79c45328f36d9b70133b59a9999cacfbdbbf5/server.py#L187>`_)
* In order to build your query, you need to create a list of SteamQueryParam objects. These objects describe the types of servers you want to receive with an implicit logical AND between the parameters

Example:

.. code:: python

    params = [SteamQueryParam.Secure,SteamQueryParam.NotEmpty] 
    
describes a query that will search for password protected and not empty steam servers

* After you created your SteamQueryParam list, you call the SteamServerQuery() function and pass your parameter list to it. This will return a list of steam servers that comply to your parameters

Logic Operators
-------
Each SteamQueryParam on your parameter list is implicitely connected with a logical AND. You can apply other logic operations by using the generate_logical_query function.

Example:

.. code:: python

  params = [SteamQueryParam.Secure,SteamQueryParam.NotEmpty]
  SteamQueryParam.generate_logical_query(Logical.OR,params)
  
This will return a query that will return servers that are either password protected or not empty

The library supports the OR, AND, NOR, NAND operators

Notes
-------
Steam queries seem to return a maximum of 20k servers per request. If you need bigger results you will need to break the query into multiple smaller queries and collect the results together (`see example <https://github.com/gspentzas1991/GameSnoop-Server/blob/37d79c45328f36d9b70133b59a9999cacfbdbbf5/server.py#L117>`_)
