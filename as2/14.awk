BEGIN {
        FS = ",";
}
{
        orgs[$10]++;
	score[$10] += $3;
}
END { 
        max = 0;
        for (var in orgs) {
		average = score[var]/orgs[var];
                if (max < average){
                        result = var;
			max = average;
                }
        }    
        print result,max;
}
