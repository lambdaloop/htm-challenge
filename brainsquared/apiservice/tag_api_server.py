"""
Endpoint to send tags to rabbitMQ
"""
import json

from flask import Flask, request

from brainsquared.publishers.PikaPublisher import PikaPublisher

_RMQ_ADDRESS = "rabbitmq.cloudbrain.rocks"
_RMQ_USER = "cloudbrain"
_RMQ_PWD = "cloudbrain"
_WEBSERVER_PORT = 8080
_API_VERSION = "v0.1"

modules = {}

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

tag_publisher = PikaPublisher(_RMQ_ADDRESS, _RMQ_USER, _RMQ_PWD)
tag_publisher.connect()
tag_publisher.register("brainsquared:module0:tag")


@app.route('/api/%s/users/<string:user_id>/modules/<string:module_id>/tag' %
           _API_VERSION, methods=['POST'])
def create_tag(user_id, module_id):
  """Create new module tag"""
  timestamp = request.json["timestamp"]
  value = request.json['value']
  data = {"timestamp": timestamp, "value": value}
  
  routing_key = "%s:%s:%s" % (user_id, module_id, "tag")
  
  tag_publisher.publish(routing_key, data)
  return json.dumps("Tag published: %s" % data), 200

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=_WEBSERVER_PORT)
