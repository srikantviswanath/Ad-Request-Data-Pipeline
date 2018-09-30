## Ad Request Data Augmentation Pipeline

### Overview
This is a service to take in an incoming ad request from advertiser and pass it thru an data 
augmentation pipeline that augments several contextual information in the following order dictated
by the INDIVIDUAL_PROCESSING_UNITS pipeline:

* fetch country of ad request origin
* inject the demographics of the advertising site
* lookup the publisher site's details

Timed Caching for 24 hours has been enabled for each of the above individual data augmentations
as neither of them is volatile 

#### Running the service

To run the service, simple run the module 
```python
request_augment_service.py
```




