stage 'Build'
node {
   stage 'Clone'
   checkout scm
   stage 'Stage 1 build bztar'
   sh 'python setup.py sdist --format=bztar'
   stage 'Upload artifact'
   sshagent(['ci-cdn-nocproject-org']) {
     sh 'echo SSH_AUTH_SOCK=$SSH_AUTH_SOCK'
     sh 'ls -al $SSH_AUTH_SOCK || true'
     sh 'scp -vvv -o StrictHostKeyChecking=no -P 2228 dist/*.tar.bz2 ci@cdn.nocproject.org:/www/cdn/tower/'
   }

}
