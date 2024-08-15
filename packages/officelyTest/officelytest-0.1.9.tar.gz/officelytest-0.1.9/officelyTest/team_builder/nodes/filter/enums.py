from enum import Enum

class DataType(str, Enum):
    TEXT = 'TEXT'
    NUMBER = 'NUMBER'
    BOOLEAN = 'BOOLEAN'
    DATE = 'DATE'
    BASIC = 'BASIC'


class OperatorLabel(str, Enum):
    EQUAL = 'equal to'
    NOT_EQUAL = 'not equal to '
    EQUAL_INSENSETIVE = 'equal to (case insensitive)'
    NOT_EQUAL_INSENSETIVE = 'not equal to (case insensitive)'
    CONTAINS_INSENSETIVE = 'contains (case insensitive)'
    NOT_CONTAINS_INSENSETIVE = 'does not contain (case insensitive)'
    CONTAINS = 'contains'
    NOT_CONTAINS = 'does not contain'
    STARTS_WITH = 'starts with'
    NOT_STARTS_WITH = 'does not start with'
    STARTS_WITH_INSENSETIVE = 'starts with (case insensitive)'
    NOT_STARTS_WITH_INSENSETIVE = 'does not start with (case insensitive)'
    ENDS_WITH_INSENSETIVE = 'ends with (case insensitive)'
    NOT_ENDS_WITH_INSENSETIVE= 'does not end with (case insensitive)'
    ENDS_WITH = 'ends with'
    NOT_ENDS_WITH = 'does not end with'
    GREATER_THAN = 'greater than'
    LESS_THAN = 'less than'
    GREATER_THAN_OR_EQUAL_TO = 'greater than or equal to'
    LESS_THAN_OR_EQUAL_TO = 'less than or equal to'
    MATCHES_REGEX = 'matches regex'
    NOT_MATCHES_REGEX = 'does not match regex'
    MATCHES_REGEX_INSENSETIVE = 'matches regex (case insensitive)'
    NOT_MATCHES_REGEX_INSENSETIVE = 'does not match regex (case insensitive)'
    EXISTS = 'exists'
    NOT_EXISTS = 'does not exist'


class OperatorValue(str, Enum):
    EQUAL = "equal to"
    NOT_EQUAL = "not equal to "
    EQUAL_INSENSETIVE = "equal to (case insensitive)"
    NOT_EQUAL_INSENSETIVE = "not equal to (case insensitive)"
    CONTAINS_INSENSETIVE = "contains (case insensitive)"
    NOT_CONTAINS_INSENSETIVE = "does not contain (case insensitive)"
    CONTAINS = "contains"
    NOT_CONTAINS = "does not contain"
    STARTS_WITH = "starts with"
    NOT_STARTS_WITH = "does not start with"
    STARTS_WITH_INSENSETIVE = "starts with (case insensitive)"
    NOT_STARTS_WITH_INSENSETIVE = "does not start with (case insensitive)"
    ENDS_WITH_INSENSETIVE = "ends with (case insensitive)"
    NOT_ENDS_WITH_INSENSETIVE = "does not end with (case insensitive)"
    ENDS_WITH = "ends with"
    NOT_ENDS_WITH = "does not end with"
    GREATER_THAN = "greater than"
    LESS_THAN = "less than"
    GREATER_THAN_OR_EQUAL_TO = "greater than or equal to"
    LESS_THAN_OR_EQUAL_TO = "less than or equal to"
    MATCHES_REGEX = "matches regex"
    NOT_MATCHES_REGEX = "does not match regex"
    MATCHES_REGEX_INSENSETIVE = "matches regex (case insensitive)"
    NOT_MATCHES_REGEX_INSENSETIVE = "does not match regex (case insensitive)"
    EXISTS = "exists"
    NOT_EXISTS = "does not exist"
