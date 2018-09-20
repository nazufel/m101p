use enron

project = {$project: {_id:1, headers:1}}; null;

unwind_original_to = {$unwind:"$headers.To"}; null;

group_by_idfrom_then_addtoset = {$group:{
	_id: {oid:"$_id", from:"$headers.From"},
	to_filtered: {$addToSet:"$headers.To"}
}}; null;

unwind_filtered_to = {$unwind:"$to_filtered"}; null;

group_by_fromto = {$group:{
	_id: {from:"$_id.from", to:"$to_filtered"},
	count: {$sum:1}
}}; null;

sort_count_desc = {$sort: {count:-1}}; null;

limit = {$limit:5}; null;

db.messages.aggregate(
	project,
	unwind_original_to,
	group_by_idfrom_then_addtoset,
	unwind_filtered_to,
	group_by_fromto,
	sort_count_desc,
	limit
)
