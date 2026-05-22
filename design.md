# RetailPulse Analytics Management Suite: Comprehensive UI/UX Specification Document

---

## 1. Executive Design Vision & Paradigm

The RetailPulse Management Suite is engineered as a highly performant, data-dense web application optimized for retail enterprise operators and senior administrators. The design balances micro-level operational tracking with macro-level trend forecasting.

### 1.1 Aesthetic & Mental Model
* **The Paradigm:** The interface employs a flat, clean design language influenced by material layers. It rejects unnecessary ornamentation in favor of sharp typographic hierarchy and deliberate spacing.
* **The Emotional Target:** Focuses on clarity and control. By reducing visual cognitive load, administrators are guided to notice anomalies instantly (e.g., negative trend percentages, pending transaction statuses) within an ambient environment of calm, structured data.
* **Spatial Architecture:** Uses a fixed left-rail navigation scheme coupled with a pinned header. This layout bounds a fluid, single-pane canvas container (`max-w-1440px`), ensuring that system telemetry points remain structurally unified on wide-aspect workstation monitors.

---

## 2. Design System Tokens & Foundations

### 2.1 Typographic Scale & Hierarchy
The application leverages two distinct type families to separate narrative context from raw transactional data metrics.

| System Variable / Utility | Font Family | Size (px) | Line Height | Weight | Contextual Application |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `display-lg` | Hanken Grotesk | 36px | 44px | 700 (Bold) | High-impact data values, Metric totals |
| `headline-md` | Hanken Grotesk | 24px | 32px | 600 (Semi-Bold)| Page-level greetings, Panel definitions |
| `title-sm` | Inter | 18px | 24px | 600 (Semi-Bold)| Section headers, Sub-component contexts |
| `body-md` | Inter | 16px | 24px | 400 (Regular) | Explanatory labels, Primary text data |
| `body-sm` | Inter | 14px | 20px | 400 (Regular) | Form controls, Table cells, Meta descriptive logs |
| `label-caps` | Inter | 12px | 16px | 600 (Semi-Bold)| Navigation titles, Action triggers, Uppercase tokens |

### 2.2 Color Palette & Semantic Assignment
The palette relies on dynamic tonal variations to convey system health and interactive states cleanly.

