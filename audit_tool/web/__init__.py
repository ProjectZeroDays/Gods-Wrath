from flask import Flask

app = Flask(__name__)

from audit_tool.web import routes
