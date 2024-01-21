import os
import web3
import kylink
from kylink.evm import ContractDecoder
import dotenv
dotenv.load_dotenv()

# FIXME: for intranet

# for internet
ky = kylink.Kylink(api_token=os.environ["KYLINK_API_TOKEN"]) 
