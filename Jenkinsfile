stage 'Build'
node {
    stage 'Clone'
    checkout scm
}
parallel 'Binaries': {
    node {
        sh 'cd contrib/test-image'
        def timage = docker.image('test-image:1')
        timage.inside {
            sh 'pep8 --ignore=E265,E266,E501 .'
            sh 'python setup.py sdist --format=bztar'
        }
    }
    node {
        docker.build 'noc-tower:1'
    }
}
stage 'Stage 99 artifact'
node {
     sshagent(['ci-cdn-nocproject-org']) {
        sh '''export VERSION=$(basename dist/*.tar.bz2)
        echo "put dist/${VERSION} tower/noc-tower-latest.tar.bz2" | sftp -P 2228 ci@cdn.nocproject.org'''
    }
}