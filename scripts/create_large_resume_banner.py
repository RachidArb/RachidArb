import math
from PIL import Image, ImageDraw, ImageFont

def draw_large_resume_banner(mode='dark', output_path='art/header-dark.png', width=2000, height=750):
    scale = 2
    W, H = width * scale, height * scale

    if mode == 'dark':
        bg_0 = (6, 9, 15)          # #06090F Deepest Obsidian
        bg_1 = (10, 15, 25)        # #0A0F19 Technical Navy
        bg_2 = (14, 21, 35)        # #0E1523 Slate Charcoal
        
        dot_color = (56, 189, 248, 25) # Soft cyber micro-dots
        grid_line = (30, 45, 68, 18)   # Ultra-faint grid
        
        hud_bg = (11, 17, 28, 245)
        hud_border = (40, 60, 95, 230)
        hud_header_bg = (16, 25, 42, 255)
        
        c_cyan = (0, 229, 255)      # #00E5FF Electric Cyan
        c_blue = (59, 130, 246)     # #3B82F6 Neon Blue
        c_purple = (168, 85, 247)   # #A855F7 Cyber Violet
        c_green = (16, 185, 129)    # #10B981 Emerald Neon
        c_amber = (245, 158, 11)    # #F59E0B Java Amber
        
        t_white = (255, 255, 255)
        t_cyan = (56, 189, 248)
        t_slate = (226, 232, 240)
        t_muted = (148, 163, 184)
        t_dim = (100, 116, 139)
        code_dim = (56, 189, 248, 24)
    else:
        bg_0 = (248, 250, 253)
        bg_1 = (241, 245, 250)
        bg_2 = (235, 240, 248)
        
        dot_color = (2, 132, 199, 30)
        grid_line = (210, 220, 235, 50)
        
        hud_bg = (255, 255, 255, 245)
        hud_border = (195, 210, 230, 240)
        hud_header_bg = (240, 245, 252, 255)
        
        c_cyan = (2, 132, 199)
        c_blue = (29, 78, 216)
        c_purple = (126, 34, 206)
        c_green = (5, 150, 105)
        c_amber = (217, 119, 6)
        
        t_white = (15, 23, 42)
        t_cyan = (2, 132, 199)
        t_slate = (51, 65, 85)
        t_muted = (71, 85, 105)
        t_dim = (100, 116, 139)
        code_dim = (2, 132, 199, 18)

    # 1. Base Gradient Canvas
    img = Image.new('RGBA', (W, H), bg_0)
    draw = ImageDraw.Draw(img)

    for y in range(H):
        t = y / H
        if t < 0.5:
            f = t / 0.5
            r = int(bg_0[0] * (1 - f) + bg_1[0] * f)
            g = int(bg_0[1] * (1 - f) + bg_1[1] * f)
            b = int(bg_0[2] * (1 - f) + bg_1[2] * f)
        else:
            f = (t - 0.5) / 0.5
            r = int(bg_1[0] * (1 - f) + bg_2[0] * f)
            g = int(bg_1[1] * (1 - f) + bg_2[1] * f)
            b = int(bg_1[2] * (1 - f) + bg_2[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # 2. Ambient Glowing Flares (Focused behind the text & architecture)
    bloom = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bloom)
    
    # Large central glow behind RACHID
    for r in range(450 * scale, 0, -15):
        a = int(18 * (1 - r / (450 * scale)))
        col = (c_cyan[0], c_cyan[1], c_cyan[2], a) if mode == 'dark' else (c_cyan[0], c_cyan[1], c_cyan[2], a // 2)
        bdraw.ellipse([450 * scale - r, 300 * scale - r, 450 * scale + r, 300 * scale + r], fill=col)

    # Right side architectural glow (Purple/Violet & Cyan)
    for r in range(500 * scale, 0, -18):
        a = int(22 * (1 - r / (500 * scale)))
        col = (c_purple[0], c_purple[1], c_purple[2], a) if mode == 'dark' else (c_blue[0], c_blue[1], c_blue[2], a // 2)
        bdraw.ellipse([W - 400 * scale - r, 380 * scale - r, W - 400 * scale + r, 380 * scale + r], fill=col)
        
    img = Image.alpha_composite(img, bloom)
    draw = ImageDraw.Draw(img)

    # 3. Micro-Dot Matrix Background (Subtle Texture)
    dot_step = 45 * scale
    for x in range(30 * scale, W, dot_step):
        for y in range(30 * scale, H, dot_step):
            draw.rectangle([x - 1 * scale, y - 1 * scale, x + 1 * scale, y + 1 * scale], fill=dot_color)

    # 4. Background Code & Watermark (Java Architecture)
    code_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(code_layer)
    f_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14 * scale)
    code_lines = [
        "@RestController",
        "@RequestMapping(\"/api/v1/tasks\")",
        "public class EnterpriseTaskController {",
        "    private final TaskService taskService;",
        "    @PreAuthorize(\"hasRole('ADMIN')\")",
        "    @PostMapping(\"/execute\")",
        "    public ResponseEntity<TaskResponse> dispatch(@Valid @RequestBody TaskRequest req) {",
        "        return ResponseEntity.ok(taskService.process(req));",
        "    }",
        "}",
        "// DATA_BUS: 0x7F // PROTOCOL: TCP/IP // HIKARICP POOL: ACTIVE // FLYWAY: OK"
    ]
    for idx, line in enumerate(code_lines):
        cdraw.text((int(W * 0.44), 95 * scale + idx * 24 * scale), line, font=f_code, fill=code_dim)
    img = Image.alpha_composite(img, code_layer)
    draw = ImageDraw.Draw(img)

    # 5. Fonts Setup — MASSIVE, COMMANDING TYPOGRAPHY
    f_mono_hdr = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 15 * scale)
    f_tag = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 18 * scale)
    f_name = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 155 * scale)       # HUGE 155pt name!
    f_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 46 * scale)      # 46pt Bold Job Title
    f_pillars = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 26 * scale)    # 26pt BACKEND • SECURITY • TESTING
    f_tagline = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 26 * scale)     # 26pt Philosophy
    f_spec_hdr = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 14 * scale)
    f_spec_val = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15 * scale)
    f_spec_key = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13 * scale)
    f_node_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18 * scale)
    f_node_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13 * scale)
    f_node_num = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 12 * scale)

    # 6. Futuristic Digital Résumé HUD Frame
    hud_top = 40 * scale
    hud_bot = H - 40 * scale
    hud_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(hud_layer)

    # Outer Frame
    hdraw.rounded_rectangle([50 * scale, hud_top, W - 50 * scale, hud_bot], radius=14 * scale, outline=hud_border, width=int(1.5 * scale))
    
    # Top HUD Bar
    hdraw.rounded_rectangle([50 * scale, hud_top, W - 50 * scale, hud_top + 46 * scale], radius=14 * scale, fill=hud_header_bg)
    hdraw.rectangle([50 * scale, hud_top + 24 * scale, W - 50 * scale, hud_top + 46 * scale], fill=hud_header_bg)
    hdraw.line([(50 * scale, hud_top + 46 * scale), (W - 50 * scale, hud_top + 46 * scale)], fill=hud_border, width=1 * scale)

    # Window Controls (Cyan, Violet, Green)
    dots = [c_cyan, c_purple, c_green]
    for i, dc in enumerate(dots):
        cx = 80 * scale + i * 22 * scale
        cy = hud_top + 23 * scale
        hdraw.ellipse([cx - 5 * scale, cy - 5 * scale, cx + 5 * scale, cy + 5 * scale], fill=dc)

    # Header Telemetry Metadata
    hdraw.text((160 * scale, hud_top + 14 * scale), "DOCUMENT: TECHNICAL_CV_INTERFACE // ID: RACHID_ARB // DOMAIN: ENTERPRISE_SYSTEMS", font=f_mono_hdr, fill=t_muted)
    hdraw.text((W - 380 * scale, hud_top + 14 * scale), "STATUS: VERIFIED // OPEN TO WORK", font=f_mono_hdr, fill=c_green)

    img = Image.alpha_composite(img, hud_layer)
    draw = ImageDraw.Draw(img)

    # 7. LEFT / CENTER HERO — THE RESUME IDENTITY (MAXIMUM READABILITY)
    # Safe central area
    left_x = 90 * scale
    start_y = hud_top + 65 * scale

    # Telemetry Badge Tag
    draw.text((left_x, start_y), "// PROFESSIONAL RÉSUMÉ & ARCHITECTURAL DIRECTIVE", font=f_tag, fill=c_cyan)

    # --- 1. RACHID (MASSIVE & UNMISTAKABLE) ---
    name_y = start_y + 26 * scale
    # Multi-pass electric cyan neon back-glow for dark mode
    if mode == 'dark':
        for ox, oy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)]:
            draw.text((left_x + ox * scale, name_y + oy * scale), "RACHID", font=f_name, fill=(0, 229, 255, 70))
    draw.text((left_x, name_y), "RACHID", font=f_name, fill=t_white)

    # --- 2. JAVA FULL-STACK SOFTWARE ENGINEER (LARGE & BOLD) ---
    title_y = name_y + 165 * scale
    draw.text((left_x, title_y), "JAVA FULL-STACK SOFTWARE ENGINEER", font=f_title, fill=t_cyan)

    # --- 3. BACKEND • SECURITY • TESTING • FULL-STACK (HIGH-IMPACT PILLARS) ---
    pillars_y = title_y + 60 * scale
    # Draw high-contrast pillar bar
    draw.text((left_x, pillars_y), "BACKEND  •  SECURITY  •  TESTING  •  FULL-STACK", font=f_pillars, fill=c_purple if mode == 'dark' else c_blue)

    # --- 4. Building secure, tested & maintainable software ---
    tagline_y = pillars_y + 44 * scale
    draw.text((left_x, tagline_y), "Building secure, tested & maintainable software", font=f_tagline, fill=t_slate)

    # --- 5. CV SPECIFICATION MATRICES (TWO CLEAN RESUME-STYLE CARDS) ---
    cards_y = tagline_y + 50 * scale
    card_w = 370 * scale
    card_h = 160 * scale

    spec_cards = [
        ("CORE TECH STACK", [
            ("LANGUAGE", "Java 21 LTS"),
            ("BACKEND", "Spring Boot 3.3"),
            ("DATABASE", "PostgreSQL 16"),
            ("FRONTEND", "React 18 · TypeScript")
        ], c_cyan),
        ("ENGINEERING SPECS", [
            ("SECURITY", "Stateless JWT · BCrypt"),
            ("VERIFICATION", "114 Tests (Mockito)"),
            ("CONTAINER", "Docker Compose"),
            ("PIPELINE", "GitHub Actions CI")
        ], c_green)
    ]

    for c_idx, (card_title, items, border_acc) in enumerate(spec_cards):
        cx = left_x + c_idx * (card_w + 20 * scale)
        cy = cards_y
        
        c_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(c_layer)
        
        # Rounded Card
        cdraw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=7 * scale, fill=hud_bg, outline=hud_border, width=1 * scale)
        # Header strip
        cdraw.rounded_rectangle([cx, cy, cx + card_w, cy + 30 * scale], radius=7 * scale, fill=hud_header_bg)
        cdraw.rectangle([cx, cy + 18 * scale, cx + card_w, cy + 30 * scale], fill=hud_header_bg)
        cdraw.line([(cx, cy + 30 * scale), (cx + card_w, cy + 30 * scale)], fill=hud_border, width=1 * scale)
        
        # Left Accent Tag
        cdraw.rectangle([cx + 10 * scale, cy + 8 * scale, cx + 14 * scale, cy + 22 * scale], fill=border_acc)
        cdraw.text((cx + 22 * scale, cy + 7 * scale), card_title, font=f_spec_hdr, fill=t_white)
        
        # Rows
        for row_i, (k, v) in enumerate(items):
            ry = cy + 38 * scale + row_i * 28 * scale
            cdraw.text((cx + 14 * scale, ry), k, font=f_spec_key, fill=t_dim)
            cdraw.text((cx + 140 * scale, ry), v, font=f_spec_val, fill=t_white)
            
        img = Image.alpha_composite(img, c_layer)
        draw = ImageDraw.Draw(img)

    # 8. RIGHT SIDE — THE SYSTEM ARCHITECTURE SCHEMATIC & THE SIGNATURE "R" DATA FLOW
    # Clean 4-Node Architecture Map
    arch_x = int(W * 0.54)
    arch_top = start_y + 10 * scale
    
    draw.text((arch_x, start_y), "// SYSTEM ARCHITECTURE TOPOLOGY", font=f_tag, fill=c_purple)

    node_w = 265 * scale
    node_h = 95 * scale
    
    # 4 Primary Nodes
    # Node 1 (Top Left): Client Gateway
    an1_x, an1_y = arch_x + 50 * scale, arch_top + 45 * scale
    # Node 2 (Top Right): Security Shield
    an2_x, an2_y = arch_x + 360 * scale, arch_top + 45 * scale
    # Node 3 (Center): Spring Boot Core
    an3_x, an3_y = arch_x + 200 * scale, arch_top + 190 * scale
    # Node 4 (Bottom Left): PostgreSQL
    an4_x, an4_y = arch_x + 50 * scale, arch_top + 335 * scale
    # Node 5 (Bottom Right): Quality Harness
    an5_x, an5_y = arch_x + 360 * scale, arch_top + 335 * scale

    arch_nodes = [
        (an1_x, an1_y, "01 // CLIENT TIER", "React 18 · TypeScript", "Vite · Responsive SPA", c_cyan),
        (an2_x, an2_y, "02 // SECURITY SHIELD", "Stateless JWT Auth", "BCrypt · Security Chain", c_amber),
        (an3_x, an3_y, "03 // APPLICATION CORE", "Spring Boot 3.3.5", "Domain Services · REST", c_green),
        (an4_x, an4_y, "04 // PERSISTENCE", "PostgreSQL 16", "Flyway Migrations · JPA", c_blue),
        (an5_x, an5_y, "05 // QUALITY HARNESS", "114 Automated Tests", "Mockito · MockMvc · 100%", c_purple),
    ]

    # --- THE SIGNATURE NEON "R" ARCHITECTURE DATA FLOW ---
    # The glowing neon data bus line flows through the nodes and subtly forms the letter "R"
    sig_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sig_layer)

    stem_x = an1_x - 30 * scale
    stem_top_y = an1_y + 15 * scale
    stem_bot_y = an4_y + node_h - 15 * scale

    def draw_neon_line(points, col):
        sdraw.line(points, fill=(col[0], col[1], col[2], 35), width=8 * scale)
        sdraw.line(points, fill=(col[0], col[1], col[2], 120), width=4 * scale)
        sdraw.line(points, fill=(255, 255, 255, 255), width=2 * scale)

    def draw_neon_arc(bbox, start, end, col):
        sdraw.arc(bbox, start=start, end=end, fill=(col[0], col[1], col[2], 40), width=8 * scale)
        sdraw.arc(bbox, start=start, end=end, fill=(col[0], col[1], col[2], 130), width=4 * scale)
        sdraw.arc(bbox, start=start, end=end, fill=(255, 255, 255, 255), width=2 * scale)

    # 1. R Stem Line (Vertical spine)
    draw_neon_line([(stem_x, stem_top_y), (stem_x, stem_bot_y)], c_cyan)
    
    # 2. R Top Horizontal Line (Stem to Security Node)
    loop_right_x = an2_x + node_w + 30 * scale
    loop_mid_y = an3_y + node_h // 2
    draw_neon_line([(stem_x, stem_top_y), (an2_x + node_w // 2, stem_top_y)], c_cyan)
    
    # 3. R Upper Loop (Arc looping around Node 2 into Spring Boot Core Node 3)
    arc_box = [an2_x + node_w // 2 - 20 * scale, stem_top_y, loop_right_x + 20 * scale, loop_mid_y]
    draw_neon_arc(arc_box, start=270, end=90, col=c_purple)
    draw_neon_line([(loop_right_x - 10 * scale, loop_mid_y), (an3_x + node_w, loop_mid_y)], c_purple)
    
    # 4. R Center Crossbar (closing into stem)
    draw_neon_line([(an3_x, loop_mid_y), (stem_x, loop_mid_y)], c_green)
    
    # 5. R Diagonal Leg (kicking down from Center Core into Node 5 Quality Harness)
    draw_neon_line([(an3_x + node_w // 2, loop_mid_y + 15 * scale), (an5_x + node_w // 2, an5_y + 15 * scale)], c_blue)

    # Monogram Signature Label
    f_sig = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 13 * scale)
    sdraw.text((stem_x - 15 * scale, stem_top_y - 25 * scale), "TRACE: [R]", font=f_sig, fill=c_cyan)

    # Glowing data packets along signature R
    junctions = [
        (stem_x, stem_top_y, c_cyan),
        (stem_x, loop_mid_y, c_green),
        (stem_x, stem_bot_y, c_blue),
        (loop_right_x + 5 * scale, (stem_top_y + loop_mid_y) // 2, c_purple),
        (an5_x + node_w // 2, an5_y + 15 * scale, c_cyan)
    ]
    for (jx, jy, jc) in junctions:
        sdraw.ellipse([jx - 7 * scale, jy - 7 * scale, jx + 7 * scale, jy + 7 * scale], fill=(jc[0], jc[1], jc[2], 60))
        sdraw.ellipse([jx - 4 * scale, jy - 4 * scale, jx + 4 * scale, jy + 4 * scale], fill=jc)
        sdraw.ellipse([jx - 2 * scale, jy - 2 * scale, jx + 2 * scale, jy + 2 * scale], fill=(255, 255, 255))

    img = Image.alpha_composite(img, sig_layer)

    # Draw Architecture Node Cards
    for (nx, ny, n_tag, n_title, n_sub, n_acc) in arch_nodes:
        nd_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ndraw = ImageDraw.Draw(nd_layer)
        
        # Rounded Card
        ndraw.rounded_rectangle([nx, ny, nx + node_w, ny + node_h], radius=8 * scale, fill=hud_bg, outline=hud_border, width=1 * scale)
        # Left Accent Border
        ndraw.rounded_rectangle([nx, ny, nx + 5 * scale, ny + node_h], radius=2 * scale, fill=n_acc)
        # Micro Header Strip
        ndraw.rounded_rectangle([nx, ny, nx + node_w, ny + 26 * scale], radius=8 * scale, fill=hud_header_bg)
        ndraw.rectangle([nx, ny + 16 * scale, nx + node_w, ny + 26 * scale], fill=hud_header_bg)
        ndraw.line([(nx, ny + 26 * scale), (nx + node_w, ny + 26 * scale)], fill=hud_border, width=1 * scale)
        
        # Text
        ndraw.text((nx + 14 * scale, ny + 6 * scale), n_tag, font=f_node_num, fill=t_dim)
        ndraw.text((nx + 14 * scale, ny + 34 * scale), n_title, font=f_node_title, fill=t_white)
        ndraw.text((nx + 14 * scale, ny + 66 * scale), n_sub, font=f_node_sub, fill=t_slate)
        
        # Status pulse in top right
        px = nx + node_w - 14 * scale
        py = ny + 13 * scale
        ndraw.ellipse([px - 3 * scale, py - 3 * scale, px + 3 * scale, py + 3 * scale], fill=n_acc)
        
        img = Image.alpha_composite(img, nd_layer)

    # 9. Bottom Terminal Status Bar
    footer_y = hud_bot - 45 * scale
    foot_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(foot_layer)
    
    fdraw.line([(50 * scale, footer_y), (W - 50 * scale, footer_y)], fill=hud_border, width=1 * scale)
    
    f_term = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 15 * scale)
    fdraw.text((70 * scale, footer_y + 13 * scale), "TERMINAL: mvn clean test ── [114/114 TESTS PASSED - 100% COVERAGE] ── DOCKER: ACTIVE", font=f_term, fill=c_cyan)
    fdraw.text((W - 560 * scale, footer_y + 13 * scale), "VERIFIED: CLEAN ARCHITECTURE · FLYWAY V1 · ZERO REGRESSION", font=f_term, fill=t_muted)

    img = Image.alpha_composite(img, foot_layer)

    # 10. Final Resampling
    final_img = img.resize((width, height), Image.Resampling.LANCZOS)
    final_img.save(output_path, 'PNG', optimize=True)
    print(f"Grand Résumé Banner {mode} saved to {output_path} ({width}x{height})")

if __name__ == '__main__':
    # 2000 x 750 (optimal GitHub profile ratio with massive readable text)
    draw_large_resume_banner('dark', 'art/header-dark.png', 2000, 750)
    draw_large_resume_banner('light', 'art/header-light.png', 2000, 750)
    draw_large_resume_banner('dark', 'art/social-media-dark.png', 1200, 630)
    
    # Sync to assets/
    draw_large_resume_banner('dark', 'assets/header-dark.png', 2000, 750)
    draw_large_resume_banner('light', 'assets/header-light.png', 2000, 750)
    draw_large_resume_banner('dark', 'assets/social-media-dark.png', 1200, 630)
