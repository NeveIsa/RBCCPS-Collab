#!/bin/sh
id=$1
itemfile=$2

echo $itemfile

#sed -e "s/idXYZ/$1/g" $2 >> tmp.txt

rm -f tmp_noapi.sh
#sed -e "/\"item-metadata\": \[/ r $itemfile" cmd.txt >> tmp.sh
sed -e "/data / r $itemfile" cmd.txt >> tmp_noapi.sh
sed -i -e "s/idXYZ/$1/g" tmp_noapi.sh 
chmod +x tmp_noapi.sh
#rm -f tmp.txt
#rm -f tmp.sh
