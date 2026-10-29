"""Exception domain. Dipetakan ke HTTP status code di app/main.py."""


class DomainError(Exception):
    """Base class untuk semua error bisnis."""


class NotFoundError(DomainError):
    """Data tidak ditemukan -> 404."""


class BusinessRuleError(DomainError):
    """Pelanggaran aturan bisnis (mis. durasi > 3 jam) -> 422."""


class ConflictError(DomainError):
    """Konflik data (mis. jadwal bentrok) -> 409."""
