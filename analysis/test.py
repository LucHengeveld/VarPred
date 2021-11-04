import vcf

file = vcf.Reader(open(
    "ALL.chr1.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf"))
print(file)
count = 0
for entry in file:
    print(entry)
    count += 1
    if count > 1:
        break
