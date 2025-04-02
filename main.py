import pygame
import random
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas as pd
from pygame import mixer
import sys
import os
from screeninfo import get_monitors 

monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height
window_width, window_height = 800, 600 
pos_x = (screen_width - window_width) // 2  
pos_y = (screen_height - window_height) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{pos_x},{pos_y}' 
pygame.init()
mixer.init()
# os.environ['SDL_VIDEO_CENTERED'] = '1' 
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SEXT simp-mulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
BLUE = (0, 0, 200)
DARK_BLUE = (0, 0, 150)
GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

font_small = pygame.font.SysFont('Arial', 12)
font_medium = pygame.font.SysFont('Arial', 16)
font_large = pygame.font.SysFont('Arial', 24)
font_title = pygame.font.SysFont('Arial', 28, bold=True)

stocks = {
    "AAPL": {"name": "Apple Inc.", "price": 150.0, "history": [], "color": RED, "sector": "Technology"},
    "MSFT": {"name": "Microsoft", "price": 250.0, "history": [], "color": BLUE, "sector": "Technology"},
    "GOOGL": {"name": "Alphabet", "price": 120.0, "history": [], "color": GREEN, "sector": "Technology"},
    "AMZN": {"name": "Amazon", "price": 110.0, "history": [], "color": ORANGE, "sector": "E-commerce"},
    "TSLA": {"name": "Tesla", "price": 180.0, "history": [], "color": (0, 200, 200), "sector": "Car"},
    "NVDA": {"name": "NVIDIA", "price": 300.0, "history": [], "color": (76, 187, 23), "sector": "Technology"},
    "META": {"name": "Meta", "price": 200.0, "history": [], "color": (0, 102, 204), "sector": "Technology"},
    "JPM": {"name": "JPMorgan", "price": 140.0, "history": [], "color": (0, 0, 100), "sector": "Finance"},
    "V": {"name": "Visa", "price": 220.0, "history": [], "color": (0, 100, 0), "sector": "Finance"},
    "WMT": {"name": "Walmart", "price": 60.0, "history": [], "color": (0, 150, 150), "sector": "Retail"},
}

market_indices = {
    "VN-INDEX": {"price": 1200.0, "history": [], "color": RED, "stocks": ["AAPL", "MSFT"]},
    "S&P 500": {"price": 4500.0, "history": [], "color": BLUE, "stocks": list(stocks.keys())[:10]},
    "NASDAQ": {"price": 14000.0, "history": [], "color": GREEN, "stocks": list(stocks.keys())[:15]}
}

news_items = [
    {"title": "The Federal Reserve may raise interest rates ", "impact": -0.03, "sectors": ["Finance"]},
    {"title": "AI technology has reached a new breakthrough", "impact": 0.05, "sectors": ["Technology"]},
    {"title": "Global oil prices are rising sharply", "impact": 0.02, "sectors": ["Energy"]},
    {"title": "Political instability in Europe", "impact": -0.04, "sectors": ["all"]},
    {"title": "Retail sales are experiencing strong growth", "impact": 0.03, "sectors": ["Retail", "e-commerce"]},
    {"title": "Inflation has slightly decreased", "impact": 0.01, "sectors": ["all"]},
    {"title": "Quarterly income announcement exceeds expectations", "impact": 0.08, "stocks": ["AAPL", "MSFT"]},
]

account = {
    "balance": 50000.0,
    "portfolio": {symbol: 0 for symbol in stocks},
    "pending_orders": [],
    "transaction_history": [],
    "total_value_history": []
}

simulation_time = datetime.now()
simulation_speed = 1
paused = False
news_log = []

particles = []

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.life = 30
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -1)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(0, self.size - 0.1)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

def add_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append(Particle(x, y, color))

