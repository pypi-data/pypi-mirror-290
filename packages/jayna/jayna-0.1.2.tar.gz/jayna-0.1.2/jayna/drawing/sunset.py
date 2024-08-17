import matplotlib.pyplot as plt
import numpy as np
import random

def draw_classic_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.magma(Y)
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.3), 0.1, color='yellow', alpha=0.8)
    ax.add_artist(sun)
    ax.fill_between(x, 0, 0.3 + 0.1 * np.sin(10 * x), color='#2c3e50')
    ax.axhline(y=0.3, color='white', linestyle='--', alpha=0.5)
    ax.fill_between(x, 0, 0.3, color='#3498db', alpha=0.3)

def draw_palm_beach_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.YlOrRd(Y) 
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.2), 0.15, color='#FF4500', alpha=0.6)
    ax.add_artist(sun)
    
    def draw_palm(x, height):
        ax.add_artist(plt.Rectangle((x, 0), 0.02, height, color='black'))
        for angle in [-50, -25, 0, 25, 50]:
            ax.add_artist(plt.Polygon([(x, height), (x + 0.1 * np.cos(np.deg2rad(angle)), height + 0.1 * np.sin(np.deg2rad(angle)))], closed=False, color='black'))
    
    draw_palm(0.2, 0.4)
    draw_palm(0.8, 0.5)
    ax.fill_between(x, 0, 0.1 + 0.02 * np.sin(20 * x), color='#4169E1', alpha=0.6)

def draw_mountain_lake_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.coolwarm(Y)
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.6), 0.08, color='#FFD700', alpha=0.8)
    ax.add_artist(sun)
    
    def mountain(peak_height):
        return peak_height + 0.2 * np.random.random(100) - 0.1
    
    ax.fill_between(x, 0, mountain(0.5), color='#2F4F4F')
    ax.fill_between(x, 0, mountain(0.3), color='#3D5A5A')
    ax.fill_between(x, 0, 0.2, color='#4682B4', alpha=0.6)
    reflection = plt.Circle((0.5, 0.1), 0.06, color='#FFD700', alpha=0.4)
    ax.add_artist(reflection)

def draw_cityscape_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.plasma(Y)
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.4), 0.12, color='#FFA500', alpha=0.7)
    ax.add_artist(sun)
    
    for i in range(20):
        height = np.random.uniform(0.2, 0.6)
        width = np.random.uniform(0.03, 0.08)
        x_pos = np.random.uniform(0, 1)
        ax.add_artist(plt.Rectangle((x_pos, 0), width, height, color='black'))
        
    ax.fill_between(x, 0, 0.05, color='#696969')  # Road

def draw_desert_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.YlOrRd(Y)
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.2), 0.15, color='#FF6347', alpha=0.8)
    ax.add_artist(sun)
    
    # Sand dunes
    ax.fill_between(x, 0, 0.3 + 0.1 * np.sin(5 * x), color='#D2691E')
    ax.fill_between(x, 0, 0.2 + 0.05 * np.sin(8 * x), color='#8B4513')
    
    # Cactus
    ax.add_artist(plt.Rectangle((0.7, 0.2), 0.02, 0.2, color='#006400'))
    ax.add_artist(plt.Rectangle((0.68, 0.3), 0.06, 0.02, color='#006400'))

def draw_snowy_mountain_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.winter(Y)
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.7), 0.08, color='#FF69B4', alpha=0.6)
    ax.add_artist(sun)
    
    def snowy_mountain(peak_height):
        return peak_height + 0.2 * np.random.random(100) - 0.1
    
    ax.fill_between(x, 0, snowy_mountain(0.6), color='#F0F8FF')
    ax.fill_between(x, 0, snowy_mountain(0.4), color='#E6E6FA')
    ax.fill_between(x, 0, snowy_mountain(0.2), color='#B0E0E6')

def draw_stormy_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    storm_colors = plt.cm.gist_gray(Y)
    ax.imshow(storm_colors, extent=[0, 1, 0, 1], aspect='auto')
    
    # Sun peeking through clouds
    sun = plt.Circle((0.2, 0.6), 0.1, color='#FFA07A', alpha=0.4)
    ax.add_artist(sun)
    
    # Lightning
    for _ in range(3):
        start = np.random.uniform(0.4, 0.8)
        ax.plot([start, start + np.random.uniform(-0.1, 0.1)], 
                [1, np.random.uniform(0.4, 0.8)], color='yellow', linewidth=2, alpha=0.7)
    
    # Stormy sea
    ax.fill_between(x, 0, 0.3 + 0.05 * np.sin(20 * x), color='#4682B4', alpha=0.7)

def draw_tropical_island_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.twilight(Y)
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.3), 0.12, color='#FF4500', alpha=0.7)
    ax.add_artist(sun)
    
    # Island
    island = plt.Polygon([(0.3, 0), (0.7, 0), (0.6, 0.2), (0.4, 0.2)], color='#228B22')
    ax.add_artist(island)
    
    # Palm trees
    def draw_palm(x, height):
        ax.add_artist(plt.Rectangle((x, 0.2), 0.01, height, color='#8B4513'))
        for angle in [-60, -30, 0, 30, 60]:
            ax.add_artist(plt.Polygon([(x, 0.2 + height), (x + 0.05 * np.cos(np.deg2rad(angle)), 0.2 + height + 0.05 * np.sin(np.deg2rad(angle)))], closed=False, color='#228B22'))
    
    draw_palm(0.45, 0.1)
    draw_palm(0.55, 0.12)
    
    # Ocean
    ax.fill_between(x, 0, 0.2 + 0.02 * np.sin(10 * x), color='#4169E1', alpha=0.6)

def draw_arctic_sunset(ax):
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    sunset_colors = plt.cm.cool(Y)
    ax.imshow(sunset_colors, extent=[0, 1, 0, 1], aspect='auto')
    sun = plt.Circle((0.5, 0.8), 0.07, color='#FFB6C1', alpha=0.6)
    ax.add_artist(sun)
    
    # Ice
    ax.fill_between(x, 0, 0.4 + 0.05 * np.sin(8 * x), color='white')
    ax.fill_between(x, 0, 0.3 + 0.03 * np.sin(12 * x), color='#F0FFFF')
    
    # Polar bear silhouette
    bear = plt.Polygon([(0.6, 0.4), (0.7, 0.4), (0.75, 0.45), (0.7, 0.5), (0.65, 0.5), (0.6, 0.45)], color='black')
    ax.add_artist(bear)

def draw_sunset():
    fig, ax = plt.subplots(figsize=(10, 6))
    sunset_functions = [
        draw_classic_sunset,
        draw_palm_beach_sunset,
        draw_mountain_lake_sunset,
        draw_cityscape_sunset,
        draw_desert_sunset,
        draw_snowy_mountain_sunset,
        draw_stormy_sunset,
        draw_tropical_island_sunset,
        draw_arctic_sunset
    ]
    random.choice(sunset_functions)(ax)
    ax.axis('off')
    plt.show()

# Example usage
draw_sunset()