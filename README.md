# EVENTPASS — Sistema de Gestión de Eventos y Tickets

Trabajo práctico de **Proyecto de Construcción de Software** (UADE, 2026). Docente: María Julia Monasterio. Grupo 2.

## Descripción

EVENTPASS centraliza la publicación de eventos y la venta de entradas. Los administradores registran los lugares, los organizadores publican sus eventos en esos lugares y los compradores consultan la cartelera y compran por sector o butaca. Funciona solo por consola.

Quedan fuera del sistema los pagos reales, las notificaciones, la interfaz web, el uso simultáneo de varios usuarios y la emisión de entradas con código QR.

## Roles

- **Administrador**: gestiona venues, sectores, horarios, categorías y cuentas de usuario.
- **Organizador**: crea y edita sus eventos, define precios, consulta ventas y genera el reporte de un evento.
- **Comprador**: busca la cartelera, compra entradas y consulta o cancela sus órdenes.

## Tecnologías

- Python 3
- Datos en archivos JSON
- Contraseñas almacenadas con hash SHA-256

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python main.py
```

Los tests se corren con `pytest`. El reporte de ventas de un evento se guarda en `reports/events-sales-report.txt`.

## Usuarios de prueba

| Usuario | Contraseña | Rol |
| --- | --- | --- |
| ADMIN | ADMIN123 | Administrador |
| LICHA | LICHA123 | Organizador |
| PEDRO | PEDRO123 | Comprador |
| JORGE | JORGE123 | Comprador |

Los datos de venues, eventos, categorías y órdenes están en `data/`.

## Estado del proyecto

Entrega final.

## Integrantes

- Lisandro Tosini (1244174)
- Pedro Zarza (1242754)
