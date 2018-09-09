use test
db.zips.aggregate([
{ $project: { _id: 0, city: 1, pop: 1 } },
{ $match: { city: /^(B|D|O|G|N|M).*/ } },
{ $group: { _id: null, pop: { $sum: "$pop" } } },
{ $sort: { city: 1} }
])
