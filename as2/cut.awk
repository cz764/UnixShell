BEGIN {
      ORS="";
      OFS="";
}
{
      if(NR%10 != 0) {print $0,","}
      else { print $0,"\n"}
}
