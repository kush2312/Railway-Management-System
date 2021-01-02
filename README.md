# Railway-Management-System
E-Railway Management System is the cumulation of all aspects related to train journey. Right from easy ticket booking over the internet, which avoids long queues, tracking the booking status, the train status, schedules to checking out nearby tourist attractions, this service covers it all. The website solves multiple issues for users such no waiting in queues for booking tickets, anywhere-anytime access to transactions and bookings, and easy process for booking and checking availability and train status.

On the other hand, E-Railway Management System provides and easy and efficient way for railway authorities to manage the train schedules and routes. Not only can the railway authorities update the schedules of the trains, they can also add new trains to the system. This allows the authorities to have centralized portal for management. Also, they can update the seat status of any of the classes of the train and regulate the fare prices to suit their needs.


## Setup

* Clone the repository
```bash
$ git clone https://github.com/Saif807380/Railway-Management-System
```
* Create a virtual environment and install all dependencies from the requirements.txt file
```bash
$ virtualenve your_env
$ source your_env/bin/activate
$ pip install -r requirements.txt
```
* Install wkhtmltopdf, a command line tool to render HTML into PDF using the Qt WebKit rendering engine, required by pdfkit.
 * For MacOS
 ```bash
  $ brew install wkhtmltopdf
 ```
 * For Linux
 ```bash
 $ cd ~
 $ wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
 $ tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz 
 $ cp wkhtmltox/bin/wk* /usr/local/bin/
 ```
 * For Windows
 Download wkhtmltopdf from [here](https://wkhtmltopdf.org/downloads.html)

* Set the path of wkhtmltopdf in the config variable in routes.py

*	From the command line, go to the project folder and execute run.py.

*	Check server is running and then from your browser visit http://localhost:5000 

## Screenshots

![Book Tickets](https://github.com/Saif807380/Railway-Management-System/blob/master/Images/Screenshot%202020-04-27%20at%2017.59.41.png)

![Features](https://github.com/Saif807380/Railway-Management-System/blob/master/Images/Screenshot%202020-04-27%20at%2018.02.16.png)

![Fare Chart](https://github.com/Saif807380/Railway-Management-System/blob/master/Images/Screenshot%202020-04-27%20at%2018.02.25.png)

![Bookings](https://github.com/Saif807380/Railway-Management-System/blob/master/Images/Screenshot%202020-04-27%20at%2018.02.33.png)

![Ticket](https://github.com/Saif807380/Railway-Management-System/blob/master/Images/Screenshot%202020-04-27%20at%2017.14.13.png)

![Admin Add Trains](https://github.com/Saif807380/Railway-Management-System/blob/master/Images/Screenshot%202020-04-27%20at%2018.03.27.png)
