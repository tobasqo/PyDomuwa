# PyDomuwa

## Domuwa is a locally hosted service, created to play games on a party

In the future, there will be implementation of games like Ego or Who's most likely,
Cards against humanity, etc.

App uses Python 3.11, FastAPI, SQLite database (pointed to file in project directory)
with alembic. Client will be created with React + Typescript (later).

Every player needs to connect their device (phone or pc) to the same Wi-Fi
as pc that app is hosted on. Then everybody goes to http address,
which is printed in console once the app has been started.

Every player can modify question and answers database (initially empty):

- add their own
- modify existing ones
- mark questions as excluded
- delete one by one

### Create `.env` in root folder (checkout `.env.example`)

`SECRET_KEY` can be created as:

```console
openssl rand -hex 32
```

### Run app

```console
docker compose up -d --build
```

### Shutdown app

```console
docker compose down
```

### List docker logs

```console
docker logs <container name> [-f] [-t]
```

Then go to http address printed in console

#### TODO

- [x] fix autoformatting in pycharm using ruff (probably paths)
- [x] raise 404 in routers
- [x] add tests for question
  - [x] understand `next_version` from questions and answers
  - [x] add tests for update and delete
- [x] add ep for questions view
- [x] fix answer services - update and delete
- [x] on `get_all` in questions and answers filter for `deleted` and order by `excluded`
- [x] update tests for answers
- [x] add game type
- [x] add qna category
- [x] services return None on error -> raise custom exc
- [ ] add game category
- [ ] add `deleted_by` field
- [x] [async test client](https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#set-tests-client-async-from-day-0)
- [ ] [async sqlite](https://arunanshub.hashnode.dev/async-database-operations-with-sqlmodel)
- permissions tests
  - [x] game type
  - [x] qna category
- add auth
  - [x] add user model
  - [x] remove `player_id` from `create` models
  - [x] update player to use user
  - [x] admin privileges
  - update allowed only by admin
    - [x] game type
    - [x] qna category
    - [ ] game category
  - delete allowed only by admin
    - [x] game type
    - [x] qna category
    - [ ] game category
  - update author on update
    - [x] question
    - [x] answer
- add game room
  - [ ] services
  - [ ] router
  - [ ] tests
- add ranking
  - [ ] services
  - [ ] router
  - [ ] tests
- [ ] aliases for api models' fields

##### TODO later

- [ ] add alembic
- [ ] start ui
- [ ] add pagination
- [ ] move to postgres
- [ ] add auth with fb
- [ ] lookup previous answer and question versions
