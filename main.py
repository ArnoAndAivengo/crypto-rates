import json
import tkinter as tk
import urllib.error
import urllib.parse
import urllib.request
from tkinter import messagebox, ttk

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

API_URL = "https://api.coingecko.com/api/v3/simple/price"


def format_price(value: float) -> str:
    if value >= 1000:
        return f"{value:,.2f} USD"
    if value >= 1:
        return f"{value:.2f} USD"
    return f"{value:.6f} USD"


def fetch_rates() -> dict[str, float]:
    params = urllib.parse.urlencode(
        {
            "ids": ",".join(CRYPTOS.keys()),
            "vs_currencies": "usd",
        }
    )
    url = f"{API_URL}?{params}"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode())

    rates: dict[str, float] = {}
    for crypto_id in CRYPTOS:
        if crypto_id not in data or "usd" not in data[crypto_id]:
            raise KeyError(f"курс для {CRYPTOS[crypto_id]} не найден")
        rates[crypto_id] = float(data[crypto_id]["usd"])
    return rates


def update_rates() -> None:
    try:
        rates = fetch_rates()
    except urllib.error.URLError:
        messagebox.showerror(
            "Ошибка",
            "Не удалось подключиться к CoinGecko.\nПроверьте интернет-соединение.",
        )
        return
    except (KeyError, ValueError, json.JSONDecodeError) as error:
        messagebox.showerror("Ошибка", f"Не удалось получить курсы:\n{error}")
        return

    for crypto_id, price in rates.items():
        price_labels[crypto_id].config(text=format_price(price))


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
