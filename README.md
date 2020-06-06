# Unagi_ChatRooms
Бэкенд для чата-рулетки. Цифровой прорыв 2020 Кейс#2 Команда Унаги

API

GET /roulette/status
	OK

GET /roulette/contacts
	контакты

GET /roulette/chatrooms
	список комнат


GET /roulette/chatroom(integer)
	комната по (id=integer)


GET /roulette/addchatroom
	форма добавления новой комнаты
	
POST /roulette/addchatroom
	{'name'=string,
	'capacity'=integer}
	добавить новую комнату с заданным названием и вместимостью

GET /roulette/removechatroom(integer)
	удалить комнату по (id=integer)
	
GET /roulette/persons
	список участников
	
GET /roulette/person(integer)
	участник по (id=integer)
	
GET /roulette/addperson
	форма добавления нового участника
	
POST /roulette/addperson
	{'name'=string,
	'ticket'=string}
	добавить нового участника с заданным именем и номером билета

GET /roulette/removeperson(integer)
	удалить участника по (id=integer)
	
POST /roulette/movepersontochatroom
	{'person_id'=integer,
	'chatroom_id'=integer}
        добавить участника с id=person_id в комнату с id=chatroom_id, если хватит места

