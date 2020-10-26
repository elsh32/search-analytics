# SearchAnalytics API 

### Technologies
SearchAnalytics API uses some open source projects to work properly:

* [Python 3] - a programming language that lets you work quickly and integrate systems more effectively!
* [Falcon Framework] - a blazing fast, minimalist Python web API framework for building reliable app backends and microservices.
* [Docker] - the de facto standard to build and share containerized apps - from desktop, to the cloud.
* [Supervisor] - supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.
* [Guinicorn] - python WSGI HTTP Server for UNIX.

## Project structure
    │── api                                              # Api code 
    │   │── main
    │   │     │── computer                               # Data computer
    │   │     │     │── __init__.py                
    │   │     │     │── analytics_computer.py            # Contains a Singleton class that compute search analytics
    │   │     │── helper                                 # helpers
    │   │     │     │── __init__.py                
    │   │     │     │── helpers.py                       # Falcon middleware and helper methods
    │   │     │── loader                                 # Data Loader
    │   │     │     │── __init__.py                
    │   │     │     │── queries_log_ingestor.py          # Load and ingest TSV file at API initialisation
    │   │     │── ressource                              # Rest API endpoints  
    │   │     │     │── __init__.py                  
    │   │     │     │── search_analytics_ressources.py   # Analytics endpoints
    │   │     │── service                                # Services
    │   │     │     │── __init__.py                 
    │   │     │     │── search_analytics_service.py      # Analytics service
    │   │     │── utility                                # Global utilities
    │   │     │     │── __init__.py                 
    │   │     │     │── constants.py                     # Constants of the project
    │   │     │── __init__.py
    │   │── static                                       # Static files
    │   │     │── file                                   # Files
    │   │     │     │── hn_logs.tsv                      # Log file to ingest
    │   │     │── v1                                     # V1 swagger API DOC
    │   │     │     │── swagger.json                     # Swagger API documentation file
    │   │── test                                         # API test           
    │   │── __init__.py                                  # Init of the project where TSV file is loaded
    │   │── server.py                                    # Api main starter file
    │   │     │── ...
    │── launcher.conf           #  supervisord conf file for the project
    │── Dockerfile              #  docker deployment file
    │── requirements.txt        #  python required libs file
    │── run_server_deploy.sh    #  bash script to build and run docker project  
    └── ...

### Running with Docker (Prefered)
- Clone the project
- Add the *hn_logs.tsv*  in *api/static/file* folder
- If you don't have docker installed on your machine. Kindly follow [the docker official guide] to install it before executing the command below.
- Also, please make sure the port 8080 is not used on your machine
- At the root of the project, please run the following command to build and run the API


    $ sh run_server_deploy.sh
    
- After running the command above, wait until the installation is done and the file is uploaded
- Head over to the URL bellow to test the API. If the APi didn't load, the file is probably being laoding. Just wait a few minutes and reload the link :)
    
        http://localhost:8080/v1/doc
    
    
### Thought Process
To build the API, i basically have two options in mind:
- Compute the analytics informations at request time (slower).
- Pre-compute the analytics informations at file ingestion and serve directly the result at request time.

I have decided to go with the second approach. Since i can not use an external database to store the data of the log file, i needed a way to load this  into memory
and have it available through out the life cycle of the API. I decided then to go with the Singleton Pattern with the class (*AnalyticsComputer* [api/main/computer/analytics_computer.py]). This class will be responsible to hold all the processed data from the TSV file and the computation of the analytics that was needed.
I have noticed that all the API requests are based on the date. So i decided to pre-compute all the analytical data that is needed at ingestion time. I then go with a dict (python version of HashMap) where the key will be the possible date in string format (i.e: 2015, 2015:08 etc). 
The data structure that i went with is as follows:

    {
        'dateString': {
            'count': Number, 
            'queriesCount': {
                'query': Number
            }, 
            'sortedDinstinctQueries': [], 
            'isSortedDistinctQueriesUpToDate': Boolean
        }
    }

##### Structure Description
    - dateString: Any valid date string (2015, 2015-02-02, 2014-09-01 00:00)
    - count: Represent the total number of distinct query during the period *dateString*
    - queriesCount: A Key value pair, count of distinct queries
    - query: unique query.Its value is related to the number of occurences of that query during the period defined by *dateString*
    - sortedDinstinctQueries: A sorted arrays of distinct queries according to their occurences.
    - isSortedDistinctQueriesUpToDate : This is a boolean value that informed if the sortedDinstinctQueries is already computed.
    
The Class that is reponsible of computing the data in the above defined data structure is the  *AnalyticsComputer* [api/main/computer/analytics_computer.py] class.
I decided to consider here in my code each line of query in the log TSV file as a *SearchLogEvent* [api/main/computer/analytics_computer.py]
When the application launch, we have *QueriesLogIngestor* [api/main/loader/queries_log_ingestor.py] class that read the file in a stream like fashion and create when streaming each line a *SearchLogEvent* [api/main/computer/analytics_computer.py].
At each generated *SearchLogEvent*, it is passed to the *AnalyticsComputer*  class `ingestLog` method to ingest the new *SearchLogEvent*. Then this *SearchLogEvent* is then integrated in the previously explained data structure to basically pre-compute
with a date based index the statistical data that will be needed by the API.

At the loading of the log file into the data structure, all the analytical data that will be needed by the API to handle request optimally is pre-computed and ready except one details,
the popular queries count. For the popular queries count, i had tried to pre-compute it at load time but it was very heavy for my computer. The i have decided to implement a dynamic programming based approach using memoization. 
So my approach was then to compute the top popular k queries, at request time and to cache (save) that in my data structure so that for each subsequents requests i won't be computed again.

Overall, i have managed to make retrieving the count of distinct query in constant time (O(1))  and for the popular query request, O(aloga), where a is the number of distinct queries performed during the consider period. O(aloga) is due to the sorting that took place the first time 
the request is performed concerning a give period. After that it turns to a constant time response O(1).

If there are any points that are unclear or if you have any question, don't hesitate !

Thank you !
Elshaddhai
### Time take to create the code
I worked on this Sunday, 25 from 6 pm - 12pm and Monday, 26 from 7pm - 8pm (mostly the documentation and some little re-ajustment)


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Python 3]: <https://www.python.org/>
   [Falcon Framework]: <https://falconframework.org/>
   [Docker]: <https://www.docker.com/>
   [Supervisor]: <http://supervisord.org/>
   [Guinicorn]: <https://gunicorn.org/>
   [the docker official guide]: <https://docs.docker.com/get-docker/>

 
