function abs(n){
	return n > 0 ? n : -n
}

BEGIN{
	FS=",";
	max = 0;
}

$10 != "Unopposed" { 
	if(max < abs($3 - $5)) { max = abs($3 - $5); name = $10;}
} 

END{
	print name;
}
