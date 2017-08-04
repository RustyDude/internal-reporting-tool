# Project: Log Analysis

A **SQL Query Project**, replicating a given mock-up live database using **Postgresql** and **Python** to create a reporting tool that produces a plain text file containing answers to 3 specific questions.

## Requirements

* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Virtual Machine](https://www.virtualbox.org/wiki/Downloads)
* [Python3](https://www.python.org/downloads/)
Or if you already have it, upgrade Python through _pip_:
```pip install 'python>=3'```

## Get it started.

### Setting up VM configuration

* Download and unzip [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/May/59125904_fsnd-virtual-machine/fsnd-virtual-machine.zip). Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.

### Downloading a copy
* **Fork** the [repository](https://github.com/russeladrianlopez/internal-reporting-tool). _(You may fork or not totally up to you)_

* Once you have your own repository. **You may click Clone or download**, then use _HTTPs section_ and copy the clone URL. (Put it inside your vagrant subdirectory)

### Start the virtual machine

* Once inside the vagrant subdirectory, run the command:
```vagrant up```

* Upon installation, run this command to log you inside the VM.
```vagrant ssh```

### Set up the database
* Unzip **newsdata.zip**. now you should have a folder called "_**newsdata**_" which contains the following:
    * **newsdata.sql** - creates the tables and alterations neccesary for the news database.
    * **database_setup.sql** - setup the news database and creates views neccesary.


* Once logged on in vagrant, to load the data and create the database, run this command inside the **"newsdata"** folder:
```psql -f database_setup.sql```

* For more information on the views required for the queries. [See Views Below.](#views)

### Running the report tool
* Run this command:
``` python3 report.py```
_This should result in a creation of a file called "**reportfile.text**"_

## Questions

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Views
* **viewcount** - counts the views per article _(Used in Questions 1 & 2)_
```
create view viewcount as
select ar.author as id, ar.title, l.view_count
from articles as ar left join (
    select path, count(path) as view_count
    from log
    where status like '%200%'
group by log.path)
as l
on ar.slug = substring(l.path from 10);
```

* **log_errors** - tallies the logs and errors per each day. _(Used in Question 3)_
```
create view log_errors as
select date_trunc('day', time) as date, count(*) as logs, sum(case when status='404 NOT FOUND' then 1 else 0 end) as errors
from log
group by date;
```

* **percentage** - calculates the percentage of error per day. _(Used in Question 3)_
```
create view percentage as
select date, round((errors/logs::numeric)*100,2) as error_percentage
from log_errors
group by date, errors, logs
order by error_percentage desc;
```

Nanodegree Course courtesy of [Udacity](https://www.udacity.com/).
