from steam.client import SteamClient
from enum import Enum

steam_client = SteamClient()

def sign_in(username,password):
    '''
    Signs in the global SteamClient object, with the provided username and password
    '''
    global steam_client 
    if(steam_client.session_id is None):
        steam_client.cli_login(username,password)

class Logical(Enum):
    '''
    An enum of all possible logic operations
    '''
    OR = 'or'
    AND = 'and'
    NOR = 'nor'
    NAND = 'nand'

    def __str__(self):
        return self.value

class SteamQueryParam(Enum):
    '''
    Enums with strings for different Steam query parameters
    '''
    NotEmpty = r'\empty\1'   
    NotFull = r'\full\1'  
    Secure = r'\secure\1'
    Dedicated = r'\dedicated\1'
    Linux = r'\linux\1'
    SpectatorProxy = r'\proxy\1'
    Whitelisted = r'\white\1'
    CollapseAddressHash = r'\collapse_addr_hash\1'
    #these require additional input and are generated from the get_param functions below
    __AppId = r'\appid'
    __GameType = r'\gametype'
    __ServerName = r'\name_match'
    __GameDir = r'\gamedir'
    __Map = r'\map'
    __GameAddr = r'\gameaddr'
    __Version = r'\version_match'

    def __str__(self):
        return self.value

    def generate_logical_query(logicOperation,params):
        '''
        Returns a string query that applies a logical operation on the supplied params
        logicOperation: The logic that connects the params. Accepted values or,and,nor,nand
        params: A list of SteamQueryParam that we want to apply the logical operation on

        ***

        example call: generate_logical_query(Logical.OR,[SteamQueryParam.NotEmpty,SteamQueryParam.Secure])
        return: '\or\\2\empty\\1\secure\\1'
        This query would return servers that are not empty OR not password protected 
        '''
        query = '\\'
        paramCount = len(params)
        if(paramCount==0):
            return query
        else:
            query+=str(logicOperation)
            query+=f'\{paramCount}'
        for param in params:
            query+=str(param)
        return query
    def get_servername_param(name):
        '''
        Returns a string query for the specified server name, surrounded by wildcards
        '''
        return rf'{SteamQueryParam.__ServerName}\*{name}*'
    def get_gametype_param(gametype):        
        '''
        Returns a string query for the specified gametype
        '''
        return f'{SteamQueryParam.__GameType}\{gametype}'
    def get_appId_param(appId):        
        '''
        Returns a string query for the specified appId
        '''
        return f'{SteamQueryParam.__AppId}\{appId}'
    def get_gamedir_param(gamedir):        
        '''
        Returns a string query for the specified gamedir
        '''
        return f'{SteamQueryParam.__GameDir}\{gamedir}'
    def get_map_param(map):        
        '''
        Returns a string query for the specified map
        '''
        return f'{SteamQueryParam.__Map}\{map}'
    def get_gameaddr_param(gameaddr):        
        '''
        Returns a string query for servers on the specified IP address (port supported and optional)
        '''
        return f'{SteamQueryParam.__GameAddr}\{gameaddr}'
    def get_version_param(version):
        '''
        Returns a string query for the specified version, surrounded by wildcards
        '''
        return rf'{SteamQueryParam.__Version}\*{version}*'
    
class SteamServerQuery():
    '''
    Generates Steam Server queries from the string list parameters
    See https://developer.valvesoftware.com/wiki/Master_Server_Query_Protocol for parameter syntax
    params: a string list of the parameters to be applied to the query. They are implicitly connected with an "AND" logical operator. 

    For other logical operators see SteamQueryParam.generate_logical_query()

    ***
    example call: SteamServerQuery(params=[SteamQueryParam.NotEmpty,SteamQueryParam.get_appId_param(1604030)])
    query result:  \\empty\\1\\appid\\1604030
    This query would return non-empty servers of appID 1604030
    
    '''
    def __init__(self,params=[] ):
        self.params = params

    def get_query(self):
        """
        Returns a string query with the parameters of the object
        """
        query = ''
        #for every parameter provided, adds its string to the query
        for param in self.params:
            query+=str(param)
        return query
    
def get_server_list(stringQuery, max_servers=20000,timeout = 50):
    '''
    Returns information about servers that match the description of the query

    stringQuery: A Steam Server Query
    '''
    result =  steam_client.gameservers.get_server_list(stringQuery,max_servers,timeout)
    return result