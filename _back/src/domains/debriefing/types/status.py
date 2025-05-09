from enum import Enum


class DebriefingStatus(Enum):
    NAO_CONCLUIDO = "[ 📑 Não Concluído ]"
    NOTIFICAR = "[ 📨 Notifique! ]"
    SEM_ESTIMATIVA = "[ ⏱️ Sem Estimativa ]"
    ATRELAR_PROJETO = "[ 📦 Priorizar ]"
    CONCLUIDO = "[ ✅ Concluído ]"

    def __str__(self) -> str:
        return self.value
