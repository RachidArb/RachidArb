import math
from PIL import Image, ImageDraw, ImageFont

def draw_resume_banner(mode='dark', output_path='art/header-dark.png', width=2200, height=880):
    scale = 2
    W, H = width * scale, height * scale

    if mode == 'dark':
        bg_0 = (6, 9, 15)          # #06090F Deepest Obsidian Void
        bg_1 = (10, 15, 25)        # #0A0F19 Technical Navy
        bg_2 = (14, 21, 35)        # #0E1523 Slate Navy
        
        dot_color = (56, 189, 248, 30) # Soft cyber micro-dots
        grid_line = (30, 45, 68, 20)   # Ultra-faint structural grid (barely visible texture)
        
        hud_bg = (11, 17, 28, 245)
        hud_border = (38, 55, 85, 230)
        hud_header_bg = (16, 25, 42, 255)
        
        c_cyan = (0, 229, 255)      # Electric Cyan
        c_blue = (59, 130, 246)     # Neon Blue
        c_purple = (168, 85, 247)   # Cyber Violet
        c_green = (16, 185, 129)    # Emerald Neon
        c_amber = (245, 158, 11)    # Java Amber
        
        t_white = (255, 255, 255)
        t_cyan = (56, 189, 248)
        t_slate = (203, 213, 225)
        t_muted = (148, 163, 184)
        t_dim = (100, 116, 139)
        code_dim = (56, 189, 248, 28)
    else:
        bg_0 = (248, 250, 253)
        bg_1 = (241, 245, 250)
        bg_2 = (235, 240, 248)
        
        dot_color = (2, 132, 199, 35)
        grid_line = (210, 220, 235, 60)
        
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
        code_dim = (2, 132, 199, 20)

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

    # 2. Ambient Lighting Flares (Soft Cyber Glow Behind Panels)
    bloom = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bloom)
    
    # Glow behind Name (Cyan)
    for r in range(400 * scale, 0, -15):
        a = int(18 * (1 - r / (400 * scale)))
        col = (c_cyan[0], c_cyan[1], c_cyan[2], a) if mode == 'dark' else (c_cyan[0], c_cyan[1], c_cyan[2], a // 2)
        bdraw.ellipse([280 * scale - r, 380 * scale - r, 280 * scale + r, 380 * scale + r], fill=col)

    # Glow behind Architecture HUD (Violet & Green)
    for r in range(550 * scale, 0, -20):
        a = int(22 * (1 - r / (550 * scale)))
        col = (c_purple[0], c_purple[1], c_purple[2], a) if mode == 'dark' else (c_blue[0], c_blue[1], c_blue[2], a // 2)
        bdraw.ellipse([W - 550 * scale - r, 440 * scale - r, W - 550 * scale + r, 440 * scale + r], fill=col)
        
    img = Image.alpha_composite(img, bloom)
    draw = ImageDraw.Draw(img)

    # 3. Micro-Dot Technical Grid (Non-intrusive)
    step = 45 * scale
    for x in range(30 * scale, W, step):
        for y in range(30 * scale, H, step):
            draw.rectangle([x - 1 * scale, y - 1 * scale, x + 1 * scale, y + 1 * scale], fill=dot_color)

    # 4. Subtle Background Java Code / Hex Watermark
    code_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(code_layer)
    f_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13 * scale)
    bg_code_snippets = [
        "@RestController",
        "@RequestMapping(\"/api/v1/orchestrator\")",
        "public class EnterpriseTaskController {",
        "    private final TaskService taskService;",
        "    private final JwtTokenProvider jwtProvider;",
        "    @PreAuthorize(\"hasRole('ADMIN')\")",
        "    @PostMapping(\"/dispatch\")",
        "    public ResponseEntity<TaskResponse> execute(@Valid @RequestBody TaskRequest req) {",
        "        return ResponseEntity.ok(taskService.process(req));",
        "    }",
        "}",
        "// 0x7F4A9B · TCP:PORT 8080 · POOL: HIKARICP · FLYWAY: V1_INIT",
        "// MEMORY: HEAP_OPTIMIZED // GC: ZGC // THREADS: VIRTUAL"
    ]
    code_x = int(W * 0.38)
    code_y = 95 * scale
    for idx, line in enumerate(bg_code_snippets):
        cdraw.text((code_x, code_y + idx * 24 * scale), line, font=f_code, fill=code_dim)
    img = Image.alpha_composite(img, code_layer)
    draw = ImageDraw.Draw(img)

    # 5. Fonts Setup
    f_mono_hdr = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 15 * scale)
    f_mono_dim = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13 * scale)
    f_name = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 138 * scale)       # Huge commanding name
    f_title = ImageFont.truetype("C:/Windows/Fonts/segoeuiz.ttf", 46 * scale)      # Bold title
    f_tagline = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 30 * scale)     # Clear philosophy
    f_section = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 16 * scale)
    f_label = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 14 * scale)
    f_val = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15 * scale)
    f_node_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 19 * scale)
    f_node_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13 * scale)
    f_node_tag = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 12 * scale)

    # 6. Futuristic CV Top Window Bar / HUD Metadata
    hud_bar_y = 45 * scale
    bar_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bldraw = ImageDraw.Draw(bar_layer)
    
    # Outer frame
    bldraw.rounded_rectangle([60 * scale, hud_bar_y, W - 60 * scale, H - 45 * scale], radius=16 * scale, outline=hud_border, width=int(1.5 * scale))
    
    # Top HUD Bar
    bldraw.rounded_rectangle([60 * scale, hud_bar_y, W - 60 * scale, hud_bar_y + 44 * scale], radius=16 * scale, fill=hud_header_bg)
    bldraw.rectangle([60 * scale, hud_bar_y + 24 * scale, W - 60 * scale, hud_bar_y + 44 * scale], fill=hud_header_bg)
    bldraw.line([(60 * scale, hud_bar_y + 44 * scale), (W - 60 * scale, hud_bar_y + 44 * scale)], fill=hud_border, width=1 * scale)

    # Window Control Dots (Cyan, Violet, Green)
    dots = [c_cyan, c_purple, c_green]
    for i, dc in enumerate(dots):
        cx = 90 * scale + i * 20 * scale
        cy = hud_bar_y + 22 * scale
        bldraw.ellipse([cx - 5 * scale, cy - 5 * scale, cx + 5 * scale, cy + 5 * scale], fill=dc)

    # Header Telemetry Metadata
    bldraw.text((170 * scale, hud_bar_y + 13 * scale), "DOC: CURRICULUM_VITAE // SYS_ID: RACHID_ARB // ROLE: FULL-STACK ENGINEER", font=f_mono_hdr, fill=t_muted)
    bldraw.text((W - 380 * scale, hud_bar_y + 13 * scale), "STATUS: VERIFIED // OPEN TO WORK", font=f_mono_hdr, fill=c_green)

    img = Image.alpha_composite(img, bar_layer)
    draw = ImageDraw.Draw(img)

    # 7. LEFT SIDE — The Résumé Core Identity
    left_x = 100 * scale
    content_y = hud_bar_y + 70 * scale

    # Section tag
    sec_tag = "// PROFESSIONAL PROFILE & TECHNICAL DIRECTIVE"
    draw.text((left_x, content_y), sec_tag, font=f_section, fill=c_cyan)

    # NAME: RACHID
    name_y = content_y + 30 * scale
    if mode == 'dark':
        for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((left_x + ox * scale, name_y + oy * scale), "RACHID", font=f_name, fill=(0, 229, 255, 60))
    draw.text((left_x, name_y), "RACHID", font=f_name, fill=t_white)

    # SUBTITLE: JAVA FULL-STACK SOFTWARE ENGINEER
    title_y = name_y + 155 * scale
    draw.text((left_x, title_y), "JAVA FULL-STACK SOFTWARE ENGINEER", font=f_title, fill=t_cyan)

    # STATEMENT: Building secure, tested & maintainable software
    stmt_y = title_y + 64 * scale
    draw.text((left_x, stmt_y), "Building secure, tested & maintainable software", font=f_tagline, fill=t_slate)

    # 8. Resume-Style Structured Metadata Cards (Compact Spec Tables)
    card_y = stmt_y + 65 * scale
    
    cv_cards = [
        ("CORE ARCHITECTURE", [
            ("LANGUAGE", "Java 21 LTS"),
            ("BACKEND", "Spring Boot 3.3"),
            ("PERSISTENCE", "PostgreSQL 16"),
            ("FRONTEND", "React 18 · TS")
        ]),
        ("ENGINEERING SPECS", [
            ("SECURITY", "Stateless JWT · BCrypt"),
            ("TEST HARNESS", "114 Tests (Mockito)"),
            ("CONTAINER", "Docker & Compose"),
            ("PIPELINE", "GitHub Actions CI")
        ])
    ]

    card_w = 410 * scale
    card_h = 175 * scale
    
    for c_idx, (c_title, c_items) in enumerate(cv_cards):
        cx = left_x + c_idx * (card_w + 24 * scale)
        cy = card_y
        
        c_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(c_layer)
        
        # Glass card
        cdraw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=8 * scale, fill=hud_bg, outline=hud_border, width=1 * scale)
        # Header strip
        cdraw.rounded_rectangle([cx, cy, cx + card_w, cy + 34 * scale], radius=8 * scale, fill=hud_header_bg)
        cdraw.rectangle([cx, cy + 20 * scale, cx + card_w, cy + 34 * scale], fill=hud_header_bg)
        cdraw.line([(cx, cy + 34 * scale), (cx + card_w, cy + 34 * scale)], fill=hud_border, width=1 * scale)
        
        # Accent tag
        cdraw.rectangle([cx + 10 * scale, cy + 10 * scale, cx + 14 * scale, cy + 24 * scale], fill=c_cyan if c_idx == 0 else c_purple)
        cdraw.text((cx + 24 * scale, cy + 9 * scale), c_title, font=f_label, fill=t_white)
        
        # Rows
        for row_i, (k, v) in enumerate(c_items):
            ry = cy + 44 * scale + row_i * 30 * scale
            cdraw.text((cx + 16 * scale, ry), k, font=f_mono_dim, fill=t_dim)
            cdraw.text((cx + 150 * scale, ry), v, font=f_val, fill=t_white)
            
        img = Image.alpha_composite(img, c_layer)
        draw = ImageDraw.Draw(img)

    # 9. RIGHT SIDE — The Futuristic Software Architecture & Signature "R" Data Flow
    arch_x0 = int(W * 0.52)
    arch_y0 = content_y + 10 * scale
    
    # Topology Header
    topo_tag = "// DISTRIBUTED SYSTEMS TOPOLOGY & ARCHITECTURE"
    draw.text((arch_x0, content_y), topo_tag, font=f_section, fill=c_purple)

    node_w = 260 * scale
    node_h = 100 * scale
    
    n1_x, n1_y = arch_x0, arch_y0 + 40 * scale                        # Node 1: REST Gateway / Client
    n2_x, n2_y = arch_x0 + 320 * scale, arch_y0 + 40 * scale          # Node 2: Security Filter
    n3_x, n3_y = arch_x0 + 160 * scale, arch_y0 + 195 * scale         # Node 3: Spring Boot Domain Core
    n4_x, n4_y = arch_x0, arch_y0 + 355 * scale                       # Node 4: PostgreSQL Persistence
    n5_x, n5_y = arch_x0 + 320 * scale, arch_y0 + 355 * scale         # Node 5: Verification & Tests
    
    arch_nodes = [
        (n1_x, n1_y, "01 // CLIENT TIER", "React 18 · TypeScript", "Vite · Responsive SPA", c_cyan),
        (n2_x, n2_y, "02 // SECURITY FENCE", "Stateless JWT Auth", "BCrypt · Filter Chain", c_amber),
        (n3_x, n3_y, "03 // SPRING BOOT 3", "Layered Domain Core", "REST APIs · Service Mesh", c_green),
        (n4_x, n4_y, "04 // PERSISTENCE", "PostgreSQL 16", "Flyway Migrations · JPA", c_blue),
        (n5_x, n5_y, "05 // QUALITY HARNESS", "114 Automated Tests", "Mockito · MockMvc · 100%", c_purple),
    ]

    # --- THE SIGNATURE NEON "R" DATA FLOW ---
    sig_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sig_layer)

    stem_x = n1_x - 30 * scale
    stem_top_y = n1_y + 20 * scale
    stem_bot_y = n4_y + node_h - 20 * scale

    def draw_neon_line(points, col):
        sdraw.line(points, fill=(col[0], col[1], col[2], 40), width=8 * scale)
        sdraw.line(points, fill=(col[0], col[1], col[2], 130), width=4 * scale)
        sdraw.line(points, fill=(255, 255, 255, 255), width=2 * scale)

    def draw_neon_arc(bbox, start, end, col):
        sdraw.arc(bbox, start=start, end=end, fill=(col[0], col[1], col[2], 45), width=8 * scale)
        sdraw.arc(bbox, start=start, end=end, fill=(col[0], col[1], col[2], 140), width=4 * scale)
        sdraw.arc(bbox, start=start, end=end, fill=(255, 255, 255, 255), width=2 * scale)

    # R Stem Line
    draw_neon_line([(stem_x, stem_top_y), (stem_x, stem_bot_y)], c_cyan)
    
    # R Top Horizontal (from stem to Node 2)
    loop_right_x = n2_x + node_w + 30 * scale
    loop_mid_y = n3_y + node_h // 2
    draw_neon_line([(stem_x, stem_top_y), (n2_x + node_w // 2, stem_top_y)], c_cyan)
    
    # R Upper Loop (Arc curving right and back into Center Spring Core Node 3)
    arc_box = [n2_x + node_w // 2 - 20 * scale, stem_top_y, loop_right_x + 20 * scale, loop_mid_y]
    draw_neon_arc(arc_box, start=270, end=90, col=c_purple)
    draw_neon_line([(loop_right_x - 10 * scale, loop_mid_y), (n3_x + node_w, loop_mid_y)], c_purple)
    
    # R Center Crossbar (closing into stem)
    draw_neon_line([(n3_x, loop_mid_y), (stem_x, loop_mid_y)], c_green)
    
    # R Diagonal Leg (kicking down from Center Core to Node 5 Test Harness)
    draw_neon_line([(n3_x + node_w // 2, loop_mid_y + 20 * scale), (n5_x + node_w // 2, n5_y + 20 * scale)], c_blue)

    # Signature Tag Monogram Label placed neatly above
    f_sig = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 12 * scale)
    sdraw.text((stem_x - 10 * scale, stem_top_y - 24 * scale), "DATA_TRACE // [R]", font=f_sig, fill=c_cyan)

    # Data packets / glowing junction points along signature R
    junctions = [
        (stem_x, stem_top_y, c_cyan),
        (stem_x, loop_mid_y, c_green),
        (stem_x, stem_bot_y, c_blue),
        (loop_right_x + 5 * scale, (stem_top_y + loop_mid_y) // 2, c_purple),
        (n5_x + node_w // 2, n5_y + 20 * scale, c_cyan)
    ]
    for (jx, jy, jc) in junctions:
        sdraw.ellipse([jx - 7 * scale, jy - 7 * scale, jx + 7 * scale, jy + 7 * scale], fill=(jc[0], jc[1], jc[2], 60))
        sdraw.ellipse([jx - 4 * scale, jy - 4 * scale, jx + 4 * scale, jy + 4 * scale], fill=jc)
        sdraw.ellipse([jx - 2 * scale, jy - 2 * scale, jx + 2 * scale, jy + 2 * scale], fill=(255, 255, 255))

    img = Image.alpha_composite(img, sig_layer)

    # Draw Architecture Node Boxes
    for (nx, ny, n_tag, n_title, n_sub, n_acc) in arch_nodes:
        nd_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ndraw = ImageDraw.Draw(nd_layer)
        
        # Card Body
        ndraw.rounded_rectangle([nx, ny, nx + node_w, ny + node_h], radius=8 * scale, fill=hud_bg, outline=hud_border, width=1 * scale)
        # Left Accent Border
        ndraw.rounded_rectangle([nx, ny, nx + 5 * scale, ny + node_h], radius=2 * scale, fill=n_acc)
        # Micro Header Strip
        ndraw.rounded_rectangle([nx, ny, nx + node_w, ny + 26 * scale], radius=8 * scale, fill=hud_header_bg)
        ndraw.rectangle([nx, ny + 16 * scale, nx + node_w, ny + 26 * scale], fill=hud_header_bg)
        ndraw.line([(nx, ny + 26 * scale), (nx + node_w, ny + 26 * scale)], fill=hud_border, width=1 * scale)
        
        # Texts
        ndraw.text((nx + 14 * scale, ny + 6 * scale), n_tag, font=f_node_tag, fill=t_dim)
        ndraw.text((nx + 14 * scale, ny + 35 * scale), n_title, font=f_node_title, fill=t_white)
        ndraw.text((nx + 14 * scale, ny + 68 * scale), n_sub, font=f_node_sub, fill=t_slate)
        
        # Active pulse in top right
        px = nx + node_w - 14 * scale
        py = ny + 13 * scale
        ndraw.ellipse([px - 3 * scale, py - 3 * scale, px + 3 * scale, py + 3 * scale], fill=n_acc)
        
        img = Image.alpha_composite(img, nd_layer)

    # 10. Bottom HUD Status & Terminal Feed
    footer_y = H - 85 * scale
    foot_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(foot_layer)
    
    fdraw.line([(80 * scale, footer_y), (W - 80 * scale, footer_y)], fill=hud_border, width=1 * scale)
    
    # Left terminal message
    fdraw.text((85 * scale, footer_y + 12 * scale), "TERMINAL: git commit -m \"feat: resilient clean architecture\" [114/114 TESTS PASSING]", font=f_mono_hdr, fill=c_cyan)
    
    # Right telemetry tags
    fdraw.text((W - 620 * scale, footer_y + 12 * scale), "VERIFIED: CLEAN CODE · DOCKER CONTAINERIZED · ZERO REGRESSION", font=f_mono_hdr, fill=t_muted)

    img = Image.alpha_composite(img, foot_layer)

    # 11. Final High-Quality Downsampling
    final_img = img.resize((width, height), Image.Resampling.LANCZOS)
    final_img.save(output_path, 'PNG', optimize=True)
    print(f"Cyber-Resume {mode} banner saved to {output_path} ({width}x{height})")

if __name__ == '__main__':
    # 2200x880 gives a 2.5:1 ratio (substantially bigger and taller!)
    draw_resume_banner('dark', 'art/header-dark.png', 2200, 880)
    draw_resume_banner('light', 'art/header-light.png', 2200, 880)
    draw_resume_banner('dark', 'art/social-media-dark.png', 1200, 630)
    
    # Sync to assets/
    draw_resume_banner('dark', 'assets/header-dark.png', 2200, 880)
    draw_resume_banner('light', 'assets/header-light.png', 2200, 880)
    draw_resume_banner('dark', 'assets/social-media-dark.png', 1200, 630)
