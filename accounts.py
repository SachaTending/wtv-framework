from json import load, dump

class Account:
    name: str
    ssid: str

def gen_class(name: str, ssid: str) -> Account:
    temp = Account()
    temp.name = name
    temp.ssid = ssid
    return temp

def load_account(ssid: str):
    try: data = load(open(f"accounts/{ssid}.json"))
    except FileNotFoundError: data = {'name': 'Not exists anymore'}
    return gen_class(data['name'], ssid)