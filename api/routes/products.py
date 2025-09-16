from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from services.product_service import ProductService
from repositories.product_repo import ProductRepository
import shutil
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/", response_model=ProductOut)
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)):
    image_url = None
    if image:
        # guardas en static/images
        file_path = UPLOAD_DIR / image.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/images/{image.filename}"
    
    service = ProductService(ProductRepository(db))
    return service.create_product(ProductCreate(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image_url=image_url
    ))

@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    service = ProductService(ProductRepository(db))
    return service.get_products()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(ProductRepository(db))
    return service.get_product(product_id)

@router.put("/{product_id}", response_model=ProductOut, responses={
    404: {"description": "Product not found"},
    422: {"description": "Validation error"}
})
async def update_product(
    product_id: int,
    name: str = Form(None, min_length=1, max_length=100),
    description: str = Form(None, min_length=1, max_length=500),
    price: float = Form(None, gt=0),
    quantity: int = Form(None, ge=0),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    service = ProductService(ProductRepository(db))
    
    # Verificar si el producto existe
    existing_product = service.get_product(product_id)
    if not existing_product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = {}

    # Solo agregar los campos que no son None
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if price is not None:
        update_data["price"] = price
    if quantity is not None:
        update_data["quantity"] = quantity

    # Validar que al menos un campo fue proporcionado
    if not update_data and not image:
        return existing_product

    # Manejar la imagen si se proporciona
    if image:
        try:
            # Validar tipo de archivo
            if not image.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="File must be an image")
                
            # Crear un nombre de archivo único para evitar colisiones
            import uuid
            file_extension = Path(image.filename).suffix.lower()
            if not file_extension:
                file_extension = ".jpg"
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename
            
            # Guardar el archivo
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            # Actualizar la URL de la imagen
            update_data["image_url"] = f"/static/images/{unique_filename}"
            
            # Limpiar la imagen anterior si existe
            if existing_product.image_url:
                old_image_path = Path(".") / existing_product.image_url.lstrip("/")
                if old_image_path.exists() and old_image_path.is_file():
                    try:
                        old_image_path.unlink()
                    except Exception as e:
                        # Si falla al eliminar la imagen anterior, registrar el error pero continuar
                        print(f"Warning: Could not delete old image: {e}")
                        
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

    # Actualizar el producto con los datos validados
    try:
        updated_product = service.update_product(product_id, update_data)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product
    except ValueError as e:
        # Capturar errores de validación del modelo
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(ProductRepository(db))
    if not service.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
