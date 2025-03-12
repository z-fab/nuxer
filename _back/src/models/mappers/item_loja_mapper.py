from models.entities.item_loja_entity import ItemLojaEntity
from models.orm.item_loja import ItemLoja


class ItemLojaMapper:
    @staticmethod
    def orm_to_entity(orm_itemloja: ItemLoja) -> ItemLojaEntity:
        return ItemLojaEntity(
            cod=orm_itemloja.cod,
            nome=orm_itemloja.nome,
            descricao=orm_itemloja.descricao,
            valor=orm_itemloja.valor,
            valor_real=orm_itemloja.valor_real,
            amount=orm_itemloja.amount,
            enable=orm_itemloja.enable,
        )
