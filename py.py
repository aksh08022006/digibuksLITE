python3 << 'PYEOF'
with open('/tmp/existing_css.txt','r') as f: existing_css = f.read()
with open('/tmp/svg_bg.txt','r') as f: svg_bg = f.read()
with open('/tmp/left_panel.txt','r') as f: left_panel = f.read()
with open('/tmp/original_script.txt','r') as f: original_script = f.read()
with open('/tmp/logo_data.txt','r') as f: logo_data = f.read().strip()

# Build the new auth styles to insert before </style>
new_css = '''
    /* ══ PART 1: AUTH MODE TOGGLE — NEW ADDITIONS ══ */

    /* Panel container uses CSS grid stacking so both panels
       occupy the same grid cell; height = tallest panel */
    .auth-panels {
      display: grid;
      grid-template-columns: 1fr;
      grid-template-rows: auto;
    }

    .form-panel {
      grid-column: 1;
      grid-row: 1;
      width: 100%;
      transition: opacity 0.42s ease, transform 0.42s ease;
    }

    .form-panel.is-active {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
      z-index: 2;
    }

    .form-panel.is-inactive {
      opacity: 0;
      transform: translateY(14px);
      pointer-events: none;
      z-index: 1;
    }

    /* Auth header transition */
    .auth-header {
      transition: opacity 0.3s ease;
    }

    /* Remember me + forgot password row */
    .remember-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .remember-row .checkbox-label {
      flex: 1;
    }

    .forgot-link {
      color: var(--green-dark);
      font-size: 0.875rem;
      font-weight: 600;
      text-decoration: none;
      white-space: nowrap;
      flex-shrink: 0;
    }

    .forgot-link:hover { text-decoration: underline; }

    /* Required asterisk */
    .req { color: var(--green-dark); }

    /* ── Keyboard focus ring fix for hidden panels ── */
    .form-panel.is-inactive * { tabindex: -1; }
'''

# Insert new CSS before closing </style>
modified_css = existing_css.replace('</style>', new_css + '\n  </style>')

# Build the new auth card HTML
new_auth_card = '''      <!-- Right panel: Auth card — PART 1: Toggle System -->
      <section class="auth-right" aria-labelledby="auth-heading">
        <div class="auth-card">

          <!-- Dynamic header — text changes on mode switch -->
          <div class="auth-header" id="auth-header">
            <h2 id="auth-heading">Create your account</h2>
            <p id="auth-subheading">Start filing your taxes and managing finances with confidence.</p>
          </div>

          <!-- ── Stacked panels container ── -->
          <div class="auth-panels" id="auth-panels">

            <!-- PANEL: Create Account (default active) -->
            <div class="form-panel is-active" id="panel-register" role="tabpanel" aria-labelledby="auth-heading">
              <form class="auth-form" id="form-register" onsubmit="return false" novalidate>
                <div class="form-row">
                  <div class="form-field">
                    <label for="first-name">First Name</label>
                    <input id="first-name" type="text" name="first-name" autocomplete="given-name" placeholder="Aarav" required />
                  </div>
                  <div class="form-field">
                    <label for="last-name">Last Name</label>
                    <input id="last-name" type="text" name="last-name" autocomplete="family-name" placeholder="Sharma" required />
                  </div>
                </div>
                <div class="form-field">
                  <label for="mobile">Mobile</label>
                  <input id="mobile" type="tel" name="mobile" autocomplete="tel" placeholder="+91 98765 43210" required />
                </div>
                <div class="form-field">
                  <label for="reg-email">Email</label>
                  <input id="reg-email" type="email" name="email" autocomplete="email" placeholder="you@domain.com" required />
                </div>
                <div class="form-field">
                  <label for="reg-password">Password</label>
                  <input id="reg-password" type="password" name="password" autocomplete="new-password" placeholder="Create a strong password" required />
                </div>
                <label class="checkbox-label">
                  <input type="checkbox" name="terms" required />
                  <span>I agree to the <a href="#" style="color:var(--green-dark);font-weight:600;">Terms of Service</a> and <a href="#" style="color:var(--green-dark);font-weight:600;">Privacy Policy</a></span>
                </label>
                <button class="btn-primary" type="submit">Create Account &rarr;</button>

                <div class="signin-section">
                  <div class="form-divider">Already have an account?</div>
                  <a class="link-signin" href="#" id="go-to-signin" role="button" aria-label="Switch to sign in">Sign in to Digibuks</a>
                </div>
              </form>
            </div><!-- end panel-register -->

            <!-- PANEL: Sign In (initially inactive) -->
            <div class="form-panel is-inactive" id="panel-signin" role="tabpanel" aria-labelledby="auth-heading" aria-hidden="true">
              <form class="auth-form" id="form-signin" onsubmit="return false" novalidate>
                <div class="form-field">
                  <label for="signin-email">Email Address</label>
                  <input id="signin-email" type="email" name="email" autocomplete="email" placeholder="you@domain.com" required />
                </div>
                <div class="form-field">
                  <label for="signin-password">Password</label>
                  <input id="signin-password" type="password" name="password" autocomplete="current-password" placeholder="Your password" required />
                </div>
                <div class="remember-row">
                  <label class="checkbox-label">
                    <input type="checkbox" name="remember-me" />
                    <span>Remember me</span>
                  </label>
                  <a href="#" class="forgot-link">Forgot password?</a>
                </div>
                <button class="btn-primary" type="submit">Sign In &rarr;</button>

                <div class="signin-section">
                  <div class="form-divider">New to Digibuks?</div>
                  <a class="link-signin" href="#" id="go-to-register" role="button" aria-label="Switch to create account">Create Account</a>
                </div>
              </form>
            </div><!-- end panel-signin -->

          </div><!-- end auth-panels -->

          <div class="auth-footer">
            <span>Need help?</span>
            <a href="digibuks-tax-expert.html">Talk to a tax expert &rarr;</a>
          </div>
        </div>
      </section>
'''

