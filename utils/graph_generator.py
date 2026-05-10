import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
from PIL import Image

def generate_forecast_graph(forecast_data):
    """
    OpenWeatherMap 5 günlük (3 saatlik) tahmin verisini alıp 
    PIL Image olarak dönen bir fonksiyon.
    """
    times = []
    temps = []
    
    # API'den gelen listedeki verileri ayıklayalım
    for item in forecast_data['list']:
        dt = datetime.fromtimestamp(item['dt'])
        times.append(dt)
        temps.append(item['main']['temp'])
        
    # Sadece ilk 24 saati (veya 48 saati) gösterelim ki grafik çok sıkışık olmasın.
    # Her gün 8 veri var. 2 günlük = 16 veri.
    limit = min(16, len(times))
    times = times[:limit]
    temps = temps[:limit]

    # Grafiği çiz
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    fig.patch.set_facecolor('#2b2b2b') # CustomTkinter dark mode ile uyumlu arka plan
    ax.set_facecolor('#2b2b2b')
    
    ax.plot(times, temps, marker='o', color='#0AC8B9', linewidth=2, markersize=5)
    
    # Eksenleri düzenle
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%a'))
    ax.tick_params(axis='x', colors='white', labelsize=8)
    ax.tick_params(axis='y', colors='white', labelsize=8)
    
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('none') 
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5, axis='y')
    
    plt.title("Önümüzdeki 48 Saatin Sıcaklık Trendi", color='white', pad=10, fontsize=10)
    plt.tight_layout()

    # PIL Image'a dönüştür
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), transparent=True)
    buf.seek(0)
    img = Image.open(buf)
    
    # Hafıza sızıntısı olmaması için plot'u kapat
    plt.close(fig)
    return img
