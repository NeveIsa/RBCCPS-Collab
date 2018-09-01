prev_dir=`pwd`
BASEDIR=$(dirname "$0")
tput setaf 1;echo "changing dir to $BASEDIR"
tput sgr0;
cd $BASEDIR

git add .
git commit -m "auto commit by $USER"
git push

tput setaf 1;echo "changing dir to $prev_dir"
cd $prev_dir
tput sgr0;
