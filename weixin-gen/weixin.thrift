struct Article {
	1: string title,
	2: string description,
	3: string imageurl,
	4: string url,
}

struct News {
	1: string title,
	2: list<Article> articles,
}

struct Message {
	1: i32 id,
	2: string title,
	3: string content,
	4: string reason,
	5: string create_time,	
	6: i32 sort_id,
}

service DataService {
	bool pushMsg(1: list<Message> data),
	bool pushNews(1: list<News> data),
	bool pushString(1: string data),
	bool msgSortMark(1: list<i32> ids,2: i32 sort_id),

	bool deleteMeta(1: list<i32> ids),
	i32 getMsgCount(),
	i32 getMsgCountBySort(1: i32 sort_id),
	list<Message> pullMsg(1: i32 size),
	list<Message> pullMsgBySort(1: i32 size,2: i32 sort_id),
	list<Message> pullPaginateMsg(1: i32 start_index,2: i32 item_num),
	list<Message> pullPaginateMsgBySort(1: i32 start_index,2: i32 item_num,3: i32 sort_id),

	i32 pushApprove(1: list<Message> data),
	bool deleteMsgs(1: list<i32> ids),
	i32 getApproveCount(),
	list<Message> pullApprove(1: i32 start_index,2: i32 item_num),

	i32 pushDelicious(1: list<Message> data),
	bool deleteDelicious(1: list<i32> ids),
	i32 getDeliciousCount(),
	list<Message> pullDelicious(1: i32 start_index,2: i32 item_num),

	i32 pushHealthy(1: list<Message> data),
	bool deleteHealthy(1: list<i32> ids),
	i32 getHealthyCount(),
	list<Message> pullHealthy(1: i32 start_index,2: i32 item_num),
	
}