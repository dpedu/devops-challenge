import sys
import cherrypy
import signal
import logging
import argparse
import os
from doctorapp.api import ApiV1
from doctorapp.datasource import get_secret


def get_args(args):
    """
    Parse and return command line args.
    :return: #TODO what type is it
    """
    parser = argparse.ArgumentParser(description="doctorapp http server daemon")
    parser.add_argument("-l", "--listen", help="listen address",
                        default=os.environ.get("DOCTORAPP_LISTEN", "0.0.0.0"))
    parser.add_argument("-p", "--port", type=int, help="tcp port to listen on",
                        default=int(os.environ.get("DOCTORAPP_PORT", 5000)))
    parser.add_argument("--debug", action="store_true", help="enable development options",
                        default=True if os.environ.get("DOCTORAPP_DEBUG") else False)
    return parser.parse_args(args)


def main():
    """
    Main entrypoint for the application. Parse args, couple the api and data source, set up signal handlers, and run the
    app.
    """
    args = get_args(sys.argv[1:])

    # Configure logging
    logging.basicConfig(format="%(asctime)-15s %(levelname)-8s %(filename)s:%(lineno)d %(message)s",
                        level=logging.INFO if args.debug else logging.WARNING)

    logging.info(args)

    # Configure cherrypy webserver
    cherrypy.config.update({
        "tools.sessions.on": False,
        "tools.sessions.locking": "explicit",
        "request.show_tracebacks": args.debug,
        "server.socket_port": args.port,
        "server.socket_timeout": 5,
        "server.socket_host": args.listen,
        "server.thread_pool": 10,
        "server.show_tracebacks": True,
        "log.screen": False,
        "engine.autoreload.on": args.debug})

    # Create instance of the API and mount it on the "/" path. More complex apps may specify endpoint-specific options
    # in mount()'s 3rd argument, such as changing routing rules by using cherrypy.dispatch.MethodDispatcher, etc
    api = ApiV1()
    cherrypy.tree.mount(api, "/", {"/": {}})
    # Register the secret-fetching method to the secret-requesting bus channel
    cherrypy.engine.subscribe("get:secret", get_secret)

    # Gracefully shut down the application on SIGINT or SIGTERM
    def signal_handler(signum, stack):
        logging.critical("Got sig {}, exiting...".format(signum))
        cherrypy.engine.exit()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        cherrypy.engine.start()  # Run it
        cherrypy.engine.block()
    finally:
        logging.info("API has shut down")
        cherrypy.engine.exit()


if __name__ == "__main__":
    main()
