import logging.config, json
import os, sys, pathlib, logging, requests
from requests.auth import HTTPBasicAuth

# Add "modules" to sys.path
sys.path.append(os.path.join(pathlib.Path(__file__).resolve().absolute().parents[2])) 

from airports_pipeline_modules.log_config.log_config import LoggingConf
from airports_pipeline_modules.main_config.main_config import Config

loggingConf = LoggingConf()
logging.config.dictConfig(config = loggingConf.config)
logger = logging.getLogger(__name__)

config = Config().mainConfigDict

username = config['ddlh']['username']
password = config['ddlh']['password']
host = config['ddlh']['host']
port = config['ddlh']['port']
systemRole = config['ddlh']['systemRole']
serviceUser = config['ddlh']['serviceUser']
redirectRole = config['ddlh']['redirectRole']
mviewRole = config['ddlh']['mviewRole']

authEndPoint = "/api/v1/biac/roles"
rolesEndPoint = "/api/v1/biac/roles"
queryParameters = dict(pageToken = "", pageSize = "", pageSort = "")


class DDLH(object):

    def __init__(self, host = host, port = port, username = username, password = password, authEndPoint = authEndPoint, rolesEndPoint = rolesEndPoint, 
                 systemRole = systemRole, redirectRole = redirectRole, mviewRole = mviewRole, serviceUser = serviceUser
                 ):
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.serviceUser = serviceUser

        self.authUrl = f"https://{host}:{port}{authEndPoint}"
        self.rolesUrl = f"https://{host}:{port}{rolesEndPoint}"
        
        
        self.systemRole = systemRole 
        self.systemRoleId = None
        self.systemRoleHeader = { "X-Trino-Role": "system=ROLE{" + systemRole + "}" }

        self.redirectRole = redirectRole
        self.redirectRoleId = None

        self.mviewRole = mviewRole
        self.mviewRoleId = None
        
        self.authenticated = False  
        self.redirectRoleCreated = False
        self.redirectGrantsGranted = False
        self.mviewRoleCreated = False
        self.mviewGrantsGranted = False

        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username = self.username, password = self.password)
        self.session.verify = False

    def log_in(self, queryParameters = queryParameters):

        _header = {"Accept": "application/json" }
        _header.update(self.systemRoleHeader)

        _queryParameters = queryParameters
        
        try:    
            response = self.session.get( url=self.authUrl, headers = _header, params = _queryParameters )
            response.raise_for_status()
        except Exception as err:
            logger.warning(err)
            return
        
        # print(response.status_code)
        # print(response.content)
        if response.status_code == requests.codes.ok:
            self.authenticated = True

    def create_redirect_role(self):

        _header = { "Accept": "application/json", "Content-Type": "application/json" }
        _header.update(self.systemRoleHeader)

        _payload = dict(name = self.redirectRole, description = "Redirect Role")

        try:
            response = self.session.post(url = self.rolesUrl, headers = _header, data = json.dumps(_payload))
            response.raise_for_status()
            self.redirectRoleId = json.loads(response.content.decode('UTF-8'))["id"]
        except Exception as err:
            logger.warning(err)
            return
        
        if response.status_code == requests.codes.ok:
            self.redirectRoleCreated = True

    def create_mview_role(self):

        _header = { "Accept": "application/json", "Content-Type": "application/json" }
        _header.update(self.systemRoleHeader)

        _payload = dict(name = self.mviewRole, description = "Materialized View Role")

        try:
            response = self.session.post(url = self.rolesUrl, headers = _header, data = json.dumps(_payload))
            response.raise_for_status()
            self.mviewRoleId = json.loads(response.content.decode('UTF-8'))["id"]
        except Exception as err:
            logger.warning(err)
            return
        
        if response.status_code == requests.codes.ok:
            self.mviewRoleCreated = True

        
    def get_system_role_id(self, queryParameters = queryParameters):

        _header = {"Accept": "application/json" }
        _header.update(self.systemRoleHeader)

        try: 
            response = self.session.get(url = self.rolesUrl, headers = _header, params = queryParameters)
            response.raise_for_status()
        except Exception as err:
            logger.critical(err)
            return
        
        responseDict = json.loads(response.content.decode('UTF-8'))
        # print(responseDict)

        systemRoleIdFound = False
        for role in responseDict["result"]:
            if not systemRoleIdFound:
                for k,v in role.items():
                    if v == self.systemRole:
                        self.systemRoleId = role["id"]
                        systemRoleIdFound = True
                        break
            else:
                break

    
    def assign_redirect_grants(self, rolesEndPoint = rolesEndPoint):

        if not self.redirectRoleId:
            logger.warning(f"System redirect role: {self.redirectRole} exists. Skipping grants...")
            return

        _header = { "Accept": "application/json", "Content-Type": "application/json" }
        _header.update(self.systemRoleHeader)

        self.redirectGrantsUrl = f"https://{host}:{port}{rolesEndPoint}/{self.redirectRoleId}/grants"

        # Table privileges
        actions = [ "SHOW", "CREATE", "ALTER", "DROP", "EXECUTE", "SELECT", "INSERT", "DELETE", "UPDATE", "REFRESH", "IMPERSONATE", "KILL", "SET", "PUBLISH"]
        # actions = ["SHOW"]

        self.redirectGrantsGranted = True
        for action in actions:

            logger.debug(f"Setting {action}...")

            _payload = dict(effect = "ALLOW", action = action, 
                        entity = dict(category = "TABLES", allEntities = True))

            try:
                response = self.session.post(url = self.redirectGrantsUrl, headers = _header, data = json.dumps(_payload))
                response.raise_for_status()
            except Exception as err:
                logger.critical(err)
        
            if response.status_code != requests.codes.ok:
                self.redirectGrantsGranted = False
        
        # System session privileges
        _payload = dict(effect = "ALLOW", action = "SET", 
                        entity = dict(category = "SYSTEM_SESSION_PROPERTIES", allEntities = True))   
          
        try:
            response = self.session.post(url = self.redirectGrantsUrl, headers = _header, data = json.dumps(_payload))
            response.raise_for_status()
        except Exception as err:
            logger.critical(err)
    
        if response.status_code != requests.codes.ok:
            self.redirectGrantsGranted = False

        # Catalog session privileges
        _payload = dict(effect = "ALLOW", action = "SET", 
                        entity = dict(category = "CATALOG_SESSION_PROPERTIES", allEntities = True))   
          
        try:
            response = self.session.post(url = self.redirectGrantsUrl, headers = _header, data = json.dumps(_payload))
            response.raise_for_status()
        except Exception as err:
            logger.critical(err)
    
        if response.status_code != requests.codes.ok:
            self.redirectGrantsGranted = False


    def assign_redirect_role_to_service_user(self):

        if not self.redirectRoleId:
            logger.warning(f"Redirect role {self.redirectRole} exists. Skipping role assignment...")
            return
        
        _header = { "Accept": "application/json", "Content-Type": "application/json" }
        _header.update(self.systemRoleHeader)

        _url = f"https://{host}:{port}/api/v1/biac/subjects/users/{self.serviceUser}/assignments"

        _payload = dict(roleId = self.redirectRoleId, roleAdmin = False)

        try:
            response = self.session.post(url = _url, headers = _header, data = json.dumps(_payload))
            response.raise_for_status()
        except Exception as err:
            logger.critical(err)
        
        return True if response.status_code == requests.codes.ok else False
    
    
    def assign_mview_grants(self, rolesEndPoint = rolesEndPoint):

        if not self.mviewRoleId:
            logger.warning(f"Materialized view role: {self.mviewRole} exists. Skipping grants...")
            return

        _header = { "Accept": "application/json", "Content-Type": "application/json" }
        _header.update(self.systemRoleHeader)

        self.mviewGrantsUrl = f"https://{host}:{port}{rolesEndPoint}/{self.mviewRoleId}/grants"

        # Table privileges
        actions = [ "SHOW", "CREATE", "ALTER", "DROP", "EXECUTE", "SELECT", "INSERT", "DELETE", "UPDATE", "REFRESH", "IMPERSONATE", "KILL", "SET", "PUBLISH"]
        # actions = ["SHOW"]

        self.mviewGrantsGranted = True
        for action in actions:

            logger.info(f"Setting {action}...")

            _payload = dict(effect = "ALLOW", action = action, 
                        entity = dict(category = "TABLES", allEntities = True))

            try:
                response = self.session.post(url = self.mviewGrantsUrl, headers = _header, data = json.dumps(_payload))
                response.raise_for_status()
            except Exception as err:
                logger.critical(err)
        
            if response.status_code != requests.codes.ok:
                self.mviewGrantsGranted = False

    def assign_mview_role_to_sytem_user(self):

        if not self.mviewRoleId:
            logger.warning(f"Materialized view role {self.mviewRole} exists. Skipping role assignment...")
            return
        
        _header = { "Accept": "application/json", "Content-Type": "application/json" }
        _header.update(self.systemRoleHeader)

        _url = f"https://{host}:{port}/api/v1/biac/subjects/users/{self.username}/assignments"

        _payload = dict(roleId = self.mviewRoleId, roleAdmin = True)

        try:
            response = self.session.post(url = _url, headers = _header, data = json.dumps(_payload))
            response.raise_for_status()
        except Exception as err:
            logger.critical(err)
        
        return True if response.status_code == requests.codes.ok else False
        
if __name__ == "__main__":

    ddlh = DDLH()
    ddlh.log_in()
    if not ddlh.authenticated:
        logger.critical("Could not log in to DDAE. Quiting...")
        sys.exit(-1)
    
    # Table Scan Reirect Privileges
    ddlh.create_redirect_role()
    print(ddlh.redirectRoleCreated)
    print(ddlh.redirectRoleId)

    ddlh.assign_redirect_grants()
    print(ddlh.redirectGrantsGranted)

    ddlh.assign_redirect_role_to_service_user()

    # Materialized View Privileges
    ddlh.get_system_role_id()
    print(ddlh.systemRoleId)

    ddlh.create_mview_role()
    print(ddlh.mviewRoleId)

    ddlh.assign_mview_grants()
    print(ddlh.mviewGrantsGranted)

    ddlh.assign_mview_role_to_sytem_user()


