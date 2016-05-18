stage 'Build'
node {
   stage 'Clone'
   checkout scm
   stage 'Stage 1 build bztar'
   sh 'python setup.py sdist --format=bztar'
   stage 'Upload artifact'
   sh 'scp -o StrictHostKeyChecking=no -P 2228 dist/*.tar.bz2 ci@cdn.nocproject.org:/www/cdn/tower/'
}