├── Primary Brand Tokens
│   ├── Primary Light (#004ac6) : Main emphasis, system brand anchor.
│   ├── Primary Container (#2563eb) : Active selection fill, high-priority interactions.
│   └── On-Primary (#ffffff) : High-contrast text on primary shapes.
├── Secondary Neutral Tokens
│   ├── Background Light (#f7f9fb) : Application-wide viewport floor.
│   ├── Surface Container (#eceef0) : Inset backgrounds, layout boundaries.
│   ├── Surface Lowest (#ffffff) : Elevated component backdrops (Bento cards, tables).
│   └── Outline Variant (#c3c6d7) : Explicit structural separation strokes.
└── Semantic Telemetry Tokens
├── Success (#006242) : Upward positive trajectories, Completed workflows.
├── Success Container (#6ffbbe) : Muted background wrapper for successful actions.
├── Error/Alert (#ba1a1a) : Deprecating trends, Refund statuses, Disastrous bounds.
└── Error Container (#ffdad6) : High-visibility backdrops for alert elements.


### 2.3 Structural Geometry & Spacing Values
The application aligns its components onto an explicit layout grid using systematic layout tokens:
* `spacing.gutter`: `1.5rem` (24px) padding between distinct modular elements.
* `spacing.stack-lg`: `2rem` (32px) separating macro semantic layouts.
* `spacing.stack-md`: `1rem` (16px) standard container internal padding.
* `spacing.stack-sm`: `0.5rem` (8px) structural group binding or text separation.
* `borderRadius.DEFAULT`: `0.25rem` (4px) for subtle inputs or semantic badges.
* `borderRadius.xl`: `0.75rem` (12px) for structural bento grid metric wrapper blocks.

---

## 3. Structural Layout & Interface Architecture

+------------------------------------------------------------------------------------+
|  SIDEBAR           |  TOP NAVIGATION HEADER                                        |
|  [RetailPulse Log] |  [Search Metrics...]                   (🔔) (❓) (⚙️) [User V] |
|--------------------+---------------------------------------------------------------|
|  (🎯) Dashboard    |  WELCOME CANVAS                                               |
|  (📦) Inventory    |  Good Morning, Amanda                  [30 Days] [Adv Filter] |
|  (💳) Sales        |                                                               |
|  (📊) Analytics    | +-----------------------------------------------------------+ |
|  (📄) Reports      | | BENTO METRICS: Revenue | Orders | Avg Value | Conv. Rate  | |
|                    | +-----------------------------------------------------------+ |
|                    |                                                               |
|  +--------------+  | +-----------------------------------+ +---------------------+ |
|  | Export Rep.  |  | | SALES PERFORMANCE CHART           | | TOP PRODUCTS      | |
|  +--------------+  | |                                   | | Nike Air Max      | |
|  (⚙️) Settings     | | [ Bar Graph Visualization ]       | | Wireless Headph.  | |
|  (🚪) Logout       | +-----------------------------------+ +---------------------+ |
|                    |                                                               |
|                    | +-----------------------------------------------------------+ |
|                    | | RECENT TRANSACTIONS TABLE                                 | |
|                    | | Order ID  | Customer      | Status   | Date    | Amount   | |
|                    | +-----------------------------------------------------------+ |
+--------------------+---------------------------------------------------------------+


### 3.1 Global Shelving Structure
The core workspace layout uses a fixed left rail (`w-64`) paired with a fluid main canvas frame. On screen configurations beneath `1024px`, the application uses screen-edge matching media queries to seamlessly collapse the sidebar layout entirely, swapping it for an absolute bottom-pinned dashboard navigation dock.

---

## 4. Component-Level UX Breakdown

### 4.1 Global Command and Search Utility Bar
* **Affordance Design:** Spans the top viewport horizon, baseline-bounded at `h-16`. The entry search field features an immediate inline magnifying glass icon (`Material Symbols: search`), communicating input utility instantly.
* **User Action State:** Input fields display a focused outline transition changing from the neutral border tint (`#c3c6d7`) to a clear blue border accent (`#004ac6`), supported by an ambient outer glow (`focus:ring-2 focus:ring-primary/20`).

### 4.2 High-Velocity KPI Bento Framework
The metrics engine uses a four-column grid system to highlight critical point-in-time statistics.

+----------------------------------------+
| (Icon)                        +12.5% ↗ | <-- Upward trend colored in Semantic Success
|                                        |
| TOTAL REVENUE                          | <-- Metric category tag label text
| $124,592                               | <-- Large scale typographic focal value
| vs. $110,243 last month                | <-- Baseline performance comparison metadata
+----------------------------------------+


* **Total Revenue Value ($124,592):** Paired with a positive semantic delta badge (`+12.5%`) styled in active green.
* **Orders Placed Volume (1,842):** Identifies macro transactional throughput changes, showing positive growth indicators (`+8.2%`).
* **Average Order Value ($67.64):** Uses a warning pattern to stand out. It highlights a slight structural dip (`-2.4%`) with a red negative delta layout to call attention to lower basket sizes.
* **Conversion Rate Efficiency (3.4%):** Captures high-level browser conversion trends with clear, bold text scaling.

### 4.3 Sales Performance Histogram Container
* **Data Layout:** Takes up a wide two-column structural block (`lg:col-span-2`) to show historical performance trends over time.
* **Visualization Logic:** The visualization bars use a soft primary canvas mix (`bg-primary/20`). It features an interactive current-week metric callout (`bg-primary`), which highlights specific target values dynamically whenever a user moves their mouse over the block.
* **Hover Micro-Interactions:** When hovering over the active data bar, a dark tool-tip box pops into view using an absolute anchor layout (`Week 3: $34.2k`). This contextual update shifts opacity seamlessly (`transition-opacity duration-200`) to give administrators immediate access to precision data values.

### 4.4 Top Products Volume Sidebar
* **Item Layout Strategy:** Items are arranged in tight, vertically stacked rows within an independent panel context to highlight high-value retail merchandise quickly.
* **Visual Assets:** High-contrast square image placeholders feature rounded corners (`rounded-lg`), backed by clean item variant titles and transaction tallies (`14 sold`).
* **Overflow Context:** Uses a custom scroll tracking container layout (`overflow-y-auto`) to let users browse long product lists comfortably without breaking the main page structure.

### 4.5 Data Ledger (Recent Transactions)
* **Data Presentation:** Data columns are arranged cleanly across a tabular interface to make skimming row details effortless.
* **State Badges:** Workflow outcomes use high-visibility status labels to help users scan operational health markers quickly:
    * `SUCCESS`: Styled with a solid green badge wrapper (`#6ffbbe`).
    * `PENDING`: Set against a neutral, soft blue badge layout (`#d3e4fe`).
    * `REFUNDED`: Marked clearly with a soft red container alert tint (`#ffdad6`).
* **Interactive Row Feedback:** When hovering over individual rows, the background shifts smoothly to a crisp light tint (`hover:bg-surface-bright`). This subtle change helps the user keep their place visually while reviewing dense lines of text.

---

## 5. Modern Code Implementation (Tailwind CSS)

The structural blueprint below provides an production-ready HTML structure matching the user interface specifications.

```html
<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>RetailPulse Analytics | Corporate Suite</title>
    <script src="[https://cdn.tailwindcss.com?plugins=forms,container-queries](https://cdn.tailwindcss.com?plugins=forms,container-queries)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap](https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap)" rel="stylesheet"/>
    <link href="[https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1](https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1)" rel="stylesheet"/>
    <script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#004ac6",
                        "primary-container": "#2563eb",
                        "on-primary": "#ffffff",
                        "surface-bright": "#f7f9fb",
                        "surface-container-low": "#f2f4f6",
                        "surface-container-lowest": "#ffffff",
                        "outline-variant": "#c3c6d7",
                        "on-surface": "#191c1e",
                        "on-surface-variant": "#434655",
                        "tertiary": "#006242",
                        "tertiary-fixed": "#6ffbbe",
                        "on-tertiary-fixed-variant": "#005236",
                        "error": "#ba1a1a",
                        "error-container": "#ffdad6",
                        "on-error-container": "#93000a",
                        "secondary-fixed": "#d3e4fe",
                        "on-secondary-fixed-variant": "#38485d"
                    },
                    fontFamily: {
                        sans: ["Inter", "sans-serif"],
                        display: ["Hanken Grotesk", "sans-serif"]
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-surface-bright font-sans text-on-surface antialiased">

    <aside class="hidden lg:flex flex-col h-screen w-64 fixed left-0 top-0 bg-surface-container-low border-r border-outline-variant p-4 gap-4 z-50">
        <div class="flex items-center gap-3 mb-6 px-2">
            <div class="w-10 h-10 bg-primary flex items-center justify-center rounded-lg text-on-primary">
                <span class="material-symbols-outlined">analytics</span>
            </div>
            <div>
                <h1 class="font-display font-bold text-xl text-primary leading-tight">RetailPulse</h1>
                <p class="text-[10px] font-semibold uppercase tracking-wider text-on-surface-variant">Management Suite</p>
            </div>
        </div>
        
        <nav class="flex-1 flex flex-col gap-1">
            <a href="#" class="flex items-center gap-3 bg-primary text-on-primary rounded-lg px-4 py-2.5 transition-all">
                <span class="material-symbols-outlined text-xl">dashboard</span>
                <span class="text-sm font-medium">Dashboard</span>
            </a>
            <a href="#" class="flex items-center gap-3 text-on-surface-variant hover:bg-white/60 rounded-lg px-4 py-2.5 transition-all">
                <span class="material-symbols-outlined text-xl">inventory_2</span>
                <span class="text-sm font-medium">Inventory</span>
            </a>
            <a href="#" class="flex items-center gap-3 text-on-surface-variant hover:bg-white/60 rounded-lg px-4 py-2.5 transition-all">
                <span class="material-symbols-outlined text-xl">payments</span>
                <span class="text-sm font-medium">Sales</span>
            </a>
        </nav>

        <div class="mt-auto border-t border-outline-variant pt-4 flex flex-col gap-1">
            <button class="w-full bg-primary hover:bg-primary-container text-white text-sm font-medium py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors">
                <span class="material-symbols-outlined text-lg">download</span>
                Export Report
            </button>
            <a href="#" class="flex items-center gap-3 text-on-surface-variant hover:bg-white/60 rounded-lg px-4 py-2.5 transition-all">
                <span class="material-symbols-outlined text-xl">settings</span>
                <span class="text-sm font-medium">Settings</span>
            </a>
        </div>
    </aside>

    <main class="lg:pl-64 flex flex-col min-h-screen">
        <header class="flex justify-between items-center w-full px-6 h-16 sticky top-0 z-40 bg-surface-bright border-b border-outline-variant">
            <div class="flex-1 max-w-md relative">
                <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-xl">search</span>
                <input class="w-full bg-white border border-outline-variant rounded-lg pl-10 pr-4 py-1.5 text-sm focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all" placeholder="Search metrics, records, transactions..." type="text"/>
            </div>
            
            <div class="flex items-center gap-4">
                <div class="flex gap-1">
                    <button class="p-2 text-on-surface-variant hover:bg-white rounded-full transition-colors"><span class="material-symbols-outlined text-xl">notifications</span></button>
                    <button class="p-2 text-on-surface-variant hover:bg-white rounded-full transition-colors"><span class="material-symbols-outlined text-xl">settings</span></button>
                </div>
                <div class="h-6 w-[1px] bg-outline-variant"></div>
                <div class="flex items-center gap-3">
                    <div class="text-right hidden sm:block">
                        <p class="text-sm font-semibold text-on-surface leading-none">Amanda Faris</p>
                        <p class="text-[11px] text-on-surface-variant mt-1">Senior Admin</p>
                    </div>
                    <div class="w-8 h-8 rounded-full bg-primary-container text-white font-bold text-xs flex items-center justify-center">AF</div>
                </div>
            </div>
        </header>

        <section class="p-6 space-y-6 flex-1">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h2 class="font-display font-bold text-2xl text-on-surface">Good Morning, Amanda</h2>
                    <p class="text-sm text-on-surface-variant">Here's your operational data snapshot for today.</p>
                </div>
                <div class="flex gap-2">
                    <button class="px-4 py-2 bg-white border border-outline-variant rounded-lg text-xs font-semibold uppercase tracking-wider text-on-surface-variant flex items-center gap-2 hover:bg-surface-container-low transition-colors">
                        <span class="material-symbols-outlined text-base">calendar_today</span> Last 30 Days
                    </button>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="bg-surface-container-lowest border border-outline-variant p-5 rounded-xl space-y-2 shadow-sm">
                    <div class="flex justify-between items-start">
                        <div class="p-2 bg-primary/10 text-primary rounded-lg"><span class="material-symbols-outlined">payments</span></div>
                        <span class="text-xs font-bold text-tertiary flex items-center gap-0.5">+12.5% <span class="material-symbols-outlined text-xs">trending_up</span></span>
                    </div>
                    <p class="text-xs font-semibold tracking-wider text-on-surface-variant uppercase">Total Revenue</p>
                    <h3 class="font-display font-bold text-3xl text-on-surface">$124,592</h3>
                    <p class="text-[11px] text-on-surface-variant">vs. $110,243 last month</p>
                </div>

                <div class="bg-surface-container-lowest border border-outline-variant p-5 rounded-xl space-y-2 shadow-sm">
                    <div class="flex justify-between items-start">
                        <div class="p-2 bg-primary/10 text-primary rounded-lg"><span class="material-symbols-outlined">shopping_cart</span></div>
                        <span class="text-xs font-bold text-tertiary flex items-center gap-0.5">+8.2% <span class="material-symbols-outlined text-xs">trending_up</span></span>
                    </div>
                    <p class="text-xs font-semibold tracking-wider text-on-surface-variant uppercase">Orders Placed</p>
                    <h3 class="font-display font-bold text-3xl text-on-surface">1,842</h3>
                    <p class="text-[11px] text-on-surface-variant">vs. 1,702 last month</p>
                </div>

                <div class="bg-surface-container-lowest border border-outline-variant p-5 rounded-xl space-y-2 shadow-sm">
                    <div class="flex justify-between items-start">
                        <div class="p-2 bg-primary/10 text-primary rounded-lg"><span class="material-symbols-outlined">avg_pace</span></div>
                        <span class="text-xs font-bold text-error flex items-center gap-0.5">-2.4% <span class="material-symbols-outlined text-xs">trending_down</span></span>
                    </div>
                    <p class="text-xs font-semibold tracking-wider text-on-surface-variant uppercase">Avg. Order Value</p>
                    <h3 class="font-display font-bold text-3xl text-on-surface">$67.64</h3>
                    <p class="text-[11px] text-on-surface-variant">vs. $69.30 last month</p>
                </div>

                <div class="bg-surface-container-lowest border border-outline-variant p-5 rounded-xl space-y-2 shadow-sm">
                    <div class="flex justify-between items-start">
                        <div class="p-2 bg-primary/10 text-primary rounded-lg"><span class="material-symbols-outlined">ads_click</span></div>
                        <span class="text-xs font-bold text-tertiary flex items-center gap-0.5">+0.8% <span class="material-symbols-outlined text-xs">trending_up</span></span>
                    </div>
                    <p class="text-xs font-semibold tracking-wider text-on-surface-variant uppercase">Conversion Rate</p>
                    <h3 class="font-display font-bold text-3xl text-on-surface">3.4%</h3>
                    <p class="text-[11px] text-on-surface-variant">vs. 2.6% last month</p>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 border border-outline-variant bg-surface-container-lowest p-5 rounded-xl flex flex-col min-h-[380px]">
                    <div class="flex justify-between items-center mb-6">
                        <h4 class="text-base font-semibold text-on-surface">Sales Performance Analysis</h4>
                        <div class="flex gap-3 text-xs text-on-surface-variant font-medium">
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-primary"></span> Current Period</span>
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-outline-variant"></span> Target Projection</span>
                        </div>
                    </div>
                    <div class="flex-1 w-full bg-surface-bright rounded-lg border border-dashed border-outline-variant relative flex items-end justify-between p-6 gap-2">
                        <div class="w-full bg-primary/20 rounded-t h-[40%] transition-all hover:bg-primary/30"></div>
                        <div class="w-full bg-primary/20 rounded-t h-[65%] transition-all hover:bg-primary/30"></div>
                        <div class="w-full bg-primary rounded-t h-[85%] relative group cursor-pointer">
                            <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-on-surface text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-20">Week 3: $34.2k</div>
                        </div>
                        <div class="w-full bg-primary/20 rounded-t h-[50%] transition-all hover:bg-primary/30"></div>
                        <div class="w-full bg-primary/20 rounded-t h-[75%] transition-all hover:bg-primary/30"></div>
                    </div>
                </div>

                <div class="border border-outline-variant bg-surface-container-lowest p-5 rounded-xl flex flex-col">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-base font-semibold text-on-surface">Top Performing Products</h4>
                        <a href="#" class="text-xs font-semibold text-primary hover:underline">View All</a>
                    </div>
                    <div class="flex-1 space-y-3">
                        <div class="flex items-center justify-between p-2 hover:bg-surface-bright rounded-lg transition-colors cursor-pointer">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-surface-container-low rounded-lg flex items-center justify-center text-on-surface-variant"><span class="material-symbols-outlined">apparel</span></div>
                                <div>
                                    <p class="text-sm font-semibold text-on-surface">Nike Air Max 270</p>
                                    <p class="text-xs text-on-surface-variant">Apparel & Footwear</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <p class="text-sm font-semibold text-on-surface">$1,420</p>
                                <p class="text-xs text-tertiary font-medium">14 sold</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="border border-outline-variant bg-surface-container-lowest rounded-xl overflow-hidden shadow-sm">
                <div class="px-5 py-4 bg-surface-container-low/40 border-b border-outline-variant flex justify-between items-center">
                    <h4 class="text-base font-semibold text-on-surface">Recent Ledger Transactions</h4>
                    <span class="material-symbols-outlined text-on-surface-variant cursor-pointer">filter_list</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-surface-container-low/20 border-b border-outline-variant text-[11px] font-semibold tracking-wider text-on-surface-variant uppercase">
                                <th class="p-4">Order Record ID</th>
                                <th class="p-4">Customer Entity</th>
                                <th class="p-4">Workflow Status</th>
                                <th class="p-4">Execution Date</th>
                                <th class="p-4 text-right">Captured Amount</th>
                            </tr>
                        </thead>
                        <tbody class="text-sm divide-y divide-outline-variant/60">
                            <tr class="hover:bg-surface-bright/80 transition-colors cursor-pointer">
                                <td class="p-4 font-medium text-primary">#ORD-90210</td>
                                <td class="p-4">James Sullivan</td>
                                <td class="p-4"><span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-tertiary-fixed text-on-tertiary-fixed-variant uppercase">Success</span></td>
                                <td class="p-4 text-on-surface-variant">Oct 24, 2023</td>
                                <td class="p-4 text-right font-semibold text-on-surface">$124.50</td>
                            </tr>
                            <tr class="hover:bg-surface-bright/80 transition-colors cursor-pointer">
                                <td class="p-4 font-medium text-primary">#ORD-90209</td>
                                <td class="p-4">Maria Williams</td>
                                <td class="p-4"><span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-secondary-fixed text-on-secondary-fixed-variant uppercase">Pending</span></td>
                                <td class="p-4 text-on-surface-variant">Oct 24, 2023</td>
                                <td class="p-4 text-right font-semibold text-on-surface">$2,104.99</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <footer class="mt-auto py-4 px-6 border-t border-outline-variant bg-surface-container-low/30 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-on-surface-variant">
            <p>© 2026 RetailPulse Systems Corp. All operations logs verified securely.</p>
            <div class="flex gap-4">
                <a href="#" class="hover:text-primary transition-colors">Security Protocol</a>
                <a href="#" class="hover:text-primary transition-colors">API Architecture docs</a>
            </div>
        </footer>
    </main>

    <nav class="lg:hidden fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-outline-variant flex items-center justify-around z-50 shadow-lg px-2">
        <button class="flex flex-col items-center justify-center gap-0.5 text-primary">
            <span class="material-symbols-outlined text-2xl">dashboard</span>
            <span class="text-[9px] font-bold tracking-tight uppercase">Home</span>
        </button>
        <button class="flex flex-col items-center justify-center gap-0.5 text-on-surface-variant">
            <span class="material-symbols-outlined text-2xl">inventory_2</span>
            <span class="text-[9px] font-bold tracking-tight uppercase">Stock</span>
        </button>
        <button class="flex flex-col items-center justify-center gap-0.5 text-on-surface-variant">
            <span class="material-symbols-outlined text-2xl">payments</span>
            <span class="text-[9px] font-bold tracking-tight uppercase">Sales</span>
        </button>
    </nav>

</body>
</html>
6. Verification and Layout Accuracy Checklist
To maintain visual accuracy, verify that your implementation meets the following core layouts and design constraints:

Sidebar Isolation Boundary: Ensure that main is bound with an explicit lg:pl-64 margin layout. This preserves structural spacing and keeps the main canvas content from sliding under the left navigation column on wide layouts.

Explicit Image Alt Handling: All profile images and transactional thumbnails must use valid alt descriptors or clear SVG fallback frameworks to ensure high usability and smooth screen-reader performance.

Color Identity Contrast Rules: Background values using light layout blocks (bg-surface-container-lowest) must clear at least a 4.5:1 text-to-surface contrast ratio. This keeps typography sharp and highly readable against light surfaces or subtle table container styles.

Bento Breakdown Stability: Verify that the multi-card row scales smoothly down to a single column on compact interfaces (grid-cols-1 md:grid-cols-2 lg:grid-cols-4). This layout responsiveness preserves metric readouts and prevents text truncation across smaller tablet or mobile displays.