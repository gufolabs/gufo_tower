stage 'Build'
node {
   stage 'Clone'
   checkout scm
   stage 'Stage 0 clean up'
   sh 'rm -r dist/* build/*'
   sh 'python setup.py clean'
   stage 'Stage 1 test pep8'
   sh 'pep8 --ignore=E265,E266,E501,E402 .'
   stage 'Stage 2 build bztar'
   sh 'python setup.py sdist --format=bztar'
   stage 'Stage 99 artifact'
   sshagent(['ci-cdn-nocproject-org']) {
     sh '''export VERSION=$(basename dist/*.tar.bz2)
     echo "put dist/${VERSION} tower/${VERSION}" | sftp -P 2228 ci@cdn.nocproject.org
     echo "put dist/${VERSION} tower/noc-tower-latest.tar.bz2" | sftp -P 2228 ci@cdn.nocproject.org'''
   }
}
