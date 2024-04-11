The FL (G)UI worker get get arbitrarily complex

What is its purpose. It should be the interface/window for the user to figure out what is going on when it comes to FL in oakestra.
E.g. What is currently going on, e.g. image build process, display if and what kind of error occured, etc.
What the current training round and accuracy is, where to find the MLflow link, etc.

One importnat thing to note - initially the idea was to use the init ML service and transform it into a FL learner/client
- the more I think about this the more better ideas I get
- how about replacing (deleting) this init trigger service with a dedicated FL UI service, than spawn as many aggregators and FL clients (were specified in the SLA)
- this is not really necessary for the user to see or tinker with - just one FL UI service should be sufficient

The RFLM should not be this place due to bottleneck, complexity, etc.

The UI can be at first just a viewer (read only) - no push/interact from it to somewhere else

One easy starting point would be to go with a mosquitto MQTT client directly that listens to a general topic regarding FL updates
this can be then further improved by
- only traffic that relates to a single service/app not to all
- write a custom python image for handling this
- allow also message pushes (for what ever reason)
- rewrite to REST ful API + proper seperate GUI (FE app) with buttons, status displays, etc. <- lot of work
- etc ...
