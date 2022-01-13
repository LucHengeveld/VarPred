mongoimport --host mongodb --db varpred --collection variants37 --type json --file variant-37.json --jsonArray 
mongoimport --host mongodb --db varpred --collection variants38 --type json --file variant-38.json --jsonArray
mongoimport --host mongodb --db varpred --collection medgen --type json --file medgen.json --jsonArray
mongoimport --host mongodb --db varpred --collection genes --type json --file gene.json --jsonArray