#TEST FILE
from dotenv import load_dotenv
import sys
import os
sys.path.append("./vaultUts")
from vaultUts import *
load_dotenv()





vlt = VaultLib("","",in_prd=True)

@vlt.link("Admin/data/TestCred")
class BotVault(): 
    hehe      : str

BotVault.hehe = "AI SIM"

BotVault.save()

pass

