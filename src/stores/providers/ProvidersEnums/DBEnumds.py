from enum import Enum


class DBProviders(Enum):
    QDRANT = "QDRANT"
    PGVECTOR = "PGVECTOR"


class PGVectorDistanceEnum(Enum):
    COSINE = "<=>"
    L2 = "<->"
    INNER_PRODUCT = "<#>"


class QDrantDistanceEnum(Enum):
    COSINE = "Cosine"
    EUCLID = "Euclid"
    DOT = "Dot"