# Tạo biểu đồ
def create_stock_chart(symbol, days=30):
    stock = stocks.get(symbol, market_indices.get(symbol))
    if not stock or len(stock["history"]) < 2:
        return None

    history = stock["history"][-days:]
    dates = [h["time"] for h in history]
    prices = [h["price"] for h in history]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(5, 2.5), dpi=80, facecolor='#2e2e2e')

    color = stock["color"]
    mpl_color = (color[0]/255, color[1]/255, color[2]/255)
    ax.plot(dates, prices, color=mpl_color, linewidth=2, label='Price')
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m'))

    if len(prices) >= 5:
        ma5 = pd.Series(prices).rolling(5).mean()
        ax.plot(dates, ma5, color='orange', linestyle='--', linewidth=1, label='MA5')

    ax.set_title(f"{symbol} - {days} Days", fontsize=10, color='white')
    ax.set_facecolor('#2e2e2e')
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax.tick_params(axis='both', which='major', labelsize=8, colors='white')
    
    if len(prices) >= 5:
        ax.legend(fontsize=8)
    
    fig.tight_layout()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    size = canvas.get_width_height()
    surf = pygame.image.frombuffer(buf, size, 'RGBA')
    plt.close(fig)
    
    return surf

def update_stock_prices():
    global news_log

    if random.random() < 0.2 and len(news_items) > 0:
        news = random.choice(news_items)
        news_time = simulation_time.strftime('%H:%M')
        news_log.append(f"{news_time}: {news['title']}")

        if "stocks" in news:
            for symbol in news["stocks"]:
                if symbol in stocks:
                    stocks[symbol]["price"] *= (1 + news["impact"])
        else:
            for symbol in stocks:
                if "sectors" in news:
                    if "all" in news["sectors"] or stocks[symbol]["sector"] in news["sectors"]:
                        stocks[symbol]["price"] *= (1 + news["impact"])

    for symbol in stocks:
        stock = stocks[symbol]
        change_percent = random.uniform(-0.5, 0.5) + (random.uniform(-1.5, 1.5) if random.random() < 0.1 else 0)
        new_price = stock["price"] * (1 + change_percent/100)
        stock["price"] = max(0.01, round(new_price, 2))

        stock["history"].append({
            "time": simulation_time,
            "price": stock["price"]
        })
    
    for index in market_indices:
        index_data = market_indices[index]
        total = 0
        valid_stocks = 0
        for symbol in index_data["stocks"]:
            if symbol in stocks:
                total += stocks[symbol]["price"]
                valid_stocks += 1
        
        if valid_stocks > 0:
            index_data["price"] = round(total / valid_stocks, 2)
            index_data["history"].append({
                "time": simulation_time,
                "price": index_data["price"]
            })

