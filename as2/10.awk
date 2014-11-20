BEGIN {FS=","; max = 0}
{ states[$1]++; }
END {
for (var in states) {
	if (max < states[var]) { name = var; max = states[var]}
}
print name;
}

