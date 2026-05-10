import customtkinter as ctk
from tkinter import messagebox
import aiohttp
import asyncio
import threading
from io import BytesIO
from PIL import Image, ImageTk
import os

from weather_api import get_weather_data, get_forecast_data
from utils.config_handler import get_api_key, save_api_key
from utils.db_handler import init_db, save_search, get_recent_searches
from utils.graph_generator import generate_forecast_graph
import requests # İkon indirmek için hala basit requests kullanılabilir

# CustomTkinter Ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class WeatherDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hava Durumu Paneli")
        self.geometry("900x600")
        self.resizable(False, False)
        
        init_db() # Veritabanını başlat
        self.set_icon() # İkonu ayarla
        self.check_api_key()
        self.create_layout()
        self.load_history()

    def set_icon(self):
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                photo = ImageTk.PhotoImage(img)
                self.wm_iconphoto(False, photo)
        except Exception as e:
            print(f"İkon yükleme hatası: {e}")
        
    def check_api_key(self):
        api_key = get_api_key()
        if not api_key:
            dialog = ctk.CTkInputDialog(text="OpenWeatherMap API Anahtarınızı girin:", title="API Anahtarı Gerekli")
            key = dialog.get_input()
            if key and key.strip():
                save_api_key(key.strip())
            else:
                messagebox.showerror("Kritik Hata", "API anahtarı olmadan uygulama çalışamaz!")
                self.destroy()

    def create_layout(self):
        # Sol Menü (Geçmiş Aramalar)
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.lbl_history = ctk.CTkLabel(self.sidebar, text="Son Aramalar", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_history.pack(pady=20, padx=20)
        
        self.history_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.history_frame.pack(fill="both", expand=True, padx=10)
        
        # Sağ Panel (İçerik)
        self.main_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.main_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Arama Kısmı
        self.search_frame = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.search_frame.pack(fill="x", pady=(0, 20))
        
        self.entry_city = ctk.CTkEntry(self.search_frame, placeholder_text="Şehir Adı Girin...", font=ctk.CTkFont(size=14))
        self.entry_city.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_search = ctk.CTkButton(self.search_frame, text="Ara", width=100, command=self.on_search_clicked, font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_search.pack(side="right")
        
        # Güncel Hava Durumu Kartı
        self.current_card = ctk.CTkFrame(self.main_panel, corner_radius=15, height=180)
        self.current_card.pack(fill="x", pady=(0, 20))
        self.current_card.pack_propagate(False)
        
        self.lbl_icon = ctk.CTkLabel(self.current_card, text="☁️", font=ctk.CTkFont(size=60))
        self.lbl_icon.pack(side="left", padx=30)
        
        self.info_frame = ctk.CTkFrame(self.current_card, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True, pady=20)
        
        self.lbl_city_name = ctk.CTkLabel(self.info_frame, text="Hoş Geldiniz", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_city_name.pack(anchor="w")
        
        self.lbl_temp = ctk.CTkLabel(self.info_frame, text="--°C", font=ctk.CTkFont(size=40, weight="bold"), text_color="#0AC8B9")
        self.lbl_temp.pack(anchor="w", pady=5)
        
        self.lbl_details = ctk.CTkLabel(self.info_frame, text="Lütfen yukarıdan bir şehir aratın.", font=ctk.CTkFont(size=14))
        self.lbl_details.pack(anchor="w")
        
        # Grafik Kartı
        self.graph_card = ctk.CTkFrame(self.main_panel, corner_radius=15)
        self.graph_card.pack(fill="both", expand=True)
        
        self.lbl_graph = ctk.CTkLabel(self.graph_card, text="Grafik Yükleniyor...", font=ctk.CTkFont(size=16))
        self.lbl_graph.pack(expand=True)

    def load_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        recent = get_recent_searches()
        if not recent:
            ctk.CTkLabel(self.history_frame, text="Henüz arama yapılmadı.").pack(pady=10)
            
        for city, temp, desc, _ in recent:
            btn = ctk.CTkButton(self.history_frame, text=f"{city.title()} ({temp}°C)", 
                              fg_color="#2b2b2b", hover_color="#3b3b3b", anchor="w",
                              command=lambda c=city: self.search_from_history(c))
            btn.pack(fill="x", pady=5)

    def search_from_history(self, city):
        self.entry_city.delete(0, "end")
        self.entry_city.insert(0, city)
        self.on_search_clicked()

    def on_search_clicked(self):
        city = self.entry_city.get().strip()
        if not city:
            return
            
        self.btn_search.configure(state="disabled", text="Aranıyor...")
        self.lbl_city_name.configure(text=f"Aranıyor: {city}")
        
        # Asenkron işlemi arka plan thread'inde başlat
        threading.Thread(target=self.run_async_fetch, args=(city,), daemon=True).start()

    def run_async_fetch(self, city):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            weather_data, forecast_data = loop.run_until_complete(self.fetch_all_data(city))
            # Tkinter arayüzünü ana thread'de güncellemek için after kullanılır
            self.after(0, self.update_ui_success, weather_data, forecast_data, city)
        except aiohttp.ClientResponseError as e:
            self.after(0, self.update_ui_error, e.status, city)
        except Exception as e:
            self.after(0, self.update_ui_error, 500, str(e))
        finally:
            loop.close()

    async def fetch_all_data(self, city):
        weather = await get_weather_data(city)
        forecast = await get_forecast_data(city)
        return weather, forecast

    def update_ui_success(self, weather, forecast, searched_city):
        self.btn_search.configure(state="normal", text="Ara")
        
        # Güncel Durum
        temp = weather['main']['temp']
        desc = weather['weather'][0]['description'].capitalize()
        name = weather['name']
        country = weather['sys']['country']
        
        self.lbl_city_name.configure(text=f"{name}, {country}")
        self.lbl_temp.configure(text=f"{temp:.1f}°C")
        self.lbl_details.configure(text=f"{desc} | Nem: %{weather['main']['humidity']} | Rüzgar: {weather['wind']['speed']} m/s")
        
        # İkonu senkron olarak yükleyebiliriz (Pillow blocking)
        icon_code = weather['weather'][0]['icon']
        try:
            resp = requests.get(f"http://openweathermap.org/img/wn/{icon_code}@2x.png")
            img = Image.open(BytesIO(resp.content)).convert("RGBA")
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 100))
            self.lbl_icon.configure(image=ctk_img, text="")
        except:
            pass
            
        # Grafik Oluştur ve Göster
        try:
            graph_img = generate_forecast_graph(forecast)
            ctk_graph = ctk.CTkImage(light_image=graph_img, dark_image=graph_img, size=(600, 300))
            self.lbl_graph.configure(image=ctk_graph, text="")
        except Exception as e:
            self.lbl_graph.configure(text=f"Grafik yüklenemedi: {e}", image="")

        # Veritabanına Kaydet ve Geçmişi Yenile
        save_search(name, temp, desc)
        self.load_history()

    def update_ui_error(self, status, context):
        self.btn_search.configure(state="normal", text="Ara")
        self.lbl_city_name.configure(text="Hata Oluştu")
        
        if status == 404:
            messagebox.showerror("Hata", f"'{context}' şehri bulunamadı!")
        elif status == 401:
            messagebox.showerror("Hata", "Geçersiz API anahtarı. Yeniden deneyin.")
            save_api_key("")
            self.check_api_key()
        else:
            messagebox.showerror("Hata", f"Bir hata oluştu. Kodu: {status}")

if __name__ == "__main__":
    app = WeatherDashboard()
    app.mainloop()