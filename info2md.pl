#!/usr/bin/env perl

print `date`;
print "\n";

$DIR=`dirname $0`;
$DIR=~s/\n//;
$DIR=`(cd $DIR; pwd)`;
$DIR=~s/\n//;

$SORRENTO=`(cd $DIR/../../sorrento; pwd)`;
if ($? != 0) {
    print "ERROR. exit\n";
    exit 2;
}
$SORRENTO=~s/\n//;

#                                           |Lines       |Functions  |Branches    
# Filename                                  |Rate     Num|Rate    Num|Rate     Num
# ================================================================================
# [p4c/extensions/capri/]                                                         
# backend.cpp                               |13.0%     77|33.3%     9|            
# backend.h                                 | 100%      2|    -     0|            
# cl-options.cpp                            |73.8%    130|80.0%    10|            
# cl-options.h                              | 0.0%      2| 0.0%     1|            
# collect_inline_asm.cpp                    |93.3%     45|66.7%    15|            
# collect_inline_asm.h                      | 0.0%      1| 0.0%     2|            
#                                                                                 
# [p4c/extensions/capri/common/]                                                  
# code_builder.h                            |90.9%     11| 100%     2|            
# slice.h                                   |89.9%     69| 100%    11|            
# 

my %f = (
);

$result = "";
while (<>) {
    $_=~s/^(.+)\|( |\-|\d|\%|\.)*$/$1|/;
    $_=~s/$SORRENTO\///g;

    if (/total/i) {
        $TOTAL=$_;
        $TOTAL=~s/^\s+//;
        $TOTAL=~s/\s+$//;
    }

    if (/\[([^\\\]]+)\]/) {
        $f{$1} = $1;
    }
    # $_=~s/(\s+\-\s+\S+|Branches[ ]*|Rate     Num|============)$//;
    # $_=~s/^\[/\`\`\`\n\[/; ~s/\]$/\]\n\`\`\`/;
    # $_=~s/\]\n/\n/;
    # $_=~s/\[/\#\#\#\#\# /;
    # $_=~s/\=/\-/g;
    $result .= $_;
}

print "$TOTAL\n";
print "$result";

foreach my $d(sort (keys %f)) {
    print "[$d]($d)\n";
}

print "\n\nDIR=$DIR\n";
print "SORRENTO=$SORRENTO\n";