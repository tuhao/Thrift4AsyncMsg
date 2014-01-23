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
	list<Message> pullMsg(1: i32 size),
	list<Message> pullMsgBySort(1: i32 size,2: i32 sort_id),
	bool deleteMsgs(1: list<i32> ids),
}