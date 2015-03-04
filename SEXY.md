OS / Hosting  -> Ubintu 11.04 (“Natty Narwhal”) on Amazon EC2
Load Balancing -> we used to run 2 nginx machines and DNS Round-Robin between them. 
We also terminate our SSL at the ELB level, which lessens the CPU load on nginx. We use Amazon’s Route53 for DNS, which they’ve recently added a pretty good GUI tool for in the AWS console.
use gunicorn as our WSGI server 
To run commands on many instances at once (like deploying code), we use Fabric, which recently added a useful parallel mode so that deploys take a matter of seconds.
what is EBS 
What is sharding 
what are master-replicas
Apache Solr
we use Memcached for caching, and currently have 6 Memcached instances

When a user decides to share out an Instagram photo to Twitter or Facebook, or when we need to notify one of our Real-time subscribers of a new photo posted, we push that task into Gearman, a task queue system originally written at Danga

For Push notification https://github.com/samuraisam/pyapns -> open-source Twisted service that has handled over a billion push notifications for us, and has been rock-solid.


  