def draw_button(text, x, y, width, height, color, hover_color, text_color=BLACK, action=None, border_radius=5):
    mouse = pygame.mouse.get_pos()
    clicked = False
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=border_radius)
        if pygame.mouse.get_pressed()[0] == 1:
            clicked = True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=border_radius)
    
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2, border_radius=border_radius)
    
    text_surf = font_medium.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surf, text_rect)
    
    if clicked and action is not None:
        result = action()
        if result and (text.startswith("Buy")):
            add_particles(x + width//2, y + height//2, GREEN, 15)
        elif result and (text.startswith("Sell")):
            add_particles(x + width//2, y + height//2, RED, 15)
        return result
    return False

def draw_trading_interface(selected_stock):
    if selected_stock is None:
        return

    pygame.draw.rect(screen, WHITE, (850, 50, 530, 800), border_radius=10)
    pygame.draw.rect(screen, BLACK, (850, 50, 530, 800), 2, border_radius=10)
    
    stock = stocks.get(selected_stock, market_indices.get(selected_stock))
    if not stock:
        return
    
    title = font_large.render(f"{selected_stock} - {stock['name']}", True, BLACK)
    screen.blit(title, (860, 60))
    
    if selected_stock in stocks:
        sector_text = font_medium.render(f"Industry: {stock['sector']}", True, DARK_GRAY)
        screen.blit(sector_text, (860, 90))
    
    price_change = 0
    change_percent = 0
    if len(stock["history"]) > 1:
        price_change = stock["price"] - stock["history"][-2]["price"]
        change_percent = (price_change / stock["history"][-2]["price"]) * 100 if stock["history"][-2]["price"] != 0 else 0
    
    price_color = GREEN if price_change >= 0 else RED
    price_text = font_title.render(f"${stock['price']:.2f}", True, price_color)
    screen.blit(price_text, (860, 120))
    
    if len(stock["history"]) > 1:
        change_text = font_medium.render(f"{price_change:+.2f} ({change_percent:+.2f}%)", True, price_color)
        screen.blit(change_text, (1020, 130))
    
    # Biểu đồ
    chart = create_stock_chart(selected_stock)
    if chart:
        screen.blit(chart, (860, 160))
    
    if selected_stock in stocks:
        owned = account["portfolio"][selected_stock]
        owned_value = owned * stock["price"]
        owned_text = font_medium.render(f"Owned: {owned} (${owned_value:.2f})", True, BLACK)
        screen.blit(owned_text, (860, 350))

        draw_button("Buy 1", 860, 390, 80, 40, GREEN, DARK_GREEN, WHITE, lambda: buy_stock(selected_stock, 1))
        draw_button("Buy 5", 950, 390, 80, 40, GREEN, DARK_GREEN, WHITE, lambda: buy_stock(selected_stock, 5))
        draw_button("Buy 10", 1040, 390, 80, 40, GREEN, DARK_GREEN, WHITE, lambda: buy_stock(selected_stock, 10))
        
        draw_button("Sell 1", 860, 440, 80, 40, RED, DARK_RED, WHITE, lambda: sell_stock(selected_stock, 1))
        draw_button("Sell 5", 950, 440, 80, 40, RED, DARK_RED, WHITE, lambda: sell_stock(selected_stock, 5))
        draw_button("Sell 10", 1040, 440, 80, 40, RED, DARK_RED, WHITE, lambda: sell_stock(selected_stock, 10))

        pygame.draw.rect(screen, LIGHT_BLUE, (860, 490, 260, 120), border_radius=5)
        pygame.draw.rect(screen, BLACK, (860, 490, 260, 120), 1, border_radius=5)
        
        limit_text = font_medium.render("Place a limit order:", True, BLACK)
        screen.blit(limit_text, (870, 500))

        qty_text = font_small.render("Quantity:", True, BLACK)
        screen.blit(qty_text, (870, 530))
        pygame.draw.rect(screen, WHITE, (940, 530, 60, 20))
        pygame.draw.rect(screen, BLACK, (940, 530, 60, 20), 1)

        price_text = font_small.render("Cost:", True, BLACK)
        screen.blit(price_text, (870, 560))
        pygame.draw.rect(screen, WHITE, (940, 560, 80, 20))
        pygame.draw.rect(screen, BLACK, (940, 560, 80, 20), 1)

        draw_button("Buy (L)", 870, 590, 80, 30, GREEN, DARK_GREEN, WHITE, lambda: place_limit_order(selected_stock, "buy", 10, stock["price"]*0.98))
        draw_button("Sell (L)", 960, 590, 80, 30, RED, DARK_RED, WHITE, lambda: place_limit_order(selected_stock, "sell", 10, stock["price"]*1.02))

    history_title = font_medium.render("Transaction history:", True, BLACK)
    screen.blit(history_title, (860, 630))
    
    pygame.draw.rect(screen, WHITE, (860, 650, 510, 150))
    pygame.draw.rect(screen, BLACK, (860, 650, 510, 150), 1)
    
    for i, transaction in enumerate(account["transaction_history"][-6:]):
        color = GREEN if transaction["type"] == "SELL" else RED
        text = f"{transaction['time'].strftime('%H:%M')} {transaction['type']} {transaction['symbol']} {transaction['quantity']} @ ${transaction['price']:.2f}"
        trans_text = font_small.render(text, True, color)
        screen.blit(trans_text, (865, 655 + i*25))

def place_limit_order(symbol, order_type, quantity, limit_price):
    if symbol not in stocks:
        return False
        
    account["pending_orders"].append({
        "symbol": symbol,
        "type": order_type,
        "quantity": quantity,
        "limit_price": limit_price,
        "time": simulation_time
    })
    return True

def process_pending_orders():
    for order in account["pending_orders"][:]:
        if order["symbol"] not in stocks:
            continue
            
        stock = stocks[order["symbol"]]
        if (order["type"] == "buy" and stock["price"] <= order["limit_price"]) or \
           (order["type"] == "sell" and stock["price"] >= order["limit_price"]):
            
            if order["type"] == "buy":
                buy_stock(order["symbol"], order["quantity"])
            else:
                sell_stock(order["symbol"], order["quantity"])
            
            account["pending_orders"].remove(order)

def buy_stock(symbol, quantity):
    if symbol not in stocks:
        return False
        
    stock = stocks[symbol]
    total_cost = stock["price"] * quantity
    
    if account["balance"] >= total_cost:
        account["balance"] -= total_cost
        account["portfolio"][symbol] += quantity
        account["transaction_history"].append({
            "time": simulation_time,
            "type": "MUA",
            "symbol": symbol,
            "quantity": quantity,
            "price": stock["price"],
            "total": total_cost
        })
        return True
    return False

def sell_stock(symbol, quantity):
    if symbol not in stocks or account["portfolio"][symbol] < quantity:
        return False
        
    stock = stocks[symbol]
    total_value = stock["price"] * quantity
    
    account["balance"] += total_value
    account["portfolio"][symbol] -= quantity
    account["transaction_history"].append({
        "time": simulation_time,
        "type": "BÁN",
        "symbol": symbol,
        "quantity": quantity,
        "price": stock["price"],
        "total": total_value
    })
    return True

def draw_main_interface(selected_stock):
    global particles
    
    screen.fill(GRAY)

    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, 50))
    time_text = font_medium.render(f"Time: {simulation_time.strftime('%Y-%m-%d %H:%M')}", True, WHITE)
    screen.blit(time_text, (10, 15))

    draw_button("⏸️" if paused else "▶️", WIDTH-250, 10, 40, 30, WHITE, LIGHT_BLUE, action=lambda: toggle_pause())
    draw_button("+", WIDTH-200, 10, 30, 30, WHITE, LIGHT_BLUE, action=lambda: change_speed(1))
    draw_button("-", WIDTH-160, 10, 30, 30, WHITE, LIGHT_BLUE, action=lambda: change_speed(-1))
    speed_text = font_medium.render(f"Speed: {simulation_speed}x", True, WHITE)
    screen.blit(speed_text, (WIDTH-120, 15))
    
    balance = account["balance"]
    portfolio_value = sum(account["portfolio"][s] * stocks[s]["price"] for s in stocks)
    total_value = balance + portfolio_value
    
    balance_text = font_medium.render(f"balance: ${balance:,.2f} | Catalog: ${portfolio_value:,.2f} | Total: ${total_value:,.2f}", True, WHITE)
    screen.blit(balance_text, (WIDTH-600, 15))
    
    pygame.draw.rect(screen, WHITE, (10, 60, 830, 60))
    pygame.draw.rect(screen, BLACK, (10, 60, 830, 60), 1)
    
    for i, (index, data) in enumerate(market_indices.items()):
        x = 20 + i * 270
        change = 0
        if len(data["history"]) > 1:
            change = data["price"] - data["history"][-2]["price"]
        
        color = GREEN if change >= 0 else RED
        index_text = font_medium.render(f"{index}: {data['price']:.2f}", True, color)
        screen.blit(index_text, (x, 70))
        
        if len(data["history"]) > 1:
            change_text = font_small.render(f"{change:+.2f}", True, color)
            screen.blit(change_text, (x, 90))

    pygame.draw.rect(screen, BLACK, (10, 130, 830, 30))
    if news_log:
        news_text = font_small.render("News: " + news_log[-1][:100], True, YELLOW) 
        screen.blit(news_text, (15, 135))
    
    pygame.draw.rect(screen, WHITE, (10, 170, 830, 670))
    pygame.draw.rect(screen, BLACK, (10, 170, 830, 670), 2)

    headers = ["Code", "Company name", "Industry", "Cost", "Change", "Owner", "Value"]
    for i, header in enumerate(headers):
        x = 20 + i * 120 if i < 3 else 20 + 360 + (i-3) * 140
        header_text = font_medium.render(header, True, BLACK)
        screen.blit(header_text, (x, 180))
    
    # Dữ liệu cổ phiếu
    visible_stocks = list(stocks.items())[:15]
    
    for i, (symbol, stock) in enumerate(visible_stocks):
        y = 210 + i * 30
        if symbol == selected_stock:
            pygame.draw.rect(screen, LIGHT_BLUE, (10, y-5, 830, 30))
        
        symbol_text = font_medium.render(symbol, True, stock["color"])
        screen.blit(symbol_text, (20, y))

        short_name = stock["name"][:15] + "..." if len(stock["name"]) > 15 else stock["name"]
        name_text = font_medium.render(short_name, True, BLACK)
        screen.blit(name_text, (140, y))

        sector_text = font_medium.render(stock["sector"], True, DARK_GRAY)
        screen.blit(sector_text, (260, y))

        price_text = font_medium.render(f"${stock['price']:.2f}", True, BLACK)
        screen.blit(price_text, (380, y))

        if len(stock["history"]) > 1:
            change = stock["price"] - stock["history"][-2]["price"]
            prev_price = stock["history"][-2]["price"]
            change_percent = (change / prev_price) * 100 if prev_price != 0 else 0
            change_color = GREEN if change >= 0 else RED
            change_text = font_medium.render(f"{change:+.2f} ({change_percent:+.2f}%)", True, change_color)
            screen.blit(change_text, (500, y))

        owned_text = font_medium.render(str(account["portfolio"][symbol]), True, BLACK)
        screen.blit(owned_text, (640, y))

        value = account["portfolio"][symbol] * stock["price"]
        value_text = font_medium.render(f"${value:,.2f}", True, BLACK)
        screen.blit(value_text, (760, y))

    draw_trading_interface(selected_stock)

    for particle in particles[:]:
        particle.update()
        particle.draw(screen)
        if particle.life <= 0:
            particles.remove(particle)

