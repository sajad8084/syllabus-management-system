from fatoora import Fatoora

fatoora_obj = Fatoora(
    seller_name="Awiteb",
    tax_number=1234567891,
    invoice_date=1635872693.3186214,
    total_amount=100,
    tax_amount=15,
)

fatoora_obj.qrcode("qr_code.png")