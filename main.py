from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class FeeRequest(BaseModel):
    auction_type: str  # 'copart' or 'iaa'
    lot_or_stock_number: str
    bid_amount: float

class FeeResponse(BaseModel):
    breakdown: dict
    total: float

@app.post("/calculate", response_model=FeeResponse)
def calculate_fees(data: FeeRequest):
    bid = data.bid_amount
    auction = data.auction_type.lower()

    if auction == "copart":
        buyer_fee = max(0.04 * bid, 50)
        internet_fee = 59
        gate_fee = 79
        doc_fee = 35
    elif auction == "iaa":
        buyer_fee = max(0.035 * bid, 40)
        internet_fee = 60
        gate_fee = 45  # pull-out fee
        doc_fee = 25
    else:
        return {"breakdown": {}, "total": 0}

    fees = {
        "Your Bid": round(bid, 2),
        "Buyer Fee": round(buyer_fee, 2),
        "Internet Fee": internet_fee,
        "Gate/Pull-out Fee": gate_fee,
        "Document Fee": doc_fee
    }

    total = round(bid + buyer_fee + internet_fee + gate_fee + doc_fee, 2)

    return FeeResponse(breakdown=fees, total=total)
