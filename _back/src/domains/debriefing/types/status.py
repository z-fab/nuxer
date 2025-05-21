from enum import Enum


class DebriefingStatus(Enum):
    NAO_CONCLUIDO = "[ 📑 Não Concluído ]"
    SEM_ESTIMATIVA = "[ ⏱️ Sem Estimativa ]"
    NOTIFICAR = "[ 📨 Notifique! ]"
    EM_VALIDACAO = "[ 👀 Em Validação ]"
    ATRELAR_PROJETO = "[ 📦 Priorizar ]"
    CONCLUIDO = "[ ✅ Concluído ]"

    def __str__(self) -> str:
        return self.value
