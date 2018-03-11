#!/bin/bash
bin_program="test_ddns_updater"

strip_comments () {
	eval file=$1
	sed 's/a/aA/g;s/__/aB/g;s/#/aC/g' "$file" |
		  gcc -P -E $arg - |
		  sed 's/aC/#/g;s/aB/__/g;s/aA/a/g'
}

[ $# -eq 1 ] && python_file="$1" || { echo "$0 [python file]"; exit 1; }

rm -rf *.c $bin_program

#sometimes obfuscating breaks c so we repeat until it works here.
pass=0
while [ $pass -eq 0 ]
do
	echo "obfuscate program..."
	pyminifier --obfuscate $python_file > ${python_file}".obs" || { echo "obfuscating failed!!!"; exit 2; }

	echo "generating c program..."
	cython --embed -o "tmp1.c" ${python_file}".obs"  && pass=1 || { rm -rf "tmp1.c"; echo "cython conversion failed!!!. trying again..."; }
done

echo "striping comments..."
strip_comments "tmp1.c" > "tmp2.c" || { echo "stripping comments from c program failed!!!"; exit 4; }

echo "compiling to binary..."
gcc $CFLAGS -I/usr/include/python2.7 -o $bin_program "tmp2.c" -lpython2.7 -lpthread -lm -lutil -ldl || \
{ echo "compiling to binary failed!!!"; exit 5; }

echo "striping symbols from binary ..."
strip -s $bin_program  

rm -rf *.c *.obs
echo "done"
exit 0
