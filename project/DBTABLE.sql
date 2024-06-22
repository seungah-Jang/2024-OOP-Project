
create table TB_SESSION_RESULT  (
session_id INT auto_increment primary key,
session_start_time datetime not null,
total_keystrokes INT,
correct_cnt INT,
elapsed_time FLOAT,
accuracy FLOAT,
wpm FLOAT
);

create table TB_KEY (
idx INT auto_increment primary key,
session_id int not null,
key_value char,
total_keyvalue INT,
correct_keyvalue INT,
incorrect_keyvalue INT,
FOREIGN KEY (session_id) REFERENCES TB_SESSION_RESULT(session_id) ON DELETE CASCADE
);


