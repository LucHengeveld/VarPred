#!/usr/bin/env bash

if [ -f "clinvar-38.vcf" ] ; then
    wget -O clinvar-38.vcf.gz.md5 https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.md5
    md5sum=$(cat clinvar-38.vcf.gz.md5)
    md5sum=$(echo "$md5sum" | cut -d' ' -f 1)
    md5check=$(md5sum clinvar-38.vcf.gz)
    md5check=$(echo "$md5check" | cut -d' ' -f 1)
    
    if [[ "$md5sum" == "$md5check" ]]; then
        echo ClinVar file is up-to date
    else
        echo ClinVar file is not up to date
        wget -O clinvar-38.vcf.gz https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
        gzip -d -k -f clinvar-38.vcf.gz
    fi
else
    echo ClinVar file not found
    wget -O clinvar-38.vcf.gz https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
    gzip -d -k -f clinvar-38.vcf.gz
fi

if [ -f "clinvar-37.vcf" ] ; then
    wget -O clinvar-37.vcf.gz.md5 https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz.md5
    md5sum=$(cat clinvar-37.vcf.gz.md5)
    md5sum=$(echo "$md5sum" | cut -d' ' -f 1)
    md5check=$(md5sum clinvar-37.vcf.gz)
    md5check=$(echo "$md5check" | cut -d' ' -f 1)
    
    if [[ "$md5sum" == "$md5check" ]]; then
        echo ClinVar file is up-to date
    else
        echo ClinVar file is not up to date
        wget -O clinvar-37.vcf.gz https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz
        gzip -d -k -f clinvar-37.vcf.gz
    fi
else
    echo ClinVar file not found
    wget -O clinvar-37.vcf.gz https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz
    gzip -d -k -f clinvar-37.vcf.gz
fi