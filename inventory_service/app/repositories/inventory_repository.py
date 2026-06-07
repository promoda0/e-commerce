from sqlalchemy.orm import Session

from inventory_service.app.models.inventory import Inventory


class InventoryRepository:
    @staticmethod
    def create_inventory(
        db: Session,
        *,
        product_id: int,
        total_stock: int,
        reserved_stock: int,
        available_stock: int,
        reorder_level: int,
    ) -> Inventory:
        inventory = Inventory(
            product_id=product_id,
            total_stock=total_stock,
            reserved_stock=reserved_stock,
            available_stock=available_stock,
            reorder_level=reorder_level,
        )
        db.add(inventory)
        db.flush()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def get_inventory_by_product(db: Session, product_id: int) -> Inventory | None:
        return db.query(Inventory).filter(Inventory.product_id == product_id).first()

    @staticmethod
    def update_stock(
        db: Session,
        inventory: Inventory,
        *,
        total_stock: int,
        available_stock: int,
        reorder_level: int,
    ) -> Inventory:
        inventory.total_stock = total_stock
        inventory.available_stock = available_stock
        inventory.reorder_level = reorder_level
        db.flush()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def reserve_stock(db: Session, inventory: Inventory, quantity: int) -> Inventory:
        inventory.reserved_stock += quantity
        inventory.available_stock -= quantity
        db.flush()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def release_stock(db: Session, inventory: Inventory, quantity: int, *, deduct: bool) -> Inventory:
        inventory.reserved_stock -= quantity
        if deduct:
            inventory.total_stock -= quantity
        else:
            inventory.available_stock += quantity
        db.flush()
        db.refresh(inventory)
        return inventory

