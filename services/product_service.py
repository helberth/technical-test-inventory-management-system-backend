from repositories.product_repo import ProductRepository
from models.product import Product

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, data):
        # data es un Pydantic model (ProductCreate)
        product = Product(**data.model_dump())  # <-- reemplazamos dict() por model_dump()
        return self.repo.create(product)

    def get_products(self):
        return self.repo.get_all()

    def get_product(self, product_id):
        return self.repo.get_by_id(product_id)

    def update_product(self, product_id, data):
        product = self.repo.get_by_id(product_id)
        if not product:
            return None
            
        # Manejar tanto diccionarios como objetos Pydantic
        update_data = data.model_dump(exclude_unset=True) if hasattr(data, 'model_dump') else data
        
        # Actualizar solo los campos proporcionados
        for key, value in update_data.items():
            if hasattr(product, key):
                # Solo actualizar si el valor no es None (a menos que sea explícitamente None en el diccionario)
                if value is not None or key in data:
                    setattr(product, key, value)
                    
        return self.repo.update(product)

    def delete_product(self, product_id):
        product = self.repo.get_by_id(product_id)
        if not product:
            return False
        self.repo.delete(product)
        return True
