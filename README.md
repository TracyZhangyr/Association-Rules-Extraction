# COMS6111 Project 3

#### a. Team Members:

Yuerong Zhang (UNI: yz4143), 
Ruixuan Fu (UNI: rf2762) 



#### b. List of Files:

1. proj3

   1. main.py
   2. spacy_help_functions.py

2. README.md

3. transcript.txt

   


#### c. Commands:

1. Install dependencies:


 Environment:

```shell
python: 3.9
```

 Installations:

```shell
pip3 install requests
```


2. Run program:

Command to run main.py:

```shell
python3 main.py <target dataset> <min_sup> <min_conf>
```

Examples:

```shell
python3 main.py INTEGRATED-DATASET.csv 0.2 0.5
```



#### d. Dataset Description
1. Which dataset:
   
   We used the 'NYPD Motor Vehicle Collisions Summary' dataset, which describes details of motor vehicle collisions in New York City provided by the Police Department (NYPD). (data resource link: https://data.cityofnewyork.us/NYC-BigApps/NYPD-Motor-Vehicle-Collisions-Summary/m666-sf2m)

2. What procedure and why this dataset is interesting:
   1. Filter recent year data: 
   
      Firstly, to conduct recent collision analysis, we excluded the data before 2022 year, which remains 252,362 "market baskets". 

   2. Delete some geographical attributes: 
   
      To make our association rules extraction keep focusing on essential parts about the collisions, we deleted the "lattitude, longitude" attrubutes of the collision data (because we are not good at geography lol) while keep "borough, on street name" as the core location information of collisions. We want to discover the associations about location and other elements. 
   
   3. Divide precise date/time information into natural dimensions: 
   
      Besides, we also want to know whether there will be a frequent collision "time" (like midnight?) or "season" (like winter which has snowstorm?). 
      
      So we divided the precise crush time (hour:minute) into "dawn"(3-6 am), "morning"(7-10 am), "noon"(11am-2pm), "afternoon"(3-6 pm), "night"(7-10 pm), "midnight"(11pm-2am). And divided the the precise crush date (mm/dd/yy) into four seasons. 
   
      In this way, we can use this dataset to figure out whether there will be some relations between time period, season and collisions, so that it may be beneficial for drivers and residents to avoid dangerous time.
   
   4. Combine person status: 
   
      We combined the original person safe status, which was divided according to the person role (pedestrain or cyclist or motorist), into three status types: there are people "injured", "killed" or everyone "safe".
   
   5. Combine vehicle type: 
   
      The original vehicle attribute's possible data input are too various. For example, it will show the exact type of truck, such as "Tractor Truck Diesel", "Box Truck", "Pick-up Truck" etc. To make it consistent with other types of vehicles like sedan or suv, we combined these truck type vehicles into "truck". 
      
         So we can better figure out potential rules of different vehicle types with collisions.
      
      

#### e. Project Description

1. Internal design:

   1. General structure:
      1. Receive and check user's input: google client key and engine key, r (relation to extract), t (extraction confidence threshold), q (seed query), k (the number of tuples required in the output).

      2. Initialize X, the dictonary of extracted tuples, which is {tuple: confidence}.

      3. Begin the main loop, for each iteration:
         1. Obtain the URLs for the top-10 results for the query from Google

         2. For each URL (not been processed before), do the followings:

            1. Retrieve the corresponding webpage (Skip it if cannot retrieve due to timeout, etc.). Extract the actual plain text from the webpage using BeautifulSoup.

            2. Truncate the resulting plain text to its first 20,000 characters if longer than these.

            3. Use spaCy to split the text into sentences.

            4. Extract named entities (e.g., PERSON, ORGANIZATION). Use the sentences and named entity pairs as input to SpanBERT to predict the corresponding relations, and extract all instances of the relation specified by r. Identify the tuples that have an associated extraction confidence >= t and add them to X. Remove exact duplicated from X: if X contains tuples that are identical to each other, keep only the copy that has the highest extraction confidence. 

         3. Print all of the tuples in X sorted in decreasing extraction confidence order and with them for this iteration.

         4. If X contains >= k tuples, then stop.

         5. Otherwise, select from X a tuple y such that (1) y has not been used for querying yet and (2) y has the highest extraction confidence among the tuples in X that have not yet been used for querying. Create a query q from tuple y by just concatenating the attribute values together, and go to the next iteration. If no such y tuple exists, then stop, as ISE has stalled before retrieving k tuples with the specified confidence threshold t.


   2. Main components:

      1. callGoogleAPI(): Through calling the google search API, fetch the top 10 search results according to user's query input.

      1. get_plain_text_from_url(): Retrieve the webpage (Skip it if cannot retrieve due to timeout, etc.). Then, extract the actual plain text from the webpage using BeautifulSoup.

      1. extract_relations(): Extract named entities (e.g., PERSON, ORGANIZATION). Use the sentences and named entity pairs as input to SpanBERT to predict the corresponding relations, and extract all instances of the relation specified by r. Identify the tuples that have an associated extraction confidence >= t and add them to X. Remove exact duplicated from X: if X contains tuples that are identical to each other, keep only the copy that has the highest extraction confidence. 

      1. main(): The main loop to do the iterative set expansion algorithm. 

         

2. External libraries:

   1. googleapiclient: Call Google Custom Search Engine API to get top-10 search results for the query.

   2. BeautifulSoup: Extract the actual plain text from a given webpage, and ignore HTML tags and other content that would interfere with the information extraction process.
   
   3. requests: Send HTTP requests to get content of the webpage by specified URL.
   
   4. spaCy: Process and annotate text through linguistic analysis. 
   
   5. SpanBERT: Extract the relations from text documents.
   
      

#### f. Command Line Specification of A Compelling Sample Run

```shell
engine_ID = de217206a85e0b817
API_Key = AIzaSyD0FBYWKa1fBB2nYsg6RvP9DfvOLCpd_TI
```



#### g. Additional Information

1. We modified the original spacy_help_functions.py in SpanBERT to suit our ISE algorithm. (Changes are mentioned in the above setion e: Step 3 Methodology).

2. Reference for using BeautifulSoup to extract plain text:

   https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text/24968429#24968429

   

   

   

