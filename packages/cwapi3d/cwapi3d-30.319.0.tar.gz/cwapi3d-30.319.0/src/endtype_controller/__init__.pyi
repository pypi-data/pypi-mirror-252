def get_last_error(error_code: int) -> str:
    """get last error
    Args:
        error_code ( int): error_code

    Returns:
        str
    """

def get_endtype_id(name: str) -> int:
    """Gets the endtypeID by endtypename 
    Args:
        name ( str): name

    Returns:
        int
    """

def get_endtype_id_start(element_id: int) -> int:
    """Gets the endtypeID of the start face 
    Args:
        element_id ( int): element_id

    Returns:
        int
    """

def get_endtype_id_end(element_id: int) -> int:
    """Gets the endtypeID of the end face 
    Args:
        element_id ( int): element_id

    Returns:
        int
    """

def get_endtype_id_facet(a0: int, a1: int) -> int:
    """get endtype id facet
    Args:
        a0 ( int): a0
        a1 ( int): a1

    Returns:
        int
    """

def set_endtype_name_start(element_id: int, name: str) -> None:
    """Sets the endtype to start face by endtypename 
    Args:
        element_id ( int): element_id
        name ( str): name

    Returns:
        None
    """

def set_endtype_name_end(element_id: int, name: str) -> None:
    """Sets the endtype to end face by endtypename 
    Args:
        element_id ( int): element_id
        name ( str): name

    Returns:
        None
    """

def set_endtype_name_facet(a0: int, a1: str, a2: int) -> None:
    """set endtype name facet
    Args:
        a0 ( int): a0
        a1 ( str): a1
        a2 ( int): a2

    Returns:
        None
    """

def set_endtype_id_start(element_id: int, endtype_id: int) -> None:
    """Sets the endtype to start face by endtypeID 
    Args:
        element_id ( int): element_id
        endtype_id ( int): endtype_id

    Returns:
        None
    """

def set_endtype_id_end(element_id: int, endtype_id: int) -> None:
    """Sets the endtype to end face by endtypeID 
    Args:
        element_id ( int): element_id
        endtype_id ( int): endtype_id

    Returns:
        None
    """

def set_endtype_id_facet(a0: int, a1: int, a2: int) -> None:
    """set endtype id facet
    Args:
        a0 ( int): a0
        a1 ( int): a1
        a2 ( int): a2

    Returns:
        None
    """

def clear_errors() -> None:
    """clear errors
    Args:

    Returns:
        None
    """

def create_new_endtype(endtype_name: str, endtype_id: int, folder_name: str) -> int:
    """Creates a new Endtype 
    Args:
        endtype_name ( str): endtype_name
        endtype_id ( int): endtype_id
        folder_name ( str): folder_name

    Returns:
        int
    """

def get_endtype_name(element_id: int) -> str:
    """Gets the endtypename by endtypeID 
    Args:
        element_id ( int): element_id

    Returns:
        str
    """

def get_endtype_name_start(element_id: int) -> str:
    """Gets the endtypename of the start face 
    Args:
        element_id ( int): element_id

    Returns:
        str
    """

def get_endtype_name_end(element_id: int) -> str:
    """Gets the endtypename of the end face 
    Args:
        element_id ( int): element_id

    Returns:
        str
    """

def get_endtype_name_facet(a0: int, a1: int) -> str:
    """get endtype name facet
    Args:
        a0 ( int): a0
        a1 ( int): a1

    Returns:
        str
    """

