# Log Insight Map Reduce
An implemenation of map reduce for extracting data from the log files of an application.
This map reduce code is designed to be run on a hadoop cluster or a single machine line via the .sh scripts.

The map reduce steps are done in python and they product data into tidy data from the unstructured log data.  Since the log this works on is proprietary, it will not be named.  This code however, 
can be used to learn from and serve as a model for other projects.  The key to its use on a particulare data set are the string splits and regex.


