# AgentFUD Password Manager #

This software is a proof of concept implenetation of a secure password storage.
It creates a single sqlite file which you can carry with you and even store it publicly,
no one will ever be able to decrypt your passwords without knowing your master password.

### Installation ###

```shell
pip install agentfud_password_manager
```

### Usage ###
```shell
bash$ af-password-manager
Usage: af-password-manager [OPTIONS] COMMAND [ARGS]...

  Welcome to AgentFUD Password Manager! A cli tool for managing your passwords

Options:
  --help  Show this message and exit.

Commands:
  add       Adding a new entry to the database
  delete    Deletes an entry
  generate  Generates a random password
  get       Decrypts the password and copies it to the clipboard
  info      AgentFUD Password Manager version and project info
  init      Initialization of the password manager
  list      Lists all the entries
```

- First initialize a new database if you don't have it (passwords.sqlite will be created)
```shell
bash$ af-password-manager init
```
It will ask for a master password. Keep it in mind that this is the key for everything, without it you won't be able to read or create new entries.

All the commands have help so the easiest way to explore what it can do is by typing --help after the command, for example:
```shell
bash$ af-password-manager add --help
Usage: af-password-manager add [OPTIONS]

  Adding a new entry to the database

Options:
  -su, --site-url TEXT    URL of the site where you want to log in
  -u, --username TEXT     User name
  -e, --email TEXT        Email address
  -p, --password TEXT     Password
  --master_password TEXT
  --help                  Show this message and exit.
```

Adding a new item is easy if you already signed for a service and you know the password.
```shell
bash$ af-password-manager add -su yoursite.com -e your@mail.com -p MySecretPassword33
```

If you don't have a password for a service the app can generate one for you. Simply just leave out the -p option
```shell
bash$ af-password-manager add -su yoursite.com -e your@mail.com
```

Getting one item is easy. first call the list, grab the id, then feed it to the ***get*** command
```shell
bash$ af-password-manager get -i 33
```
Remember, it won't print out to the screen, simply it copies to your clipboard.

### Development install ###
```shell
bash$ git@github.com:AgentFUD/agentfud-password-manager.git
bash$ cd agentfud-password-manager
bash$ python3 -m venv ./venv
bash$ source ./venv/bin/activate
bash$ pip install -r requirements.txt
bash$ pip install --editable .
```

Enjoy!