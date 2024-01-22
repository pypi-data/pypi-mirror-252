# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

class VersionCompatibilityError(RuntimeError):
    """Raised when Version Compatibility does not match up"""

class PubkeyExistsError(FileExistsError):
    """Raised during User creation and Pubkey is already associated with user"""

class InvalidAccessKeyError(ValueError):
    """Raised when access_key_id is not found"""

class InvalidPubKeyError(ValueError):
    """Raised when pubkey in DB is invalid"""

class InvalidPrivateKeyError(ValueError):
    """Raised when private key from client is invalid"""

class InvalidAuthTokenError(ValueError):
    """Raised when AuthToken was not in AuthDB"""

class SystemLockedWarning(UserWarning):
    """Raised when Locked (No unlock command has been received)"""

class KeyMapDBNotLoadedError(SystemError):
    """Raised when KeyMapDB is not loaded or was empty (should never be empty)"""

class AuthDBNotLoadedError(SystemError):
    """Raised when AuthDB is not loaded or was empty (should never be empty)"""

class ProtectedUserError(KeyError):
    """Raised when attempting to remove protected user"""

class InvalidUserError(ValueError):
    """Raised when user does not exist"""

class AuthenticationError(RuntimeError):
    """Raised when calling Command that requires authentication, but not authenticated"""

class ProtectedKeySetError(ValueError):
    """Raised when KeySet name is a Protected/Restricted KeySet name that cannot be used"""

class ACLExistsError(KeyError):
    """Raised when Item name already exists"""

class ACLNotExistError(KeyError):
    """Raised when Item name does not exist"""

class GroupNotExistError(KeyError):
    """Raised when Group does not Exist"""

class GroupExistsError(KeyError):
    """Raised when Group already exists"""

class ProtectedStoreError(ValueError):
    """Raised when attemping to use or remove a protected Store Name"""

class StoreNotLoadedError(SystemError):
    """Raised when Secrets Store attempted to be used before loading"""

class IncompleteError(SystemError):
    """Raised when Incomplete Function is called"""

class InvalidKeySet(KeyError):
    """Raised when KeySet name does not exist"""

class CriticalRotationError(Exception):
    """Raised when KeySet rotation failed in a potentially unrecoverable way"""

class KeyRotationError(SystemError):
    """Raised when KeySet rotation failed, but all rollbacks appear to have completed okay"""

class PathOutsideStoragePath(SystemError):
    """Raised when attempting to write to a storage path that is outside of the root storage path"""
