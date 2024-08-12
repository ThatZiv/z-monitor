from flask import Flask, render_template, request, url_for, redirect
from flask_basicauth import BasicAuth
from Store import Store
from Config import config
import time
import os
import gui
import Pc

class Auth(BasicAuth):
    def __init__(self, app: Flask, store: Store = Store()):
        super().__init__(app)
        self.store = store

    def check_credentials(self, username, password):
        return username == "admin" and self.store.verify_password(password)

class Webserver:
    def __init__(self, store: Store):
        self.store = store
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.basic_auth = Auth(self.app, store)
        self.pc = Pc.Info()
        self.static_info = self.pc.get_info()

        @self.app.route('/')
        @self.basic_auth.required
        def home():
            return render_template("index.html",
                title=config["appName"],
                cfg=config,
                static_info=self.static_info,
            )

        @self.app.route('/logs')
        @self.basic_auth.required
        def logs():
            limit = int(request.args.get("limit") or 100)
            page = int(request.args.get("page") or 0)
            # type = request.args.get("type")
            types = list(set(request.args.getlist("type")))

            logs = self.store.get_logs(page, limit, type=types)
            return render_template("logs.html",
                pages=logs['count']//limit,
                logs=[(*log[:2],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(log[2])), *log[3:]) for log in logs['content']],
                page_num=page,
                limit=limit,
                type=''.join([f"&type={type}" for type in types])
            )

        @self.app.route('/alert', methods=["POST"])
        @self.basic_auth.required
        def alert():
            text = request.form.get("alert")
            if not text:
                return "No alert text provided"
            self.store.log(f"Alert sent from web UI: {text}", type="ui")
            gui.alert(text)
            return "Alert sent"

        @self.app.route('/pc/sysinfo', methods=["GET"])
        @self.basic_auth.required
        def sysinfo():
            # if query params type = json, return json
            if request.args.get("type") == "json":
                return self.pc.get_system_info()
            return render_template("sysinfo.html", **self.pc.get_system_info())

        @self.app.route("/timeleft", methods=["GET"])
        @self.basic_auth.required
        def timeleft():
            return render_template("timeleft.html",
                time_used=self.store.get_time_used(),
                time_limit=self.store.get_time_limit()
            )

    def run(self):
        self.app.run(
            debug=config["env"]=="dev",
            use_reloader=False,
            host="0.0.0.0",
            port=config["webserverPort"]
        )

if __name__ == '__main__':
    store = Store()
    webserver = Webserver(store)
    webserver.run()
