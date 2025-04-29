from enum import Enum


class DebriefingStatus(Enum):
    NAO_PREENCHIDO = "[ 📑 Não preenchido ]"
    NOTIFICAR = "[ 📨 Notifique! ]"
    ATRELAR_PROJETO = "[ 📦 Atrelar Projeto ]"
    CONCLUIDO = "[ ✅ Concluído ]"

    def __str__(self) -> str:
        return self.value
