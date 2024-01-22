# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Secrets Client,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import importlib
import json
import os
import ssl
import logging
import socket
import typing
import base64
from pathlib import Path
from uuid import UUID
from sys import exit as sys_exit

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_private_key,load_pem_private_key
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.asymmetric.padding import OAEP,MGF1

from atckit.utilfuncs import UtilFuncs
import argstruct

from convection.shared.config import ConvectionConfigCore, ConvectionConfiguration
from convection.shared.functions import get_actions
from convection.shared.exceptions import AuthenticationError, InvalidPrivateKeyError

class ConvectionSecretsClient:
    """Convection Secrets Client
    """
    _SERVICE_NAME:str = "convection-secrets"
    _SERVICE_SHUTDOWN_LIMIT:int = 300

    config:ConvectionConfigCore
    logger:logging.Logger
    _ssl_context:ssl.SSLContext
    _config_file:Path
    _config_path:Path
    _config:dict[str,typing.Any]
    _tls_ca:Path
    _socket_path:Path
    _config_prefix:str
    _server_ip:str
    _server_port:int
    _argstruct:argstruct.ArgStruct
    _action_map:dict[str,typing.Callable[[ssl.SSLSocket,typing.Union[tuple[str,int],str,None],typing.Union[dict[str,typing.Any],None]],None]]
    _connected:bool
    _connection:typing.Union[ssl.SSLSocket,None]

    _auth_token:typing.Union[str,None]
    _access_key_id:typing.Union[str,None]

    ACL_MODE_ALLOW:int = 1
    ACL_MODE_DENY:int = 0
    ACL_MODE_INVALID:int = -1

    ACL_ACCESS_MODE_INVALID:int = 224
    ACL_ACCESS_MODE_NONE:int = 0
    ACL_ACCESS_MODE_READ:int = 2
    ACL_ACCESS_MODE_WRITE:int = 4
    ACL_ACCESS_MODE_MODIFY:int = 8
    ACL_ACCESS_MODE_DELETE:int = 16

    ACL_TYPE_GENERIC:str = "ACLObject"
    ACL_TYPE_COMMAND:str = "ACLCommand"
    ACL_TYPE_STORE:str = "ACLStore"

    ATTACH_ACL_GROUP:str = "group"
    ATTACH_ACL_USER:str = "user"

    @property
    def connected(self) -> bool:
        """Whether Connection has been opened or not
        @retval bool Connected
        """
        return self._connected

    def __init__(self) -> None:
        self._access_key_id = None
        self._auth_token = None
        self._connected = False
        self._connection = None
        self.logger = UtilFuncs.create_object_logger(self)
        try:
            self.config = ConvectionConfiguration.instance
            self._config_prefix = "global.secrets.client"
        except BaseException:
            self.logger.debug("Failed to get ConvectionConfiguration instance, likely server only mode")
            self._config_prefix = "service"
            return
        self._load()
        if self.config.get_configuration_value(f"{self._config_prefix}.use_network"):
            self._server_ip:str = self.config.get_configuration_value(f"{self._config_prefix}.network.target_ip")
            self._server_port:int = int(self.config.get_configuration_value(f"{self._config_prefix}.network.target_port"))

    def have_tls_ca(self) -> bool:
        """CA Cert configred/existence Check
        @retval bool CA Cert configured and is file
        """
        try:
            tls_path:str = self.config.get_configuration_value(f"{self._config_prefix}.tls_ca")
        except ValueError:
            return False
        p:Path = Path(tls_path).resolve()
        return p.is_file()

    def get_configuration_value(self,name:str,prefix:bool = False) -> typing.Any:
        """Config Getter passthrough
        @param str \c name Name of Item to get
        @param bool \c prefix Whether or not to prepend the configured `_config_prefix` to the item name
        @retval Any Configuration Value
        """
        item_name:str
        if not prefix:
            item_name = name
        else:
            item_name = f"{self._config_prefix}.{name}"
        return self.config.get_configuration_value(item_name)

    def load_standalone(self,call_args:dict[str,typing.Any]) -> None:
        """Standalone Configuration Initializer
        Used for Service Specific / CLI operations
        @param dict[str,Any] \c call_args Commandline Arguments
        @retval None Nothing
        """
        if "config_prefix" in call_args.keys():
            self._config_prefix = call_args.pop("config_prefix")
        specker_root:str = "secrets-controller"
        if "specker_root" in call_args.keys():
            specker_root = call_args.pop("specker_root")
        config_root:Path = Path(call_args["config"]).resolve()
        config_path:typing.Union[Path,None]
        if config_root.is_file():
            config_path = config_root
        else:
            UtilFuncs.add_config_search_path(config_root)
            config_path = UtilFuncs.find_config_file(self._SERVICE_NAME,self._SERVICE_NAME)
            UtilFuncs.remove_config_search_path(config_root)
        if config_path is None:
            self.logger.critical(f"Unable to locate configuration file for {self._SERVICE_NAME}")
            self._config = {}
        else:
            self._config_file = config_path
            self._config_path = config_path.parent
            config_file_str:str = self._config_file.as_posix()
            self.logger.debug(f"Loading {config_file_str}")
            self._config = UtilFuncs.load_sfile(self._config_file)
        try:
            self.config = ConvectionConfigCore(specker_root,self._config)
        except BaseException as e:
            self.logger.critical(f"{type(e).__qualname__} - {e}")
            raise type(e)(e) from e
        self._load()
        if self.config.get_configuration_value(f"{self._config_prefix}.use_network"):
            self._server_ip:str = self.config.get_configuration_value(f"{self._config_prefix}.network.listen_ip")
            self._server_port:int = int(self.config.get_configuration_value(f"{self._config_prefix}.network.listen_port"))

    def _load(self) -> None:
        """TLS Initializer
        Init TLS Context, load CA Cert, etc
        @retval None Nothing
        """
        logging_fh:logging.FileHandler = logging.FileHandler(self.config.get_configuration_value(f"{self._config_prefix}.log_file"))
        logging.getLogger().addHandler(logging_fh)
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self._ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        self._ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        use_network:bool = self.config.get_configuration_value(f"{self._config_prefix}.use_network")
        if not bool(use_network):
            self._ssl_context.check_hostname = False
            self._socket_path:Path = Path(self.config.get_configuration_value(f"{self._config_prefix}.socket_path")).resolve()
        if self.have_tls_ca():
            tls_path:str = self.config.get_configuration_value(f"{self._config_prefix}.tls_ca")
            self._tls_ca:Path = Path(tls_path).resolve()
            if not self._tls_ca.is_file():
                tls_ca_str:str = self._tls_ca.as_posix()
                self.logger.critical(f"TLS CA was configured, but does not exist at {tls_ca_str}")
                sys_exit(1)
            self._ssl_context.load_verify_locations(self._tls_ca)
        else:
            self.logger.warning("===============================================================")
            self.logger.warning(" NO TLS CA WAS CONFIGURED. THIS IS SUBOPTIMAL")
            self.logger.warning(f" You should configure {self._config_prefix}.tls_ca")
            self.logger.warning("===============================================================")
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE

        self._action_map = get_actions(self)
        shared_path:Path = Path(importlib.import_module("convection.shared").__path__[0]).resolve()
        m_path:Path = shared_path.joinpath("convection-sm-commands.toml")
        spec_path:Path = shared_path.joinpath("specs/").resolve()
        self._argstruct = argstruct.ArgStruct(m_path,"toml",[spec_path])

    def command(self,command:str,data:typing.Union[dict[str,typing.Any],None] = None) -> typing.Union[dict[str,typing.Any],None]:
        """General Command Send, Read
        @param str \c command Command Name to Send
        @param Union[dict[str,Any],None] Data for Command
        @retval Union[dict[str,Any],None] None if no data returned, Result Object otherwise
        """
        if command not in self._argstruct.commands.keys():
            raise LookupError(f"'{command}' is not a valid command")
        self.connect()
        if not self.connected or self._connection is None:
            self.logger.error("Unable to connect to server. See previous errors")
            raise ConnectionError("Unable to connect to server. See previous errors")
        command_data:argstruct.ArgStructCommand = self._argstruct.commands[command]
        if command_data.get("auth_required"):
            if data is None:
                data = {}
            data = self._attach_auth_data(data)
        else:
            if self._access_key_id is not None:
                if data is None:
                    data = {}
                data["access_key_id"] = self._access_key_id
        if data is not None:
            data["command"] = command
            data = argstruct.parse(self._argstruct,data,"command")
            data.pop("command") # type: ignore
            if data is None:
                raise ValueError("Argument processing failed")
        self._send_command(command=command,data=data)
        return self._read_result()

    def _attach_auth_data(self,request_data:dict[str,typing.Any]) -> dict[str,typing.Any]:
        """Authentication Data attachment
        @param dict[str,Any] \c request_data Assembled Request Data
        @retval dict[str,Any] Request Data with Authentication data attached
        """
        if self._access_key_id is None or self._auth_token is None:
            self.logger.error("Not Authenticated")
            raise AuthenticationError()
        request_keys:list[str] = list(request_data.keys())
        if "access_key_id" in request_keys and "auth_token" in request_keys:
            self.logger.debug("NOTE: Skipping Auth Data Attachment, Request already provides AccessKeyID and AuthToken")
            return request_data
        request_data["access_key_id"] = self._access_key_id
        request_data["auth_token"] = self._auth_token
        return request_data

    def _send_command(self,command:str,data:typing.Union[dict[str,typing.Any],None] = None) -> None:
        """RAW Send Data to Server
        @param ssl.SSLSocket \c conn Remote Connection
        @param str \c command Command Name to Send
        @param Union[dict[str,Any],None] Data for Command
        @retval None Nothing
        """
        self.logger.debug(f"Sending Command: '{command}'")
        send_data:bytes = bytes(command,"utf-8")
        if data is not None:
            data_str:str = json.dumps(data)
            send_data += bytes(" ","utf-8")
            send_data += bytes(data_str,"utf-8")
        if self._connection is None:
            raise ConnectionError("Not Connected")
        self._connection.sendall(send_data)

    def _read_result(self) -> typing.Union[dict[str,typing.Any],None]:
        """RAW Read Data from Server
        @param ssl.SSLSocket \c conn
        @retval Union[dict[str,Any],None] None if no data returned, Result Object otherwise
        """
        if self._connection is None:
            raise ConnectionError("Not Connected")
        result:bytes = self._connection.read()
        if len(result) > 0:
            out:dict[str,typing.Any] = json.loads(result.decode("utf-8")) # mypy: type=ignore # type: ignore
            return out
        return None

    def get_access_key_id(self) -> typing.Union[str,None]:
        """Get Raw Access Key ID (SECURITY HAZARD)
        @retval Union[str,None] Access Key ID that has been set. None if not set
        """
        return self._access_key_id

    def get_auth_token(self) -> typing.Union[str,None]:
        """Get Raw Auth Token (SECURITY HAZARD)
        @retval Union[str,None] Auth Token that has been set or gotten from authorize command. None if not set
        """
        return self._auth_token

    def set_auth_token(self,access_key_id:str, auth_token:str) -> None:
        """Set Access Key and Auth Token to pre-specified value
        @param str \c access_key_id Access Key ID
        @param str \c auth_token Auth Token
        @retval None Nothing
        """
        self._access_key_id = access_key_id
        self._auth_token = auth_token

    def connect(self) -> ssl.SSLSocket:
        """Connect to Server
        @retval ssl.SSLSocket Server Connection
        Also sets _connection to same ssl.SSLSocket
        """
        if self.connected and self._connection is not None:
            self.logger.debug("Already Connected")
            return self._connection
        sock_type:int
        conn_target:typing.Union[str,tuple[str,int]]
        hostname:typing.Union[str,None]
        if not bool(self.config.get_configuration_value(f"{self._config_prefix}.use_network")):
            self.logger.info("Connecting via Socket")
            sock_type = socket.AF_UNIX
            conn_target = self._socket_path.as_posix()
            hostname=None
        else:
            self.logger.info("Connecting via Network")
            sock_type = socket.AF_INET
            conn_target = (self._server_ip,self._server_port)
            hostname = self._server_ip
        sock = socket.socket(sock_type, socket.SOCK_STREAM)
        conn:ssl.SSLSocket = self._ssl_context.wrap_socket(sock,server_hostname=hostname)
        self.logger.info(f"Connecting to Server {conn_target}")
        try:
            conn.connect(conn_target)
            conn.do_handshake(True)
            self._connected = True
        except (ConnectionError,FileNotFoundError) as e:
            self.logger.critical(f"Error during Connection: {e}")
            self._connected = False
        self._connection = conn
        return conn

    def close(self) -> None:
        """Close Connection
        @param ssl.SSLSocket \c conn Server Connection
        @retval None Nothing
        """
        if not self.connected or self._connection is None:
            return
        self._connection.send(bytes("close",encoding="utf-8"))
        self._connection.close()
        self._connected = False
        self._connection = None

    def status(self) -> dict[str,bool]:
        """System Information Request
        @retval dict[str,bool] Status Name, State
        """
        response:typing.Union[dict[str,typing.Any],None] = self.command("status",None)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        response.pop("result")
        return response

    def deauth(self) -> bool:
        """Deauth / Logout Call
        @param str \c access_key_id Access Key ID
        @param str \c auth_token Auth Token
        @retval bool Deauth Result (False )
        """
        if self._access_key_id is None or self._auth_token is None:
            self.logger.error("Not Authenticated")
            raise AuthenticationError()
        self.connect()
        if not self.connected or self._connection is None:
            self.logger.error("Unable to connect to server. See previous errors")
            raise ConnectionError("Unable to connect to server. See previous errors")
        data:dict[str,typing.Any] = {}
        self._send_command("deauth",self._attach_auth_data(data))
        response:typing.Union[dict[str,typing.Any],None] = self._read_result()
        self._access_key_id = None
        self._auth_token = None
        if response is None:
            self.logger.warning("Got Empty Response from Server")
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            return False
        return True

    def authorize(self,access_key_id:str,private_key:typing.Union[Path,str],key_password:typing.Union[str,None] = None, expire_time:typing.Union[str,None] = None) -> bool:
        """Command Authorization Call
        @param str access_key_id Access Key ID
        @param Union[Path,str] private_key Private Key. If String, must be the content of the private key (not the path, use pathlib.Path to reference the file)
        @param bool close_connection Whether or not to close connection when completed
        @retval Union[dict[str,Any],None] Response Data, may be None
        @raises InvalidPrivateKeyError Invalid Private Key Format (Not PEM/DER)
        @raises InvalidPrivateKeyError Provided Private Key was unable to decrypt token (Wrong Private Key)
        """
        self.connect()
        if not self.connected or self._connection is None:
            self.logger.error("Unable to connect to server. See previous errors")
            raise ConnectionError("Unable to connect to server. See previous errors")
        data:typing.Union[dict[str,typing.Any],None] = { "access_key_id": access_key_id, "expire_time": expire_time, "command": "authorize" }
        data = argstruct.parse(self._argstruct,data,"command")
        data.pop("command") # type: ignore
        self._send_command("authorize",data)
        response:typing.Union[dict[str,typing.Any],None] = self._read_result()
        if response is None:
            self.logger.error("Authorization Failed, Server returned empty Result")
            return False
        if not response["result"]["state"]:
            self.logger.error("Authorization Failed, Result was False")
            self.logger.error(', '.join(response["result"]["messages"]))
            return False
        token_id:str = UUID(bytes=self._private_key_decrypt(private_key,response["response"],key_password)).hex
        self._connection.send(bytes(token_id,"utf-8"))
        response = self._read_result()
        if response is None:
            self.logger.warning("Got Empty Response from Server")
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            return False
        self.logger.info("Authenticated!")
        self._access_key_id = access_key_id
        self._auth_token = token_id
        return True

    def _private_key_decrypt(self,private_key:typing.Union[Path,str],content:str,key_password:typing.Union[str,None] = None) -> bytes:
        """Decrypt Encrypted data
        @param Union[Path,str] \c private_key Path to private key (as Path only) or private key content (including header and footer)
        @param str \c content Encrypted content to decrypt
        @param Union[str,None] \c key_password Private Key password, default None
        @retval bytes Decrypted data as bytes
        """
        privkey_data:str = ""
        if isinstance(private_key,Path):
            with open(private_key.expanduser().resolve(),"r",encoding="utf-8") as f:
                privkey_data = f.read()
        else:
            privkey_data = private_key
        privkey_fixed:str = '\n'.join([ p for p in privkey_data.split('\n') if not p.startswith("-----") ])
        priv_obj:_RSAPrivateKey
        try:
            priv_obj = load_der_private_key(base64.b64decode(privkey_fixed),backend=default_backend(),password=key_password) # type: ignore
        except ValueError:
            self.logger.debug("Private Key was not a DER format, attempting PEM")
            try:
                priv_obj = load_pem_private_key(base64.b64decode(privkey_fixed),backend=default_backend(),password=key_password) # type: ignore
            except ValueError as e:
                self.logger.debug("Private Key was not a PEM format either, bailing out")
                self.logger.error(f"Unable to load Private Key, {e}")
                raise InvalidPrivateKeyError() from e
        try:
            result:bytes = priv_obj.decrypt(
                base64.b64decode(content),
                OAEP(
                    mgf=MGF1(algorithm=SHA512()),
                    algorithm=SHA512(),
                    label=None
                )
            )
        except ValueError as e:
            self.logger.info("Decryption Failed. Private Key does not match Access Key ID")
            raise InvalidPrivateKeyError(e) from e
        return result

    # Pylint Unused Argument flag is disabled for a majority of the Client Commands due to usage
    #  of `locals()`, linting doesnt catch that its used and so flags args as unused.
    # pylint: disable=unused-argument
    def audit_user(self,user_name:str) -> dict[str,typing.Any]:
        """Get User Information
        @param str \c user_name Username to get info on
        @retval dict[str,Any] User data. ACLs User has attached (includes group ACLs), Groups that user is a part of, Number of Access Keys and Number of Auth Tokens
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("audit_user",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        response.pop("result")
        return response

    def audit_group(self,group_name:str) -> dict[str,typing.Any]:
        """Get Group Information
        @param str \c group_name Group Name to get info on
        @retval dict[str,Any] Group Data. ACLs that Group has attached, List of Users in Group
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("audit_group",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        response.pop("result")
        return response

    def audit_acl(self,acl_name:str) -> dict[str,typing.Any]:
        """Get ACL Information
        @param str \c acl_name Name of ACL to get info on
        @retval dict[str,Any] ACL Object
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("audit_acl",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        response.pop("result")
        return response

    def list_groups(self) -> list[str]:
        """Group List
        @retval list[dict[str,typing.Any]] List of Registered Groups
        """
        response:typing.Union[dict[str,typing.Any],None] = self.command("list_groups",None)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        result:bool = response["result"]["state"]
        if not result:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return list[str](response["groups"])

    def list_users(self) -> list[str]:
        """User List
        @retval list[str] List of Registered Usernames
        """
        response:typing.Union[dict[str,typing.Any],None] = self.command("list_users",None)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        result:bool = response["result"]["state"]
        if not result:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return list[str](response["users"])

    def list_acls(self) -> list[str]:
        """ACL List
        @retval list[str] List of Registered ACL Names
        """
        response:typing.Union[dict[str,typing.Any],None] = self.command("list_acls",None)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        result:bool = response["result"]["state"]
        if not result:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return list[str](response["acls"])

    def create_user(self,user_name:str, public_key:typing.Union[Path,str]) -> str:
        """User Creation / Access Key Generation
        @param str \c username Username, created if does not exist
        @param Union[Path,str] public_key Public Key. If String, must be the content of the public key (not the path, use pathlib.Path to reference the file)
        @retval New Access Key ID
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        pubkey_data:str = ""
        if isinstance(public_key,str):
            self.logger.debug("Public Key was directly provided (not a file)")
            pubkey_data = public_key
        else:
            pubkey_path:Path = public_key.expanduser().resolve()
            if not pubkey_path.is_file():
                public_key_str:str = public_key.as_posix()
                raise FileNotFoundError(f"No Such Public Key {public_key_str}")
            with open(pubkey_path.resolve(),"r",encoding="utf-8") as f:
                pubkey_data = f.read()
        data["public_key"] = pubkey_data
        response:typing.Union[dict[str,typing.Any],None] = self.command("create_user",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return str(response["access_key_id"])

    def create_group(self,group_name:str) -> bool:
        """Group Create
        @param str \c group_name Name of Group to create (must be unique)
        @retval bool Success / Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("create_group",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def attach_group(self,group_name:str,user_name:str) -> bool:
        """Attach Group to User
        @param str \c group_name Name of Group to attach to User
        @param str \c user_name Name of User to attach Group to
        @retval bool Success/Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("attach_group",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def detach_group(self,group_name:str,user_name:str) -> bool:
        """Detach Group from User
        @param str \c group_name Name of Group to detach from User
        @param str \c user_name Name of User to detach Group from
        @retval bool Success/Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("detach_group",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def create_acl(self,acl_name:str,mode:int,access_mode:int, acl_type:str, acl_args:typing.Union[dict[str,typing.Any],None] = None) -> bool:
        """Create a new ACL
        @param str \c acl_name Name of ACL to create, must be unique
        @param int \c mode A ConvectionSecretsClient.ACL_MODE_* value
        @param int \c access_mode A ConvectionSecretsClient.ACL_ACCESS_MODE_* value
        @param str \c acl_type A ConvectionSecretsClient.ACL_TYPE_* value
        @param dict[str,Any] \c acl_args ACL Arguments, required keys depend on `acl_type`, see Documentation
        @retval bool Success/Failure
        """
        if acl_args is None:
            acl_args = {}
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        for k,v in acl_args.items():
            data[k] = v
        response:typing.Union[dict[str,typing.Any],None] = self.command("create_acl",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def attach_acl(self,acl_name:str, attach_type:str, attach_name:str) -> bool:
        """Attach ACL to User or Group
        @param str \c acl_name Name of ACL to attach, must exist
        @param str \c attach_type A ConvectionSecretsClient.ATTACH_ACL_* value
        @param str \c attach_name Name of Group or User to attach to
        @retval bool Success/Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("attach_acl",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def detach_acl(self,acl_name:str, detach_type:str, detach_name:str) -> bool:
        """Remove ACL from User or Group
        @param str \c acl_name Name of ACL to detach, must exist
        @param str \c attach_type A ConvectionSecretsClient.ATTACH_ACL_* value
        @param str \c attach_name Name of Group or User to detach from
        @retval bool Success/Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("detach_acl",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def remove_access(self,user_name:typing.Union[str,None] = None, remove_access_key_id:typing.Union[str,None] = None, remove_public_key:typing.Union[str,None] = None) -> bool:
        """Remove a User or Access Key ID / Public Key
        @param Union[str,None] \c user_name User name to operate on (if other fields filled), otherwise, User to delete completely
        @param Union[str,None] \c remove_access_key_id Access Key ID to remove
        @param Union[str,None] \c remove_public_key Public Key to search for, and remove associated Access Key ID, if found
        @retval bool Success/Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        if len(data) == 0:
            raise RuntimeError("At least one parameter of `remove_access` must be filled")
        response:typing.Union[dict[str,typing.Any],None] = self.command("remove_access",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def remove_acl(self,acl_name:str) -> bool:
        """Delete/Remove ACL
        @param str \c acl_name Name of ACL to delete
        @retval bool Success\Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("remove_acl",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def remove_group(self,group_name:str) -> bool:
        """Delete/Remove Group
        @param str \c group_name Name of Group to delete
        @retval bool Success/Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("remove_group",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def list_stores(self) -> list[str]:
        """List Registered Secrets Stores
        @retval list[str] List of Secrets Stores
        """
        response:typing.Union[dict[str,typing.Any],None] = self.command("list_stores")
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return list[str](response["stores"])

    def create_keyset(self,keyset_name:str) -> bool:
        """Create new KeySet
        @param str \c keyset_name Name of KeySet to create, Must be unique
        @retval bool Creation Success/Failure
        """
        data:dict[str,typing.Any] = locals()
        data.pop("self")
        response:typing.Union[dict[str,typing.Any],None] = self.command("create_keyset",data)
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return bool(response["result"]["state"])

    def list_keysets(self) -> list[str]:
        """List Registered KeySets
        @retval list[str] List of KeySet Names
        """
        response:typing.Union[dict[str,typing.Any],None] = self.command("list_keysets")
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return list[str](response["keysets"])

    def list_store_types(self) -> list[str]:
        """List Secrets Store Types
        @retval list[str] List of Secrets Store Types
        """
        response:typing.Union[dict[str,typing.Any],None] = self.command("list_store_types")
        if response is None:
            raise RuntimeError("Command returned an empty response")
        if not response["result"]["state"]:
            response_messages:str = '; '.join(response["result"]["messages"])
            self.logger.error(f"Command Failed. {response_messages}")
            raise RuntimeError(response_messages)
        return list[str](response["store_types"])
    # pylint: enable=unused-argument
