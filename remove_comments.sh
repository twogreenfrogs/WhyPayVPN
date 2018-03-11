file_exists() {
        if [ "$#" = 1 ] && [ ! -f "$1" ]; then
                print "$1 does not exist"
                exit 1
        fi
}

strip_comments() {
	# Strip C comments
	# by Stewart Ravenhall <stewart.ravenhall@ukonline.co.uk> -- 4 October 2000
	# Un-Korn-ized by Paolo Bonzini <bonzini@gnu.org> -- 24 November 2000

	# Strip everything between /* and */ inclusive

	# Copes with multi-line comments,
	# disassociated end comment symbols,
	# disassociated start comment symbols,
	# multiple comments per line

	# Create shell variables for ASCII 1 (control-a)
	# and ASCII 2 (control-b)
	a="`echo | tr '\012' '\001'`"
	b="`echo | tr '\012' '\002'`"

	sed '
		# If no start comment then go to end of script
		/\/\*/!b
		:a
		s:/\*:'"$a"':g
		s:\*/:'"$b"':g
		# If no end comment
	    /'"$b"'/!{
		:b
			# If not last line then read in next one
			$!{
				N
				ba
			}
			# If last line then remove from start
			# comment to end of line
			# then go to end of script
			s:'"$a[^$b]"'*$::
			bc
		}
		
		# Remove comments
		'"s:$a[^$b]*$b"'::g
	    /'"$a"'/ bb
		
		:c
		s:'"$a"':/*:g
		s:'"$b"':*/:g
	' $1
}

file_exists $1
