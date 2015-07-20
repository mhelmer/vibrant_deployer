from flask import Flask, request, Response
import subprocess

from local_settings import SECRET_KEY, DEPLOY_TREE, VENV

application = Flask(__name__)


@application.route('/deploy/', methods=['POST'])
def deploy():
    key = request.json.get('key')
    ref = request.json.get('ref')

    if SECRET_KEY == key:
        try:
            subprocess.check_call(['./deploy',
                                   ref, DEPLOY_TREE, VENV])
        except Exception:
            return Response('Deployement failed', 500, )

        return Response('Successfully deployed', 200, )
    else:
        return Response('Incorrect token', 401, )


if __name__ == "__main__":
    application.run()
