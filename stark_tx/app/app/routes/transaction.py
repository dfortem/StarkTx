from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.engine.decoders.transaction import decode_transaction
from app.engine.output import print_transaction
from app.engine.providers.sequencer import get_transaction, get_block

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/{tx_hash}/", response_class=HTMLResponse)
@router.get("/{chain_id}/{tx_hash}/", response_class=HTMLResponse)
async def route_transaction(
    request: Request, tx_hash: str, chain_id: Optional[str] = None
):
    tx = starktx_transaction(chain_id, tx_hash)
    data = {"transaction": tx}
    return templates.TemplateResponse(
        "transaction.html", context={"request": request, "data": data}
    )


def starktx_transaction(chain_id: str, transaction_hash: str) -> dict:
    raw_transaction = get_transaction(chain_id, transaction_hash)
    raw_block = (
        (
            get_block(chain_id, raw_transaction["block_hash"])
            if "block_hash" in raw_transaction
            else None
        )
        if raw_transaction["block_hash"] != "pending"
        else "pending"
    )
    decoded_transaction = decode_transaction(chain_id, raw_block, raw_transaction)
    print_transaction(decoded_transaction)

    return decoded_transaction
