BEGIN {
FS = ",";
}
{
states[$1]++;
}
END {
for (var in states) {
	count++;
}
print NR/count;
}
