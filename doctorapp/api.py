import cherrypy
from doctorapp import project_url, image_url


class ApiV1(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def health(self):
        return {"status": "healthy",
                "container": image_url,
                "project": project_url}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def secret(self):
        try:
            secret = cherrypy.engine.publish("get:secret").pop()
        except IndexError:
            raise cherrypy.HTTPError(503, "Unavailable")
        return {"secret_code": secret}
