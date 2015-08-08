from flask import Flask, request, Response
import subprocess
import os

from local_settings import TOKENS

application = Flask(__name__)


@application.route('/deploy/', methods=['POST'])
def deploy():
    token = request.json.get('token')
    site = request.json.get('site')
    ref = request.json.get('ref')

    if site in TOKENS and TOKENS[site] == token:
        try:
            # critical that site is checked to be a key in tokens!
            deploy_script = os.path.join('deploy', site)
            subprocess.check_call([deploy_script, ref])
        except Exception:
            return Response('Deployement failed', 500, )

        return Response('Successfully deployed', 200, )
    else:
        return Response('Incorrect token', 401, )


if __name__ == "__main__":
    application.run()
