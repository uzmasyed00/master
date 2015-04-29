# master
Install Git,Vagrant and VirtualBox.
Clone the https://github.com/uzmasyed00/master repository to your local machine.
Using the terminal, change directory to fullstack/vagrant (cd fullstack/vagrant), then type "vagrant up" to launch your virtual machine followed by "vagrant ssh".
CD into vagrantfullstack//tournament where you will find the 3 files for this project:
 	tournament.sql - where the database schema in the form of sql commands is present.
	tournament.py - where the code for the tournament module is present.
	tournament_test.py - where all tests for functions in tournament.py is present.
In order to run the sql commands in tournament.sql, connect to the psql forum on the Vagrant machine by typing "psql forum".
Then, type each command listed in tournament.sql to create the database and tables in the database.
Exit out of the psql forum by typing by typing "\q".
Once the database and tables are created, run the tournament_test.py by typing "python tournament_test.py". This will generate the output of the tests.

