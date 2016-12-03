$measure=$ARGV[0];
$word1=$ARGV[1];
$word2=$ARGV[2];

sub wnsimilarityscore{
	my $m = shift;
	my $w1 = shift;
	my $w2 = shift;
	
	use WordNet::QueryData;
	my $wn = WordNet::QueryData->new();
	my $object;
	my $value;
	
	if($m eq "path"){use WordNet::Similarity::path; $object = WordNet::Similarity::path->new($wn);}
	elsif($measure eq "lch"){use WordNet::Similarity::lch; $object = WordNet::Similarity::lch->new($wn);}
	elsif($measure eq "lesk"){use WordNet::Similarity::lesk; $object = WordNet::Similarity::lesk->new($wn);}
	elsif($measure eq "wup"){use WordNet::Similarity::wup; $object = WordNet::Similarity::wup->new($wn);}
	elsif($measure eq "res"){use WordNet::Similarity::res; $object = WordNet::Similarity::res->new($wn);}
	elsif($measure eq "lin"){use WordNet::Similarity::lin; $object = WordNet::Similarity::lin->new($wn);}
	elsif($measure eq "jcn"){use WordNet::Similarity::jcn; $object = WordNet::Similarity::jcn->new($wn);}
	elsif($measure eq "hso"){use WordNet::Similarity::hso; $object = WordNet::Similarity::hso->new($wn);}
	
	$value = $object->getRelatedness($w1, $w2);
	($error, $errorString) = $object->getError();
	#die "$errorString\n" if($error);
	print "0\n" if ($error);
	
	#my $filename = 'C:\Users\Hariprabha\Desktop\NLPProject\extra.txt';
	#open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
	#print $fh "$value\n";
	#close $fh;

	print "$value\n";
}

wnsimilarityscore($measure, $word1, $word2);

