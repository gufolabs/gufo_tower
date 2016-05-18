stage 'Build'
node {
   stage 'Clone'
   checkout scm
   stage 'Stage 1 build bztar'
   sh 'python setup.py sdist --format=bztar'
}