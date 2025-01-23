from Inventory import Product
from Procurement import Supplier, PurchaseOrder


class Facade():
    def __init__(self):
        self.products = []
        self.suppliers = []
        self.stores = []        
        self.departments = []   
        self.staff = []    
        self.purchaseorders = []   
        self.sales = []
        
    @staticmethod
    def TriggerPurchaseOrder(productId, storeId):
        """
        Triggers a purchase order if the stock level of a product is below its reorder level.

        :param productId: The ID of the product to check.
        :param storeId: The ID of the store where stock is being checked.
        :return: A message indicating the result of the operation.
        """
        try:
            # Fetch the product
            product = Product.objects.get(ProductId=productId)

            # Get the current stock level for the product
            currentStock = product.GetStockLevel()

            # Check if stock is below reorder level
            if currentStock < product.ReorderLevel:
                # Fetch all associated suppliers for the product
                suppliers = Supplier.objects.filter(SupplierId=product.SupplierId.SupplierId)

                if not suppliers.exists():
                    return f"No suppliers found for product ID {productId}."

                # Choose the first supplier 
                supplier = suppliers.first()

                # Determine the reorder quantity (e.g., reorder to full stock level)
                reorderQuantity = product.ReorderLevel - currentStock
                totalAmount = reorderQuantity * product.Price

                # Create a new purchase order
                purchaseOrder = PurchaseOrder.CreatePurchaseOrder(
                    product=product,
                    totalAmount=totalAmount,
                    orderStatus="Pending",
                    supplierId = supplier
                )

                return f"Purchase order {purchaseOrder.PurchaseOrderId} created for product ID {productId} with quantity {reorderQuantity}."

            else:
                return f"Stock level ({currentStock}) for product ID {productId} is sufficient. No purchase order needed."

        except Product.DoesNotExist:
            return f"Product ID {productId} does not exist."

        except Exception as e:
            return f"Error triggering purchase order: {str(e)}"