enum Operate{
  GET,
  DEL,
  ROLLBACK,
}

enum Type {
	Weibo,
  News,
  BBS,
  Weixin,
  QQ,
  Edit,
  Other,
}

struct Request{
  1: Operate operate
  2: i32      start   #从哪开始取
  3: i32      scope   #范围.每5分钟一个文件.指定数量来确定取多少个文件.
  4: Type     type
}

struct Data {
  1: string data,
  2: Type type,
}

service DataService {
	list<Data> pull(1: Request request)
}