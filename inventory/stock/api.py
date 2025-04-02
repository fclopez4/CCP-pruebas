from typing import Annotated, List
import pandas as pd
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status, UploadFile, File
from sqlalchemy.orm import Session
from io import StringIO
from db_dependency import get_db

from . import mappers, schemas, services

stock_router = APIRouter(prefix="/stock")


@stock_router.post("/csv", status_code=status.HTTP_201_CREATED)
async def upload_inventory_csv(
    warehouse_id:  Annotated[str, Form()],
    inventory_upload: Annotated[UploadFile, File(...)],
    db: Session = Depends(get_db)
):
    """
    Carga masiva de inventario desde un archivo CSV.
    El archivo debe contener las columnas: product_id, quantity
    """
    if not inventory_upload.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un CSV"
        )
    
    # Leer el contenido del archivo CSV
    contents = await inventory_upload.read()
    s = StringIO(contents.decode('utf-8'))
    
    try:
        # Procesar el CSV con pandas
        df = pd.read_csv(s)
        
        # Verificar que el CSV tenga las columnas requeridas
        required_columns = ['product_id', 'quantity']
        if not all(column in df.columns for column in required_columns):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El CSV debe contener las columnas: {', '.join(required_columns)}"
            )
        
        # Convertir DataFrame a lista de diccionarios
        inventory_records = df.to_dict('records')
        
        # Estadísticas de la operación
        processed_records = len(inventory_records)
        successful_records = 0
        failed_records = 0

        # Validar que la bodega exista
        warehouse = services.get_warehouse(db, warehouse_id)
        if not warehouse:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="La bodega no existe"
            )

        # Validar y procesar cada registro
        for record in inventory_records:
            try:
                
                # Guardar el warehouse_id del primer registro válido para el registro de operación
                if not warehouse_id:
                    warehouse_id = record["warehouse_id"]
                
                # Validar que la cantidad sea positiva
                if record["quantity"] < 0:
                    failed_records += 1
                    continue
                
                # Buscar si ya existe el producto en la bodega
                existing_stock = services.get_stock(
                    db,
                    warehouse_id=warehouse_id,
                    product_id=record["product_id"]
                )

                if existing_stock:
                    # Actualizar el stock existente
                    services.increase_stock(
                        db,
                        warehouse_id=warehouse_id,
                        product_id=record["product_id"],
                        quantity=record["quantity"]
                    )
                else:
                    # Crear un nuevo registro de stock
                    services.create_stock(
                        db,
                        warehouse_id=warehouse_id,
                        product_id=record["product_id"],
                        quantity=record["quantity"]
                    )

                successful_records += 1
            except Exception as e:
                failed_records += 1
                continue
        
        # Registrar la operación
        operation = services.create_operation(
            db,
            file_name=inventory_upload.filename,
            warehouse_id=warehouse_id,
            processed_records=processed_records,
            successful_records=successful_records,
            failed_records=failed_records,
        )
        
        return Response(
            status_code=status.HTTP_201_CREATED,
            content=operation
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo CSV está vacío"
        )
    except pd.errors.ParserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo CSV tiene un formato inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar el archivo: {str(e)}"
        )


@stock_router.get("", response_model=List[schemas.StockResponseSchema])
def list_stock(
    params: schemas.FilterRequest = Depends(), db: Session = Depends(get_db)
):
    """
    Listar el inventario de productos en la bodega.
    """
    stock = services.get_stock(
        db,
        warehouse_id=params.warehouse,
        product_id=params.product
    )
    return mappers.stock_list_to_schema(stock)