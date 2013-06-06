#!/usr/bin/perl

print "Content-type: image/png\n\n";

@vars = split(/&/, $ENV{'QUERY_STRING'});

for $v (@vars) {
	($key, $val) = split(/=/, $v, 2);
	$val =~ s/%20/ /g;

	$val =~ s/[^A-Za-z0-9._: -]//g;

	$var{$key} = $val;
}

chdir("/root") || die "chdir";

$tile = "$var{'opt'} shapes/$var{'map'} $var{'z'} $var{'x'} $var{'y'}";

$tilef = $tile;
$tilef =~ s/\//@/g;

mkdir "cache/$var{'z'}";
mkdir "cache/$var{'z'}/$var{'x'}";
mkdir "cache/$var{'z'}/$var{'x'}/$var{'y'}";

$tilef = "$var{'z'}/$var{'x'}/$var{'y'}/$tilef";

if (-f "cache/$tilef") {
	open(IN, "cache/$tilef");
	while (<IN>) {
 		print;
	}
	close(IN);
} else {
	print STDERR "/root/datamaps/render $tile | pngquant 128\n";

	open(IN, "/root/datamaps/render $tile | pngquant 128 |");
	open(OUT, ">cache/$$");
	while (<IN>) {
		print OUT;
		print;
	}
	close(OUT);
	close(IN);
	rename("cache/$$", "cache/$tilef");
}
exit 0;
