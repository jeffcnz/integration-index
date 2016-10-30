#Integration Index

##Introduction
The intent of this project was to produce a proof of concept Integration Index, as described in http://www.bom.gov.au/environment/doc/NEII_Reference_Architecture.pdf, but for New Zealand environmental data.  The LAWA data infrastructure was used to provide the data.  The integration index effectively provides a discovery and translation service sitting over existing time series server services operated by a variety of agencies.

It uses a flask application linked to a Postgresql database using SQLAlchemy.

##Getting Started
The repository is setup to run using Vagrant to create a virtual machine. 

Fork the repository into a directory called vagrant.  

From a terminal navigate to the vagrant directory and enter 'vagrant up'.

This will initialise the machine, build the database and start the app.

Once all of the installation is complete the app will be available in your browser at http://localhost:5000/

Ctrl C will stop the app and return to the terminal prompt.

Entering 'vagrant ssh' will link to the virtual machine.  Navigate to '/vagrant/Integration' to access the files.

'python integration.py' will restart the app.

The code provided is a development version and the app will restart each time integration.py is saved.

##Initialisation
The database is built and populated by running 3 scripts in order.  This is done on 'vagrant up', but if the database needs to be refreshed or rebuilt it can be done by running the following commands from the ssh terminal.

'python database-setup.py' - creates the database structure
'python base_data_load.py' - loads the data from the base_data.py file.
'python sites_data_load.py' - loads site information from LAWA monitoringsitesreferencedata WFS. Requires a valid url to be provided in the base_data.py file, and the WFS to conform to the LAWA data specification.

'python integration.py' - starts the application