# The new toggle JS
new_script = '''  <!-- PART 1: Auth Mode Toggle Script -->
  <script>
    (() => {
      /* ── Slider (existing functionality preserved) ── */
      const slides    = Array.from(document.querySelectorAll("[data-slide]"));
      const imgSlides = Array.from(document.querySelectorAll("[data-img-slide]"));
      const dots      = Array.from(document.querySelectorAll("[data-index]"));
      const slider    = document.querySelector("[data-slider]");
      if (slides.length) {
        let idx = 0, timer = null;
        const go = n => {
          idx = (n + slides.length) % slides.length;
          slides.forEach((s, i) => s.classList.toggle("is-active", i === idx));
          imgSlides.forEach((s, i) => s.classList.toggle("is-active", i === idx));
          dots.forEach((d, i) => d.classList.toggle("is-active", i === idx));
        };
        const play = () => { stop(); timer = setInterval(() => go(idx + 1), 4800); };
        const stop = () => { clearInterval(timer); timer = null; };
        dots.forEach(d => d.addEventListener("click", () => { go(+d.dataset.index); play(); }));
        slider?.addEventListener("mouseenter", stop);
        slider?.addEventListener("mouseleave", play);
        go(0); play();
      }

      /* ── Auth Mode Toggle ── */
      const panelRegister = document.getElementById("panel-register");
      const panelSignin   = document.getElementById("panel-signin");
      const heading       = document.getElementById("auth-heading");
      const subheading    = document.getElementById("auth-subheading");
      const goSignIn      = document.getElementById("go-to-signin");
      const goRegister    = document.getElementById("go-to-register");

      const MODES = {
        register: {
          heading:    "Create your account",
          subheading: "Start filing your taxes and managing finances with confidence."
        },
        signin: {
          heading:    "Welcome back",
          subheading: "Sign in to access your Digibuks dashboard and continue managing your finances."
        }
      };

      function switchMode(mode) {
        const info = MODES[mode];

        /* Update text */
        heading.textContent    = info.heading;
        subheading.textContent = info.subheading;

        /* Swap active / inactive panels */
        if (mode === "signin") {
          panelRegister.classList.replace("is-active",   "is-inactive");
          panelRegister.setAttribute("aria-hidden", "true");
          /* Small RAF ensures CSS sees the state change for transition */
          requestAnimationFrame(() => {
            panelSignin.classList.replace("is-inactive", "is-active");
            panelSignin.setAttribute("aria-hidden", "false");
            /* Move keyboard focus to first field */
            const first = panelSignin.querySelector("input, select, textarea, button");
            first?.focus();
          });
        } else {
          panelSignin.classList.replace("is-active",   "is-inactive");
          panelSignin.setAttribute("aria-hidden", "true");
          requestAnimationFrame(() => {
            panelRegister.classList.replace("is-inactive", "is-active");
            panelRegister.setAttribute("aria-hidden", "false");
            const first = panelRegister.querySelector("input, select, textarea, button");
            first?.focus();
          });
        }
      }

      goSignIn?.addEventListener("click",   e => { e.preventDefault(); switchMode("signin");   });
      goRegister?.addEventListener("click", e => { e.preventDefault(); switchMode("register"); });
    })();
  </script>
'''

# Now assemble the final HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Digibuks — Secure ITR Filing</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet" />

  {modified_css}
</head>
<body>

{svg_bg}

  <div class="page">
    <main class="auth-layout">

{left_panel}
{new_auth_card}
    </main>
  </div>

{new_script}
</body>
</html>'''

with open('/tmp/digibuks-auth-main.html', 'w') as f:
    f.write(html)

print(f"Main auth file written: {len(html)} chars")
PYEOF