def toggle_pause():
    global paused
    paused = not paused

def change_speed(delta):
    global simulation_speed
    simulation_speed = max(1, min(10, simulation_speed + delta))

def main():
    global simulation_time, particles
    
    for symbol in stocks:
        stocks[symbol]["history"].append({
            "time": simulation_time,
            "price": stocks[symbol]["price"]
        })
    
    for index in market_indices:
        market_indices[index]["history"].append({
            "time": simulation_time,
            "price": market_indices[index]["price"]
        })
    
    clock = pygame.time.Clock()
    running = True
    selected_stock = "AAPL"
    last_update_time = time.time()
    
    while True:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 10 <= mouse_pos[0] <= 840 and 170 <= mouse_pos[1] <= 840:
                    stock_index = (mouse_pos[1] - 210) // 30
                    visible_stocks = list(stocks.keys())[:15]
                    if 0 <= stock_index < len(visible_stocks):
                        selected_stock = visible_stocks[stock_index]

        if not paused and current_time - last_update_time > 1.0 / simulation_speed:
            simulation_time += timedelta(minutes=5)
            update_stock_prices()
            process_pending_orders()

            portfolio_value = sum(account["portfolio"][s] * stocks[s]["price"] for s in stocks)
            account["total_value_history"].append({
                "time": simulation_time,
                "value": account["balance"] + portfolio_value
            })
            last_update_time = current_time

        draw_main_interface(selected_stock)
        pygame.display.flip()
        clock.tick(60)
    

if __name__ == "__main__":
    main()