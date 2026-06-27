import os

FILE = "memo.txt"

def write_memo(user_message):
    PREFIX_LIST = ["ricordami di", "crea un promemoria", "crea una nota", "scrivi un promemoria", "scrivi una nota", "mi ricordi di"]
    user_memo = user_message.lower()
    for prefix in PREFIX_LIST:
        if user_memo.startswith(prefix):
            user_memo = user_message[len(prefix):]
            break

    if not user_memo.strip():
        return "Non mi ha detto cosa devo ricordarti."
    
    with open(FILE, "a", encoding="utf-8") as file:
        file.write(f"-{user_memo}\n")

    return f"Fatto! Ho annotato '{user_memo}'." 

def read_memo():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        return "Non hai ancora nessun promemoria"

    with open(FILE, "r", encoding="utf-8") as file:
        memo_list = file.readlines()

    memo_reply = "Ecco i tuoi promemoria:\n"

    return memo_reply + "".join(memo_list)
