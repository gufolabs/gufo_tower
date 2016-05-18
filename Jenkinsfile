stage 'Build'
node {
   Stage 'Clone'
   hg clone https://bitbucket.org/nocproject/noc-tower
   stage 'Stage 1 build bztar'
   sh "./contrib/scripts/build.sh"
}