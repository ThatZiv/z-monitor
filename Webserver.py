from flask import Flask, render_template, request, url_for, redirect
from flask_basicauth import BasicAuth
from Store import Store
from Config import config
import os

import gui

class Auth(BasicAuth):
    def __init__(self, app: Flask, store: Store):
        super().__init__(app)
        self.store = store

    def check_credentials(self, username, password):
        return username == "admin" and self.store.verify_password(password)

class Webserver:
    def __init__(self, store: Store):
        self.app = Flask(__name__)
        self.basic_auth = Auth(self.app, store)
        self.store = store

        @self.app.route('/')
        @self.basic_auth.required
        def home():
            return render_template("index.html",
                title=config["appName"],
                time_used=self.store.get_time_used(),
                cfg=config,
                alert=request.args.get("alert")
            )

        @self.app.route('/logs')
        @self.basic_auth.required
        def logs():
            return self.store.get_logs()

        @self.app.route('/alert', methods=["POST"])
        @self.basic_auth.required
        def alert():
            text = request.form.get("alert")
            if not text:
                return redirect(url_for("home", alert="No alert text provided"))
            self.store.log(f"Alert sent from web UI: {text}")
            gui.alert(text)
            # no redirect
            return redirect(url_for("home", alert="Alert sent"))

    def run(self):
        self.app.run(debug=config["env"]=="dev", use_reloader=False, host="0.0.0.0")

if __name__ == '__main__':
    store = Store()
    webserver = Webserver(store)
    webserver.run()
