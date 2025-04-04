from datetime import datetime

from repositories.configs_repository import get_config_by_name

from models.entities.item_loja_entity import ItemLojaEntity


class PriceCalculationService:
    def __init__(self, total_coins: int):
        self.total_coins = total_coins
        self.reserva_real = int(get_config_by_name("RESERVA_REAL").value)
        self.reserva_segura = self.reserva_real * 0.85

    def calculate_price(self, item: ItemLojaEntity) -> int:
        if not item.valor_real:
            return item.valor

        taxa_cambio_base = self._calculate_base_exchange_rate()
        fator_escassez = self._calculate_scarcity_factor()
        fator_semanal = self._calculate_weekly_factor()
        fator_horario = self._calculate_hourly_factor()

        return round(item.valor * taxa_cambio_base * fator_escassez * fator_semanal * fator_horario)

    def _calculate_base_exchange_rate(self) -> float:
        proporcao_reserva_usada = max(0, min(1, (self.reserva_real - self.reserva_segura) / self.reserva_real))
        return self.total_coins / self.reserva_real

    def _calculate_scarcity_factor(self) -> float:
        proporcao_reserva_usada = max(0, min(1, (self.reserva_real - self.reserva_segura) / self.reserva_real))
        return 1 + (1 - proporcao_reserva_usada) ** 2

    def _calculate_weekly_factor(self) -> float:
        dia_semana = datetime.now().weekday()
        return 0.95 + (dia_semana / 60)

    def _calculate_hourly_factor(self) -> float:
        hora_atual = datetime.now().hour
        if 11 <= hora_atual < 17:
            return 1.0 + (min(abs(14 - hora_atual), 5) * 0.02)
        return 0.9 + (min(hora_atual, 24 - hora_atual) * 0.01)
