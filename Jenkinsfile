stage 'Build'
node {
   stage 'Clone'
   checkout scm
   stage 'Stage 1 build bztar'
   sh 'python setup.py sdist --format=bztar'
   stage 'Upload artifact'
   sshagent(['ci-cdn-nocproject-org']) {
     sh '''export VERSION=$(basename dist/*.tar.bz2)
     echo "put dist/${VERSION} tower/${VERSION}" | sftp -P 2228 ci@cdn.nocproject.org
     echo "put dist/${VERSION} tower/noc-tower-latest.tar.bz2" | sftp -P 2228 ci@cdn.nocproject.org'''
   }
}
