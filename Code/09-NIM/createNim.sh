#!/bin/bash

ALICEAddr=$1
BOBAddr=$2
DealerAddr=$3
HeapSize=$4
MaxMove=$5

echo 's/ALICE/'${ALICEAddr}'/'     > script.sed
echo 's/BOB/'${BOBAddr}'/'        >> script.sed
echo 's/DEALER/'${DealerAddr}'/'  >>script.sed
echo 's/HHHH/'${HeapSize}'/'      >>script.sed
echo 's/MMMM/'${MaxMove}'/'       >>script.sed

sed -f script.sed nim.templ > nim.teal
