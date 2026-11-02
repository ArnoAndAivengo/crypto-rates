import tkinter as tk
from tkinter import ttk

CRYPTOS = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "tether": "Tether (USDT)",
    "binancecoin": "BNB (BNB)",
    "solana": "Solana (SOL)",
    "ripple": "XRP (XRP)",
    "cardano": "Cardano (ADA)",
    "dogecoin": "Dogecoin (DOGE)",
}


def update_rates() -> None:
    pass


window = tk.Tk()
window.title("Курсы криптовалют")
window.geometry("360x480")
window.resizable(False, False)

tk.Label(
    window,
    text="Курсы популярных криптовалют",
    font=("", 12, "bold"),
).pack(pady=(20, 5))

tk.Label(
    window,
    text="относительно доллара США (USD)",
    font=("", 9),
    fg="gray",
).pack(pady=(0, 15))

frame = ttk.Frame(window, padding=10)
frame.pack(fill="both", expand=True, padx=20)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)

price_labels: dict[str, tk.Label] = {}

for row, (crypto_id, title) in enumerate(CRYPTOS.items()):
    tk.Label(frame, text=title, anchor="w").grid(
        row=row, column=0, sticky="w", pady=6
    )
    price = tk.Label(frame, text="— USD", anchor="e", width=14)
    price.grid(row=row, column=1, sticky="e", pady=6, padx=(10, 0))
    price_labels[crypto_id] = price

tk.Button(
    window,
    text="Обновить курсы",
    command=update_rates,
    width=20,
).pack(pady=20)

window.mainloop()
