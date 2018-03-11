# SUMMARY

The development process

This was my general order of operations while developing this project:


## Gather information, test credentials

I first looked over the [challenge repo](https://github.com/Twistbioscience/devops-challenge), making mental notes of
the requirements, challenges, and suggestions. I also used the AWS CLI to test what access the credentials I was
provided with have and to run some simple queries I thought might model later behavior.


## Language and module selection

Python is appropriate for general purpose http apis, making it an excellent language to implement the coding portion of
this challenge in.

Since we're creating an http api, selecting a web framework is a sensible next step. I'm a huge fan of
[CherryPy](http://cherrypy.org) and have had success building web application with it in the past, so it seemed a
natural choice.

Likewise, since we'll need to interact with AWS's api, Boto3 was also selected for this purpose.


## Development

I see this application as 3 components: an api, a data source, and glue logic around it. This made it easy to break into
a couple smaller segments for development:


### The api

The api needed to serve 2 endpoints, one of which served static json. In CherryPy, this means creating one class with
two methods, both named to match the endpoint they implement.

For the endpoint returning data from DynamoDB, I used CherryPy's
[publish/subscribe](http://docs.cherrypy.org/en/latest/extend.html#publish-subscribe-pattern) bus to couple with other
portions of the app. To clarify, this means that when a request comes into the application, it (effectively) publishes
an event on an event bus and waits for a response. Elsewhere in the application, other code listening for this kind of
event is triggered, returning a response to the original request handler. Lastly, it's encoded in JSON and emitted. This
design pattern, generally speaking, promotes code simplicity.


### The data source

This application's database needs are rather simple - fetching a known static value - and as a result the data source
layer did not need to be complex. It only needed to be a single importable method that, when called, fetches the secret
value from DynamoDB and returns it. This also is an excellent location to implement caching - the secret value is static
by design, which means we need not fetch it more than once.

The cache on this layer was implemented using python's builtin `lru_cache`.


### The glue logic

Having the major components, next came some "glue code" to make our app run:

- An argparser to intake settings
- A signal listener to trigger graceful shutdowns
- Logging settings
- Passing configuration items around
- Registering the data source function on the bus


### Testing

As these components were finished, test were created for them as well.


## Automated CI & Building

The requirements want the application deployable via Docker, so creating a Dockerfile became the next step. For a base
image, the Python org's published "light" images were an easy choice; they contain the python interpretor and related
tools within a reasonably small image size. If I were to, for example, use a ubuntu image and install python + tools
myself, it would have resulted in a larger image. Dockerizing this app was as simple as running the setuptool's setup.py
installer under the docker image build process.

Finally, all of this needed to be built by Travis CI. The .travis.yml was added and configures an environment where both
python3.6 and docker was available. The coded is tested, linted, built into an image, and shipped off to the Docker Hub.


## AWS Cloudformation

To be quite honest, this was the most interesting portion of this exercise! I do like container technology but I'll
admit to never having previously using AWS ECS. So, already knowing other parts of AWS, it was interesting to see both
how it was implemented on AWS's side, and the user - my - side.

My template is largely based on
[an example](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ecs.html) provided in the AWS docs.
This starting point had almost everything I needed; I ended up modifying what specific containers it launches and some
params passed to them, as well as granting the ECS instances access to DynamoDB via their instance profile.

My earlier use of Boto3 made using this new authorization strategy completely seamless. In the python code, we pass
absolutely nothing when initializing a Boto session. Because of this, Boto searches for credentials available to it -
environment vars, ~/.aws, and ec2 metadata are all checked.
