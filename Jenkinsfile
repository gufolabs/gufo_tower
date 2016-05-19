stage 'Build'
node {
   stage 'Clone'
   checkout scm
   stage 'Stage 1 build bztar'
   sh 'python setup.py sdist --format=bztar'
   stage 'Upload artifact'
   sshagent(['ci-cdn-nocproject-org']) {
     sh '''export VERSION=$(basename dist/*.tar.bz2)
     scp -o StrictHostKeyChecking=no -P 2228 dist/${VERSION} ci@cdn.nocproject.org:/www/cdn/tower/
     ssh -o StrictHostKeyChecking=no -p 2228 ci@cdn.nocproject.org /www/cdn/tower/make-latest ${VERSION}'''
   }
}
