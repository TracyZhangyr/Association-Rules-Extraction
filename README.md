# COMS6111 Project 3

#### a. Team Members:

Yuerong Zhang (UNI: yz4143), 
Ruixuan Fu (UNI: rf2762) 



#### b. List of Files:

1. proj3

   1. main.py
   
2. INTEGRATED-DATASET.csv

2. README.md

3. example-run.txt

   


#### c. Commands:

1. Environment:

```shell
python: 3.9
```


2. Run program:

Command to run main.py:

```shell
python3 main.py <target dataset> <min_sup> <min_conf>
```

Examples:

```shell
 python3 main.py INTEGRATED-DATASET.csv 0.01 0.7
```



#### d. Dataset Description
1. Which dataset:
   
   We used the 'NYPD Motor Vehicle Collisions Summary' dataset, which describes details of motor vehicle collisions in New York City provided by the Police Department (NYPD). (data resource link: https://data.cityofnewyork.us/NYC-BigApps/NYPD-Motor-Vehicle-Collisions-Summary/m666-sf2m)

2. What procedure and why this dataset is interesting:
   1. Filter recent year data: 
   
      Firstly, to conduct recent collision analysis, we excluded the data before 2022 year, which remains 28950 "market baskets". 

   2. Delete some geographical attributes: 
   
      To make our association rules extraction keep focusing on essential parts about the collisions, we deleted the "lattitude, longitude" attrubutes of the collision data (because we are not good at geography lol) while keep "borough, on street name" as the core location information of collisions. We want to discover the associations about location and other elements. 
   
   3. Divide precise date/time information into natural dimensions: 
   
      Besides, we also want to know whether there will be a frequent collision "time" (like midnight?) or "season" (like winter which has snowstorm?). 
      
      So we divided the precise crush time (hour:minute) into "dawn"(3-6 am), "morning"(7-10 am), "noon"(11am-2pm), "afternoon"(3-6 pm), "night"(7-10 pm), "midnight"(11pm-2am). And divided the the precise crush date (mm/dd/yy) into four seasons. 
   
      In this way, we can use this dataset to figure out whether there will be some relations between time period, season and collisions, so that it may be beneficial for drivers and residents to avoid dangerous time.
   
   4. Merge person safe status: 
   
      We combined the original person safe status, which was divided according to the person role (pedestrain or cyclist or motorist), into three status types: there are people "injured", "killed" or everyone "safe". So that if there exists associations between other elements with the collision's overall safe status, it will be more obvious
   
   5. Clean vehicle type: 
   
      The original vehicle attribute's possible data input are too various. For example, it will show the exact type of truck, such as "Tractor Truck Diesel", "Box Truck", "Pick-up Truck" etc. To make it consistent with other types of vehicles like sedan or suv, we combined these truck type vehicles into "truck". 
      
         So we can better figure out potential rules of different vehicle types with collisions.
      
      

#### e. Project Description

1. Internal design:
   
   We used the a-prior algorithm to construct our program. There are maily three functions in our program. The first function 'load_csv(dataset_name)' can load the dataset that the user inputed as the first argument, then return as 'data'. The second function 'get_frequency_set(data, min_sup)' was to generate the frequency itemsets based on a-prior's idea. It received data and the inputed minimal support value, found all frequency itemsets that have supp higher than min_supp, by iteratively generating frequency itemsets and finding candidate itemsets level by level, until there are no more freqency itemsets can be found. Then based on the freqency itemsets with their corresponding supp values, the third funtion get_association_rules(L_frequent_item, support_data, min_supp, min_conf) found association rules according to the formula that rule(A=>B)_confidence_value = (A,B)support_value / (A)support_value. 
   
   

#### f. Command Line Specification of A Compelling Sample Run

```shell
 python3 main.py INTEGRATED-DATASET.csv 0.01 0.7
```

Specification:

   By using this combination, we can figure out some interesting and revealing results about different situation’s safety. For example, we can find that the collisions involved bike are more possible to have people injured (['bike'] => ['injured'] (Conf: 79%, Supp: 2%)), while suv, bus, trucks or other ‘stronger’ vehicles are more likely to keep safe. Besides, we can also find various borough’s safer time period, which may have interesting differences. Such as the queens with dawn is more possible to be in association with safe (['queens', 'dawn'] => ['safe'] (Conf: 79%, Supp: 1%), while for Brooklyn is dawn and noon (['brooklyn', 'dawn'] => ['safe'] (Conf: 72%, Supp: 1%), [‘brooklyn', 'noon'] => ['safe'] (Conf: 71%, Supp: 3%)) and for Manhattan is midnight and morning (['manhattan', 'midnight'] => ['safe'] (Conf: 73%, Supp: 1%), ['manhattan', 'morning'] => ['safe'] (Conf: 73%, Supp: 1%)). There are some other associations between season, vehicle, period combinations we can also find from this combination.
The association rules results mainly contain safe consequence. We speculate that it may be because there are fewer vehicles on the road during these periods, so even if there is a collision, the number of casualties is low.


#### g. Additional Information

1. Reference for A-Priori Algorithm:

   Rakesh Agrawal and Ramakrishnan Srikant: [Fast Algorithms for Mining Association Rules in Large Databases](http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf), VLDB 1994

   

   

   

