# Project: Log Analysis

A **SQL Query Project**, replicating a given mock-up live database using **Postgresql** and **Python** to create a reporting tool that produces a plain text file containing answers to 3 specific questions.

## Requirements

* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Virtual Machine](https://www.virtualbox.org/wiki/Downloads)
* [Python3](https://www.python.org/downloads/)
Or if you already have it, upgrade python through _pip_:
```pip install 'python>=3'```

## Get it started.

### Setting up VM configuration

* Download and unzip [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/May/59125904_fsnd-virtual-machine/fsnd-virtual-machine.zip). Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.

### Downloading a copy
* **Fork** the [repository](https://github.com/RustyDude/internal-reporting-tool). _(You may fork or not totally up to you)_

* Once you have your own repository. **You may click Clone or download**, then using _HTTPs section_ copy clone URL. (Put it inside your vagrant subdirectory)

### Start the virtual machine

* Once inside the vagrant subdirectory, run the command:
```vagrant up```

* Upon installation, run this command to log you inside the VM.
```vagrant ssh```

### Set up the database
* Unzip **newsdata.zip**. now you should have a file called "_**newsdata.sql**_"

* Once logged on in vagrant, load the data into the database, run this command:
```psql -d news -f newsdata.sql```

* Setup views required in the queries. [See Below.](#views)
You need to create those views else the program won't work.

### Running the report tool
* Run this command:
``` python3 report.py```
_This should result into a creation of a file called "**reportfile.text**"_

## Questions

* 1. What are the most popular three articles of all time?
* 2. Who are the most popular article authors of all time?
* 3. On which days did more than 1% of requests lead to errors?

## Views
* **viewcount** - counts the views per article _(Used in Questions 1 & 2)_
```
create view viewcount as select ar.author as id, ar.title, count(l.path) as view_count
from articles as ar left join log as l
on ar.slug = substring(l.path from 10)
group by ar.author, ar.title;
```

* **log_errors** - tallies the logs and errors per each day. _(Used in Question 3)_
```
create view log_errors as
select to_char(time, 'FMMonth DD, YYYY') as date, count(*) as logs, sum(case when status='404 NOT FOUND' then 1 else 0 end) as errors
from log
group by date;
```
* **percentage** - calculates the percentage of error per day. _(Used in Question 3)_
```
create view percentage as select date, round((errors/logs::numeric)*100,1) as error_percentage
from log_errors
group by date, errors, logs
order by error_percentage desc;
```

Nanodegree Course courtesy of [Udacity](https://www.udacity.com/).