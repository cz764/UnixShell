BEGIN {
FS=",";
}
{
orgs[$10]++;
}
END{
for (var in orgs)
	print var, orgs[var];
}
