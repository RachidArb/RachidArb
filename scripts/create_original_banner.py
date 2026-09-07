import math
from PIL import Image, ImageDraw, ImageFont

def draw_banner(mode='dark', output_path='art/header-dark.png', width=2400, height=600):
    scale = 2
    W, H = width * scale, height * scale

    if mode == 'dark':
        bg_main = (10, 13, 20)        # #0A0D14 Deep obsidian
        bg_sec  = (13, 18, 30)        # #0D121E Subtle navy charcoal
        
        dot_color = (70, 90, 125, 60) # Micro-dots for background texture
        
        text_name = (255, 255, 255)
        text_title = (56, 189, 248)   # #38BDF8 Electric Cyan
        text_tagline = (160, 175, 200) # Crisp readable slate
        text_mono = (148, 163, 184)   # #94A3B8
        
        node_bg = (15, 23, 42, 240)
        node_border = (51, 65, 85, 240)
        
        accent_cyan = (56, 189, 248)
        accent_green = (16, 185, 129)
        accent_amber = (245, 158, 11)
        accent_purple = (168, 85, 247)
        accent_blue = (59, 130, 246)
        
        line_base = (56, 189, 248, 100)
    else:
        bg_main = (250, 252, 255)     # #FAFCFF Pristine Slate
        bg_sec  = (241, 245, 249)     # #F1F5F9 Soft Architectural Gray
        
        dot_color = (180, 195, 215, 80)
        
        text_name = (15, 23, 42)      # #0F172A Deep Navy
        text_title = (2, 132, 199)    # #0284C7 Strong Royal Azure
        text_tagline = (51, 65, 85)   # #334155 Slate
        text_mono = (71, 85, 105)     # #475569
        
        node_bg = (255, 255, 255, 250)
        node_border = (203, 213, 225, 250)
        
        accent_cyan = (2, 132, 199)
        accent_green = (5, 150, 105)
        accent_amber = (217, 119, 6)
        accent_purple = (126, 34, 206)
        accent_blue = (29, 78, 216)
        
        line_base = (2, 132, 199, 80)

    # 1. Base Gradient Canvas
    img = Image.new('RGBA', (W, H), bg_main)
    draw = ImageDraw.Draw(img)

    for y in range(H):
        t = y / H
        r = int(bg_main[0] * (1 - t) + bg_sec[0] * t)
        g = int(bg_main[1] * (1 - t) + bg_sec[1] * t)
        b = int(bg_main[2] * (1 - t) + bg_sec[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # 2. Ambient Light Flares (Sophisticated backlighting)
    ambient = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(ambient)
    
    # Left soft ambient glow (Cyan)
    for r in range(300 * scale, 0, -12):
        alpha = int(14 * (1 - r / (300 * scale)))
        c = (accent_cyan[0], accent_cyan[1], accent_cyan[2], alpha)
        a_draw.ellipse([200 * scale - r, 300 * scale - r, 200 * scale + r, 300 * scale + r], fill=c)

    # Right soft ambient glow (Emerald + Cyan for Architecture)
    for r in range(450 * scale, 0, -15):
        alpha = int(16 * (1 - r / (450 * scale)))
        c = (accent_green[0], accent_green[1], accent_green[2], alpha) if mode == 'dark' else (accent_cyan[0], accent_cyan[1], accent_cyan[2], alpha // 2)
        a_draw.ellipse([W - 600 * scale - r, 300 * scale - r, W - 600 * scale + r, 300 * scale + r], fill=c)
        
    img = Image.alpha_composite(img, ambient)
    draw = ImageDraw.Draw(img)

    # 3. Modern Micro-Dot Matrix Background (Non-distracting, clean texture)
    dot_step = 40 * scale
    for x in range(30 * scale, W, dot_step):
        for y in range(30 * scale, H, dot_step):
            draw.rectangle([x - 1 * scale, y - 1 * scale, x + 1 * scale, y + 1 * scale], fill=dot_color)

    # Fonts
    f_telemetry = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 14 * scale)
    f_name = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 94 * scale)
    f_title = ImageFont.truetype("C:/Windows/Fonts/segoeuiz.ttf", 36 * scale)
    f_tagline = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 25 * scale)
    f_pill = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 13 * scale)
    f_node_cat = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 12 * scale)
    f_node_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18 * scale)
    f_node_desc = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13 * scale)

    # 4. Left Personal Branding
    start_x = 120 * scale
    start_y = 110 * scale

    # Telemetry Badge Box
    tele_text = "ENTERPRISE ARCHITECTURE // FULL-STACK SYSTEMS"
    bbox_t = draw.textbbox((0, 0), tele_text, font=f_telemetry)
    t_w = bbox_t[2] - bbox_t[0]
    t_h = bbox_t[3] - bbox_t[1]
    
    badge_pad_x = 14 * scale
    badge_pad_y = 6 * scale
    badge_w = t_w + badge_pad_x * 2 + 16 * scale
    badge_h = t_h + badge_pad_y * 2
    
    # Draw badge frame
    draw.rounded_rectangle([start_x, start_y, start_x + badge_w, start_y + badge_h], radius=4 * scale, fill=node_bg, outline=node_border, width=1 * scale)
    
    # Pulsing dot
    dot_x = start_x + 12 * scale
    dot_y = start_y + badge_h // 2
    draw.ellipse([dot_x - 6 * scale, dot_y - 6 * scale, dot_x + 6 * scale, dot_y + 6 * scale], fill=(accent_green[0], accent_green[1], accent_green[2], 50))
    draw.ellipse([dot_x - 3 * scale, dot_y - 3 * scale, dot_x + 3 * scale, dot_y + 3 * scale], fill=accent_green)
    draw.text((start_x + 24 * scale, start_y + badge_pad_y - 1 * scale), tele_text, font=f_telemetry, fill=text_mono)

    # Name: Rachid
    name_y = start_y + 40 * scale
    draw.text((start_x, name_y), "Rachid", font=f_name, fill=text_name)

    # Title: Java Full-Stack Software Engineer
    title_y = name_y + 115 * scale
    draw.text((start_x, title_y), "Java Full-Stack Software Engineer", font=f_title, fill=text_title)

    # Tagline: Building secure, tested, maintainable software
    tagline_y = title_y + 54 * scale
    draw.text((start_x, tagline_y), "Building secure, tested, maintainable software", font=f_tagline, fill=text_tagline)

    # Technology Stack Badges
    pipeline_y = tagline_y + 60 * scale
    pills = [
        ("JAVA 21 LTS", accent_amber),
        ("SPRING BOOT 3", accent_green),
        ("REST APIS", accent_cyan),
        ("POSTGRESQL", accent_blue),
        ("CLEAN ARCHITECTURE", accent_purple),
        ("AUTOMATED TESTING", accent_green),
        ("DOCKER", accent_cyan)
    ]

    px = start_x
    for i, (label, accent) in enumerate(pills):
        bbox = draw.textbbox((0, 0), label, font=f_pill)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        pad_h = 10 * scale
        pad_v = 6 * scale
        box_w = lw + pad_h * 2 + 8 * scale
        box_h = lh + pad_v * 2

        draw.rounded_rectangle([px, pipeline_y, px + box_w, pipeline_y + box_h], radius=5 * scale, fill=node_bg, outline=node_border, width=1 * scale)
        draw.ellipse([px + 8 * scale, pipeline_y + box_h // 2 - 3 * scale, px + 14 * scale, pipeline_y + box_h // 2 + 3 * scale], fill=accent)
        draw.text((px + 18 * scale, pipeline_y + pad_v - 1 * scale), label, font=f_pill, fill=text_name)
        px += box_w + 8 * scale

    # 5. Right Side: The Systems Architecture Blueprint
    arch_start_x = int(W * 0.52)
    col_w = 215 * scale
    card_h = 76 * scale
    col_gap = 26 * scale
    row_gap = 48 * scale
    
    row1_y = 145 * scale
    row2_y = row1_y + card_h + row_gap
    
    col1_x = arch_start_x
    col2_x = col1_x + col_w + col_gap
    col3_x = col2_x + col_w + col_gap
    
    nodes = [
        (col1_x, row1_y, "CLIENT TIER", "React 18 · TypeScript", "Vite · Tailwind SPA", accent_cyan),
        (col2_x, row1_y, "SECURITY PERIMETER", "Stateless JWT Auth", "BCrypt · Security Filter", accent_amber),
        (col3_x, row1_y, "APPLICATION CORE", "Spring Boot 3.3.5", "Domain Services · REST", accent_green),
        
        (col1_x, row2_y, "PERSISTENCE TIER", "PostgreSQL 16", "Flyway Migrations · JPA", accent_blue),
        (col2_x, row2_y, "VERIFICATION HARNESS", "114 Automated Tests", "Mockito · MockMvc · 100%", accent_green),
        (col3_x, row2_y, "CONTAINER & CI", "Docker & Compose", "GitHub Actions Pipeline", accent_cyan),
    ]

    # Draw Inter-Node Data Bus Lines
    bus = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bus)
    
    # Row 1 bus
    y_mid1 = row1_y + card_h // 2
    bdraw.line([(col1_x + col_w, y_mid1), (col2_x, y_mid1)], fill=line_base, width=2 * scale)
    bdraw.line([(col2_x + col_w, y_mid1), (col3_x, y_mid1)], fill=line_base, width=2 * scale)
    
    p1 = (col1_x + col_w + col2_x) // 2
    p2 = (col2_x + col_w + col3_x) // 2
    bdraw.ellipse([p1 - 4 * scale, y_mid1 - 4 * scale, p1 + 4 * scale, y_mid1 + 4 * scale], fill=accent_cyan)
    bdraw.ellipse([p2 - 4 * scale, y_mid1 - 4 * scale, p2 + 4 * scale, y_mid1 + 4 * scale], fill=accent_green)

    # Row 2 bus
    y_mid2 = row2_y + card_h // 2
    bdraw.line([(col1_x + col_w, y_mid2), (col2_x, y_mid2)], fill=line_base, width=2 * scale)
    bdraw.line([(col2_x + col_w, y_mid2), (col3_x, y_mid2)], fill=line_base, width=2 * scale)
    
    p3 = (col1_x + col_w + col2_x) // 2
    p4 = (col2_x + col_w + col3_x) // 2
    bdraw.ellipse([p3 - 4 * scale, y_mid2 - 4 * scale, p3 + 4 * scale, y_mid2 + 4 * scale], fill=accent_blue)
    bdraw.ellipse([p4 - 4 * scale, y_mid2 - 4 * scale, p4 + 4 * scale, y_mid2 + 4 * scale], fill=accent_green)

    # Vertical cross-connections
    bdraw.line([(col1_x + col_w // 2, row1_y + card_h), (col1_x + col_w // 2, row2_y)], fill=line_base, width=1 * scale)
    bdraw.line([(col2_x + col_w // 2, row1_y + card_h), (col2_x + col_w // 2, row2_y)], fill=line_base, width=1 * scale)
    bdraw.line([(col3_x + col_w // 2, row1_y + card_h), (col3_x + col_w // 2, row2_y)], fill=line_base, width=1 * scale)

    img = Image.alpha_composite(img, bus)

    # Draw Architecture Node Cards
    for (nx, ny, n_cat, n_title, n_desc, n_acc) in nodes:
        node_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ndraw = ImageDraw.Draw(node_layer)
        
        # Rounded card background
        ndraw.rounded_rectangle([nx, ny, nx + col_w, ny + card_h], radius=7 * scale, fill=node_bg, outline=node_border, width=1 * scale)
        # Left accent pill
        ndraw.rounded_rectangle([nx, ny, nx + 4 * scale, ny + card_h], radius=2 * scale, fill=n_acc)
        # Category Micro-Header
        ndraw.text((nx + 14 * scale, ny + 9 * scale), n_cat, font=f_node_cat, fill=text_mono)
        # Node Title
        ndraw.text((nx + 14 * scale, ny + 28 * scale), n_title, font=f_node_title, fill=text_name)
        # Node Subtext
        ndraw.text((nx + 14 * scale, ny + 51 * scale), n_desc, font=f_node_desc, fill=text_tagline)
        # Status pulse
        dot_cx = nx + col_w - 14 * scale
        dot_cy = ny + 15 * scale
        ndraw.ellipse([dot_cx - 3 * scale, dot_cy - 3 * scale, dot_cx + 3 * scale, dot_cy + 3 * scale], fill=n_acc)
        
        img = Image.alpha_composite(img, node_layer)

    # Status Telemetry Bar at bottom of architecture
    trace_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(trace_layer)
    code_text = "STATUS: OPERATIONAL  //  VERIFIED END-TO-END  //  DEFENSE-IN-DEPTH"
    tdraw.text((arch_start_x, row2_y + card_h + 18 * scale), code_text, font=f_pill, fill=text_mono)
    img = Image.alpha_composite(img, trace_layer)

    # 6. Downsample to target resolution with Lanczos
    final_img = img.resize((width, height), Image.Resampling.LANCZOS)
    final_img.save(output_path, 'PNG', optimize=True)
    print(f"Refined {mode} banner saved to {output_path} ({width}x{height})")

if __name__ == '__main__':
    draw_banner('dark', 'art/header-dark.png', 2400, 600)
    draw_banner('light', 'art/header-light.png', 2400, 600)
    draw_banner('dark', 'art/social-media-dark.png', 1200, 630)
    
    # Sync to assets/
    draw_banner('dark', 'assets/header-dark.png', 2400, 600)
    draw_banner('light', 'assets/header-light.png', 2400, 600)
    draw_banner('dark', 'assets/social-media-dark.png', 1200, 630)
