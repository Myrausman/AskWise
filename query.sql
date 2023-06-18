CREATE TABLE "users" (
	"fname"	TEXT NOT NULL,
	"lname"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"gender"	TEXT NOT NULL,
	PRIMARY KEY("email")
);

CREATE TABLE "topic" (
	"topic_id"	INTEGER,
	"title"	VARCHAR(255) NOT NULL,
	"details"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"updated_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("email") REFERENCES "users"("email"),
	PRIMARY KEY("topic_id" AUTOINCREMENT)
);
CREATE TABLE "tags" (
	"tag_id"	INTEGER,
	"topic_id"	INTEGER NOT NULL,
	"tag"	TEXT NOT NULL,
	PRIMARY KEY("tag_id" AUTOINCREMENT),
	FOREIGN KEY("topic_id") REFERENCES "topic"("topic_id")
);

