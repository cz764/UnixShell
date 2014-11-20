BEGIN{
        FS=",";
}
{
        organization[$10]++;
        score[$10]+=$3;
}
END{
        tmp=0;
        for(i in organization){
                aver = score[i]/organization[i];
                if(aver>tmp){
                        result = i;
                        tmp=aver;
                }
        }
        print result, tmp;
}

