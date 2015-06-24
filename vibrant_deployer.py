from flask import Flask, request, Response
import subprocess

from local_settings import SECRET_TOKEN, DEPLOY_TREE, DJANGO_VENV

application = Flask(__name__)


@application.route('/deploy/', methods=['POST'])
def deploy():
    token = request.json.get('token')
    ref = request.json.get('ref')

    if SECRET_TOKEN == token:
        try:
            subprocess.check_call(['./deploy',
                                   ref, DEPLOY_TREE, DJANGO_VENV])
        except Exception:
            return Response('Deployement failed', 500, )

        return Response('Successfully deployed', 200, )
    else:
        return Response('Incorrect token', 401, )


if __name__ == "__main__":
    application.run()
