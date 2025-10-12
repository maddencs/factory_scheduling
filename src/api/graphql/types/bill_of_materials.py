import strawberry

from src.models import BillOfMaterials


@strawberry.type
class BillOfMaterialsType:
    id: int


def map_bill_of_materials_to_type(bill_of_materials: BillOfMaterials) -> BillOfMaterialsType:
    return BillOfMaterialsType(
        id=bill_of_materials.id,
    )
