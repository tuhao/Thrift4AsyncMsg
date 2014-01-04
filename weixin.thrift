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
	1: string title,
	2: string content,	
}

service DataService {
	bool pushMsg(1: list<Message> data),
	bool pushNews(1: list<News> data),
	bool pushString(1: string data),
}