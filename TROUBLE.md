# TROUBLE

Bumps hit along the way

### Not using Travis before

I've not used Travis CI before, so I had to pick it up along the way. I like how it places the entire build config in
the repository itself; this makes it easy to keep code and CI changes in sync. In addition to general Travis use,
protecting secret values required additional research. The Travis job needed to push a docker image containing the
completed project, and this requires authorization with my Docker Hub account.

### New to DynamoDB

Another new-to-me item! I additionally lacked access to the AWS UI, which made exploring the contents of this
challenge's DynamoDB table more difficult. I ended up using the AWS CLI to test access to and probe the database table.
After I started writing the project's code, it turned out using Boto3 to issue a query was even easier than the CLI!

### How to test CherryPy?

I've written [many python tests](https://git.davepedu.com/dave/pyircbot/src/branch/master/tests) and a handful of
CherryPy-based web applications, but rarely a project with both. The framework `py.test` seems to be the dominant Python
testing framework and I learned that CherryPy
[provides testing fixtures](http://docs.cherrypy.org/en/latest/advanced.html#testing-your-application).
