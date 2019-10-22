# BMAT test

This repository contains the solution for the BMAT technical test. The only requirements to run this demo is having
docker and docker-compose installed.

It has been developed and tested using docker version 18.09.7 and docker-compose version 1.24.1. It may don't work with
lower versions.

The first steps to play this demo:
- Clone or download this repository.
- Create the docker container and do the database migration with the following command:

`cd bmat_test`

`docker-compose run web python /code/manage.py migrate`

- Then run the django server:

`docker-compose up -d`

This will deploy a django app running in background at <http://127.0.0.1:8000>. You can go to django admin view at 
<http://127.0.0.1:8000/admin>, but first create a super user:

`docker-compose run web python /code/manage.py createsuperuser`

When you finish, remember to stop the container:

`docker-compose down`

## Part 1: Works Single View

### Instructions 

I've created a django command `data_cleaning` that will read all csv files of an specific directory. Those csv must 
follow the same format as the example given at the test (there is no format checking before reading).

The specific route will be the folder "raw_data" inside this repo. This is to simplify the demo, a better way should be
creating a shared volume between host and docker container. 

Once you have the files you want to reconcile, run this command:

`docker-compose run web python /code/manage.py data_cleaning`

Then you can go to the django admin panel and check the Songs and Contributors tables.

### Questions
**1- Describe briefly the matching and reconciling method chosen.** 

I've been looking for information about that field because I have no experience on that. It looks like pandas and 
numpy are the most common libraries to use for this type of works, but I don't have the expertise to use them 
efficiently.

I tried to group the records with pandas by iswc, concatenating the contributors and assuming that an iswc code can only
be related with one title. This will only reconcile the records with an iswc informed, blank cases must be treated 
separately.
 
**2- We constantly receive metadata from our providers, how would
you automatize the process?**

One way to automatize this task is having an API or an automation server like Jenkins getting those data updates. Then
configure a trigger to launch the command implemented. If this metadata reception is a really heavy load task, we could 
deploy several containers sharing the same database, or building a new job to reconcile
the different databases periodically.

## Part 2: Works Single View API

Using the Django Rest framework I've implemented a little api that lists all Songs and Contributors. This framework can 
render on a browser the api calls, or use an app like Postman or curl:

- All songs: <http://127.0.0.1:8000/api/songs/>

- All contributors: <http://127.0.0.1:8000/api/contributors/>

The api let you filter songs by iswc by queryparams:

<http://http://127.0.0.1:8000/api/songs?iswc=T0046951705>

### Questions

**1- Imagine that the Single View has 20 million musical works, do
you think your solution would have a similar response time?**

The response time will be worse, the query resolution time will start growing with a few million records. 

**2- If not, what would you do to improve it?**

One solution could be implementing a cache system, like redis.

Other solution could be having all the records distributed in several containers and implement some map/reduce strategy.
Making an api call to all the containers (with a smaller data set, better response time) and reconciling the responses.

## Conclusion

I enjoyed doing this tech test. It has been a long time since my last Django project, I had to re-learn a lot about it. 
Also, I've never used the Django Rest framework before and it made incredible easy to implement a simple api. I realized 
that the contributors records inside the songs response are a link to the contributors api instead of the contributor 
name, I would like to implement it that way but I can't afford more time doing this test. For the same reason I didn't 
implemented unit tests and did not cover all the cases of the works-metadata reconcile.
