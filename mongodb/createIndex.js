conn = new Mongo();
db = conn.getDB("varpred");
db.variants37.createIndex({CHROM: 1, POS: 1, REF: 1, ALT: 1}, {name: "compound_index_37"});
db.variants38.createIndex({CHROM: 1, POS: 1, REF: 1, ALT: 1}, {name: "compound_index_38"});