#!/bin/bash
#
#aliases

alias history='history 10'

#if statements

if [ "$HOSTNAME" = "$HOSTNAME" ]; then 
	echo "currently: $HOSTNAME"
fi

#shell functions

show () 
{
	echo "\$0 = $0, \$1 = $1, \$2 = $2"
	echo "$# servers exist and look like $*"

	local count=1;

	while [[ $# -gt 0 ]]; do
		echo "$count: $1..."

		if ping -c 1 -W 2 "$1" > /dev/null 2>&1; then
			echo "$1 is online"
		else
			echo "$1 is offline"
		fi

		count=$((count + 1))
		echo "finished #$count"
		shift
	done
}

