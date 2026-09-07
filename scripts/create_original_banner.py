import math
from PIL import Image, ImageDraw, ImageFont

def draw_banner(mode='dark', output_path='art/header-dark.png', width=2000, height=750):
    # 2x supersampling for razor-sharp rendering
    scale = 2
    W, H = width * scale, height * scale

    if mode == 'dark':
        bg_main = (10, 14, 23)        # #0A0E17 Deep Obsidian Slate
        bg_sec  = (15, 23, 42)        # #0F172A Charcoal Navy
        
        dot_color = (70, 95, 135, 75) # Subtle blueprint micro-dots
        
        text_name = (255, 255, 255)   # #FFFFFF Crisp White
        text_title = (56, 189, 248)   # #38BDF8 Electric Azure
        text_tagline = (165, 185, 215) # High-legibility Slate
        text_mono = (148, 163, 184)   # #94A3B8
        
        node_bg = (15, 23, 42, 245)
        node_border = (60, 80, 110, 255)
        
        accent_cyan = (56, 189, 248)
        accent_green = (16, 185, 129)
        accent_amber = (245, 158, 11)
        accent_purple = (168, 85, 247)
        accent_blue = (59, 130, 246)
        
        line_base = (56, 189, 248, 150)
    else:
        bg_main = (250, 252, 255)     # #FAFCFF Pristine Slate White
        bg_sec  = (241, 245, 249)     # #F1F5F9 Soft Pearl
        
        dot_color = (180, 195, 215, 95)
        
        text_name = (15, 23, 42)      # #0F172A Deep Navy
        text_title = (2, 132, 199)    # #0284C7 Strong Azure
        text_tagline = (51, 65, 85)   # #334155 Slate
        text_mono = (71, 85, 105)     # #475569
        
        node_bg = (255, 255, 255, 250)
        node_border = (185, 200, 220, 255)
        
        accent_cyan = (2, 132, 199)
        accent_green = (5, 150, 105)
        accent_amber = (217, 119, 6)
        accent_purple = (126, 34, 206)
        accent_blue = (29, 78, 216)
        
        line_base = (2, 132, 199, 120)

    # 1. Base Gradient Canvas
    img = Image.new('RGBA', (W, H), bg_main)
    draw = ImageDraw.Draw(img)

    for y in range(H):
        t = y / H
        r = int(bg_main[0] * (1 - t) + bg_sec[0] * t)
        g = int(bg_main[1] * (1 - t) + bg_sec[1] * t)
        b = int(bg_main[2] * (1 - t) + bg_sec[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # 2. Ambient Light Glows
    ambient = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(ambient)
    
    # Left Ambient (Cyan behind branding)
    for r in range(350 * scale, 0, -15):
        alpha = int(18 * (1 - r / (350 * scale)))
        c = (accent_cyan[0], accent_cyan[1], accent_cyan[2], alpha)
        a_draw.ellipse([220 * scale - r, 380 * scale - r, 220 * scale + r, 380 * scale + r], fill=c)

    # Right Ambient (Emerald & Cyan behind architecture)
    for r in range(500 * scale, 0, -18):
        alpha = int(22 * (1 - r / (500 * scale)))
        c = (accent_green[0], accent_green[1], accent_green[2], alpha) if mode == 'dark' else (accent_cyan[0], accent_cyan[1], accent_cyan[2], alpha // 2)
        a_draw.ellipse([W - 480 * scale - r, 380 * scale - r, W - 480 * scale + r, 380 * scale + r], fill=c)
        
    img = Image.alpha_composite(img, ambient)
    draw = ImageDraw.Draw(img)

    # 3. Micro-Dot Matrix Background
    dot_step = 42 * scale
    for x in range(25 * scale, W, dot_step):
        for y in range(25 * scale, H, dot_step):
            draw.rectangle([x - 1 * scale, y - 1 * scale, x + 1 * scale, y + 1 * scale], fill=dot_color)

    # 4. High-Legibility Scaled Typography
    font_mono_bold = "C:/Windows/Fonts/consolab.ttf"
    font_bold = "C:/Windows/Fonts/segoeuib.ttf"
    font_semi = "C:/Windows/Fonts/segoeuiz.ttf"
    font_reg = "C:/Windows/Fonts/segoeui.ttf"

    f_telemetry = ImageFont.truetype(font_mono_bold, 17 * scale)
    f_name = ImageFont.truetype(font_bold, 126 * scale)        # Huge, commanding name
    f_title = ImageFont.truetype(font_semi, 44 * scale)        # Bold, clear title
    f_tagline = ImageFont.truetype(font_reg, 30 * scale)       # Crisp philosophy
    f_pill = ImageFont.truetype(font_mono_bold, 16 * scale)    # Legible technology chips
    
    f_node_cat = ImageFont.truetype(font_mono_bold, 14 * scale)
    f_node_title = ImageFont.truetype(font_bold, 24 * scale)   # Large node titles
    f_node_desc = ImageFont.truetype(font_reg, 17 * scale)     # Clear subtitles
    f_status = ImageFont.truetype(font_mono_bold, 16 * scale)

    # 5. Left Personal Branding
    start_x = 90 * scale
    start_y = 100 * scale

    # Telemetry Badge Box
    tele_text = "ENTERPRISE ARCHITECTURE  //  FULL-STACK SYSTEMS"
    bbox_t = draw.textbbox((0, 0), tele_text, font=f_telemetry)
    badge_pad_x = 18 * scale
    badge_pad_y = 9 * scale
    badge_w = (bbox_t[2] - bbox_t[0]) + badge_pad_x * 2 + 20 * scale
    badge_h = (bbox_t[3] - bbox_t[1]) + badge_pad_y * 2
    
    draw.rounded_rectangle([start_x, start_y, start_x + badge_w, start_y + badge_h], radius=6 * scale, fill=node_bg, outline=node_border, width=int(1.5 * scale))
    
    # Pulse dot
    dot_x = start_x + 16 * scale
    dot_y = start_y + badge_h // 2
    draw.ellipse([dot_x - 8 * scale, dot_y - 8 * scale, dot_x + 8 * scale, dot_y + 8 * scale], fill=(accent_green[0], accent_green[1], accent_green[2], 50))
    draw.ellipse([dot_x - 4 * scale, dot_y - 4 * scale, dot_x + 4 * scale, dot_y + 4 * scale], fill=accent_green)
    draw.text((start_x + 32 * scale, start_y + badge_pad_y - 1 * scale), tele_text, font=f_telemetry, fill=text_mono)

    # Name: Rachid
    name_y = start_y + 46 * scale
    draw.text((start_x, name_y), "Rachid", font=f_name, fill=text_name)

    # Title: Java Full-Stack Software Engineer
    title_y = name_y + 150 * scale
    draw.text((start_x, title_y), "Java Full-Stack Software Engineer", font=f_title, fill=text_title)

    # Tagline: Building secure, tested, maintainable software
    tagline_y = title_y + 68 * scale
    draw.text((start_x, tagline_y), "Building secure, tested, maintainable software", font=f_tagline, fill=text_tagline)

    # Technology Stack Badges (2 Rows for large, highly visible badges)
    row1_pills = [
        ("JAVA 21 LTS", accent_amber),
        ("SPRING BOOT 3", accent_green),
        ("REST APIS", accent_cyan),
        ("POSTGRESQL", accent_blue),
    ]
    row2_pills = [
        ("CLEAN ARCHITECTURE", accent_purple),
        ("114 AUTOMATED TESTS", accent_green),
        ("DOCKER & CI/CD", accent_cyan),
    ]

    pills_start_y = tagline_y + 75 * scale
    
    for row_idx, pill_row in enumerate([row1_pills, row2_pills]):
        curr_y = pills_start_y + row_idx * (46 * scale)
        px = start_x
        for label, accent in pill_row:
            bbox = draw.textbbox((0, 0), label, font=f_pill)
            lw = bbox[2] - bbox[0]
            lh = bbox[3] - bbox[1]
            pad_h = 14 * scale
            pad_v = 8 * scale
            box_w = lw + pad_h * 2 + 10 * scale
            box_h = lh + pad_v * 2

            draw.rounded_rectangle([px, curr_y, px + box_w, curr_y + box_h], radius=6 * scale, fill=node_bg, outline=node_border, width=int(1.5 * scale))
            draw.ellipse([px + 10 * scale, curr_y + box_h // 2 - 4 * scale, px + 18 * scale, curr_y + box_h // 2 + 4 * scale], fill=accent)
            draw.text((px + 24 * scale, curr_y + pad_v - 1 * scale), label, font=f_pill, fill=text_name)
            px += box_w + 12 * scale

    # 6. Right Side: Big, Bold 6-Node Enterprise Architecture Schematic
    arch_start_x = int(W * 0.49)
    col_w = 295 * scale
    card_h = 115 * scale
    col_gap = 35 * scale
    row_gap = 60 * scale
    
    row1_y = 140 * scale
    row2_y = row1_y + card_h + row_gap
    
    col1_x = arch_start_x
    col2_x = col1_x + col_w + col_gap
    col3_x = col2_x + col_w + col_gap
    
    nodes = [
        (col1_x, row1_y, "CLIENT TIER", "React 18 · TypeScript", "Vite · Responsive SPA", accent_cyan),
        (col2_x, row1_y, "SECURITY PERIMETER", "Stateless JWT Auth", "BCrypt · Filter Chains", accent_amber),
        (col3_x, row1_y, "APPLICATION CORE", "Spring Boot 3.3.5", "Domain Services · REST APIs", accent_green),
        
        (col1_x, row2_y, "PERSISTENCE TIER", "PostgreSQL 16", "Flyway Migrations · JPA", accent_blue),
        (col2_x, row2_y, "QUALITY HARNESS", "114 Automated Tests", "Mockito · MockMvc · 100%", accent_green),
        (col3_x, row2_y, "DEPLOYMENT & CI", "Docker & Compose", "GitHub Actions Pipeline", accent_cyan),
    ]

    # Draw Inter-Node Data Bus Lines
    bus = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bus)
    
    # Row 1 Horizontal Bus
    y_mid1 = row1_y + card_h // 2
    bdraw.line([(col1_x + col_w, y_mid1), (col2_x, y_mid1)], fill=line_base, width=3 * scale)
    bdraw.line([(col2_x + col_w, y_mid1), (col3_x, y_mid1)], fill=line_base, width=3 * scale)
    
    p1 = (col1_x + col_w + col2_x) // 2
    p2 = (col2_x + col_w + col3_x) // 2
    bdraw.ellipse([p1 - 5 * scale, y_mid1 - 5 * scale, p1 + 5 * scale, y_mid1 + 5 * scale], fill=accent_cyan)
    bdraw.ellipse([p2 - 5 * scale, y_mid1 - 5 * scale, p2 + 5 * scale, y_mid1 + 5 * scale], fill=accent_green)

    # Row 2 Horizontal Bus
    y_mid2 = row2_y + card_h // 2
    bdraw.line([(col1_x + col_w, y_mid2), (col2_x, y_mid2)], fill=line_base, width=3 * scale)
    bdraw.line([(col2_x + col_w, y_mid2), (col3_x, y_mid2)], fill=line_base, width=3 * scale)
    
    p3 = (col1_x + col_w + col2_x) // 2
    p4 = (col2_x + col_w + col3_x) // 2
    bdraw.ellipse([p3 - 5 * scale, y_mid2 - 5 * scale, p3 + 5 * scale, y_mid2 + 5 * scale], fill=accent_blue)
    bdraw.ellipse([p4 - 5 * scale, y_mid2 - 5 * scale, p4 + 5 * scale, y_mid2 + 5 * scale], fill=accent_green)

    # Vertical cross-connections
    bdraw.line([(col1_x + col_w // 2, row1_y + card_h), (col1_x + col_w // 2, row2_y)], fill=line_base, width=2 * scale)
    bdraw.line([(col2_x + col_w // 2, row1_y + card_h), (col2_x + col_w // 2, row2_y)], fill=line_base, width=2 * scale)
    bdraw.line([(col3_x + col_w // 2, row1_y + card_h), (col3_x + col_w // 2, row2_y)], fill=line_base, width=2 * scale)

    img = Image.alpha_composite(img, bus)

    # Draw Architecture Node Cards
    for (nx, ny, n_cat, n_title, n_desc, n_acc) in nodes:
        node_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ndraw = ImageDraw.Draw(node_layer)
        
        # Rounded card background
        ndraw.rounded_rectangle([nx, ny, nx + col_w, ny + card_h], radius=10 * scale, fill=node_bg, outline=node_border, width=int(1.5 * scale))
        # Left accent pill
        ndraw.rounded_rectangle([nx, ny, nx + 6 * scale, ny + card_h], radius=3 * scale, fill=n_acc)
        # Category Micro-Header
        ndraw.text((nx + 20 * scale, ny + 14 * scale), n_cat, font=f_node_cat, fill=text_mono)
        # Node Title
        ndraw.text((nx + 20 * scale, ny + 38 * scale), n_title, font=f_node_title, fill=text_name)
        # Node Subtext
        ndraw.text((nx + 20 * scale, ny + 74 * scale), n_desc, font=f_node_desc, fill=text_tagline)
        # Status pulse
        dot_cx = nx + col_w - 20 * scale
        dot_cy = ny + 22 * scale
        ndraw.ellipse([dot_cx - 5 * scale, dot_cy - 5 * scale, dot_cx + 5 * scale, dot_cy + 5 * scale], fill=n_acc)
        
        img = Image.alpha_composite(img, node_layer)

    # Status Telemetry Bar at bottom of architecture
    trace_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(trace_layer)
    code_text = "STATUS: OPERATIONAL  //  VERIFIED END-TO-END  //  CLEAN ARCHITECTURE"
    tdraw.text((arch_start_x, row2_y + card_h + 24 * scale), code_text, font=f_status, fill=text_mono)
    img = Image.alpha_composite(img, trace_layer)

    # 7. Downsample with Lanczos
    final_img = img.resize((width, height), Image.Resampling.LANCZOS)
    final_img.save(output_path, 'PNG', optimize=True)
    print(f"High-impact {mode} banner saved to {output_path} ({width}x{height})")

if __name__ == '__main__':
    # 2000x750 provides ~2.67:1 ratio (50% taller and significantly larger in GitHub's container)
    draw_banner('dark', 'art/header-dark.png', 2000, 750)
    draw_banner('light', 'art/header-light.png', 2000, 750)
    draw_banner('dark', 'art/social-media-dark.png', 1200, 630)
    
    # Sync to assets/
    draw_banner('dark', 'assets/header-dark.png', 2000, 750)
    draw_banner('light', 'assets/header-light.png', 2000, 750)
    draw_banner('dark', 'assets/social-media-dark.png', 1200, 630)
