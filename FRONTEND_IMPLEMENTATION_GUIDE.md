# Mo-Wallet Frontend Implementation Guide

This guide provides code examples and implementation strategies for the frontend redesign.

---

## 1. Design System Implementation (Tailwind CSS)

### 1.1 Tailwind Configuration (Enhanced Django Option)

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          500: '#5B21B6',
          600: '#4C1D95',
          700: '#3C0F7B',
          900: '#1F0A47',
        },
        success: {
          50: '#f0fdf4',
          500: '#10B981',
          600: '#059669',
        },
        warning: {
          50: '#fffbeb',
          500: '#F59E0B',
          600: '#D97706',
        },
        danger: {
          50: '#fef2f2',
          500: '#EF4444',
          600: '#DC2626',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
      },
      spacing: {
        xs: '0.25rem',
        sm: '0.5rem',
        md: '1rem',
        lg: '1.5rem',
        xl: '2rem',
        '2xl': '3rem',
      },
      boxShadow: {
        sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
        base: '0 2px 4px rgba(0, 0, 0, 0.1)',
        md: '0 4px 8px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 25px rgba(0, 0, 0, 0.1)',
      },
      borderRadius: {
        xs: '0.25rem',
        sm: '0.375rem',
        base: '0.5rem',
        md: '0.75rem',
        lg: '1rem',
      },
    },
  },
  plugins: [],
};
```

---

## 2. Reusable Component Examples

### 2.1 Card Component (with Tailwind)

```html
<!-- templates/components/card.html -->
<div class="bg-white rounded-lg shadow-base border border-gray-200 transition-all hover:shadow-md hover:-translate-y-0.5">
    {{ content }}
</div>

<!-- Usage in template -->
{% include "components/card.html" with content=card_content %}
```

### 2.2 Button Component System

```html
<!-- templates/components/button.html -->
{% load static %}

<button 
  class="
    px-4 py-2 rounded-md font-medium transition-all duration-200
    {% if variant == 'primary' %}
      bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700
      focus:outline-none focus:ring-2 focus:ring-primary-300
    {% elif variant == 'secondary' %}
      bg-gray-100 text-gray-900 hover:bg-gray-200 border border-gray-300
      focus:outline-none focus:ring-2 focus:ring-gray-300
    {% elif variant == 'danger' %}
      bg-danger-500 text-white hover:bg-danger-600 active:bg-danger-700
      focus:outline-none focus:ring-2 focus:ring-danger-300
    {% elif variant == 'outline' %}
      border-2 border-primary-500 text-primary-500 hover:bg-primary-50
      focus:outline-none focus:ring-2 focus:ring-primary-300
    {% endif %}
    {% if size == 'sm' %}px-3 py-1 text-sm{% elif size == 'lg' %}px-6 py-3 text-lg{% endif %}
    {% if disabled %}opacity-50 cursor-not-allowed{% endif %}
    "
  {% if disabled %}disabled{% endif %}
>
  {% if icon %}<i class="fas fa-{{ icon }} mr-2"></i>{% endif %}
  {{ label }}
</button>
```

### 2.3 Stat Card Component

```html
<!-- templates/components/stat_card.html -->
<div class="bg-white rounded-lg shadow-base p-6 border-l-4 {% if status == 'success' %}border-l-success-500{% elif status == 'warning' %}border-l-warning-500{% else %}border-l-danger-500{% endif %}">
    <div class="flex justify-between items-start">
        <div>
            <p class="text-gray-600 text-sm font-medium uppercase">{{ label }}</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ value }}</p>
            {% if trend %}
            <div class="mt-2 flex items-center text-sm">
                <i class="fas fa-arrow-{% if trend > 0 %}up{% else %}down{% endif %} mr-1 {% if trend > 0 %}text-success-500{% else %}text-danger-500{% endif %}"></i>
                <span class="{% if trend > 0 %}text-success-600{% else %}text-danger-600{% endif %}">{{ trend|abs }}%</span>
                <span class="text-gray-500 ml-1">vs last month</span>
            </div>
            {% endif %}
        </div>
        {% if icon %}
        <div class="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center">
            <i class="fas fa-{{ icon }} text-xl text-gray-600"></i>
        </div>
        {% endif %}
    </div>
</div>
```

### 2.4 Progress Indicator Component

```html
<!-- templates/components/progress_indicator.html -->
<div class="w-full">
    <div class="flex justify-between items-center mb-2">
        <span class="text-sm font-medium text-gray-700">{{ label }}</span>
        <span class="text-sm font-semibold text-gray-900">{{ percentage|floatformat:1 }}%</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
        <div 
          class="h-full rounded-full transition-all duration-300 {% if percentage >= 90 %}bg-danger-500{% elif percentage >= 75 %}bg-warning-500{% else %}bg-success-500{% endif %}"
          style="width: {{ percentage }}%;"
        ></div>
    </div>
    {% if subtitle %}
    <p class="text-xs text-gray-600 mt-1">{{ subtitle }}</p>
    {% endif %}
</div>
```

### 2.5 Form Input Component

```html
<!-- templates/components/form_input.html -->
<div class="mb-4">
    <label for="{{ field_name }}" class="block text-sm font-medium text-gray-700 mb-1">
        {{ label }}
        {% if required %}<span class="text-danger-500">*</span>{% endif %}
    </label>
    <div class="relative">
        {% if prefix %}
        <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm font-medium">
            {{ prefix }}
        </span>
        <input 
          type="{{ input_type|default:'text' }}"
          name="{{ field_name }}"
          id="{{ field_name }}"
          class="w-full pl-12 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-500 transition-colors"
          {% if placeholder %}placeholder="{{ placeholder }}"{% endif %}
          {% if required %}required{% endif %}
          {% if value %}value="{{ value }}"{% endif %}
        />
        {% else %}
        <input 
          type="{{ input_type|default:'text' }}"
          name="{{ field_name }}"
          id="{{ field_name }}"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-500 transition-colors"
          {% if placeholder %}placeholder="{{ placeholder }}"{% endif %}
          {% if required %}required{% endif %}
          {% if value %}value="{{ value }}"{% endif %}
        />
        {% endif %}
    </div>
    {% if helper_text %}
    <p class="text-xs text-gray-500 mt-1">{{ helper_text }}</p>
    {% endif %}
</div>
```

---

## 3. Dashboard Redesign Example

### 3.1 Enhanced Dashboard Template

```html
<!-- templates/dashboard_redesigned.html -->
{% extends 'base.html' %}
{% load humanize %}
{% load custom_filters %}

{% block content %}
<div class="space-y-6">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-8 text-white mb-8">
        <h1 class="text-3xl font-bold mb-2">Welcome back, {{ user.first_name|default:user.username }}!</h1>
        <p class="text-primary-100">Here's your financial overview for {{ current_month_name }}</p>
    </div>

    <!-- Key Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Income Card -->
        {% include "components/stat_card.html" with 
            label="Monthly Income" 
            value="KES " 
            trend=income_trend 
            status="success" 
            icon="wallet"
        %}

        <!-- Expenses Card -->
        {% include "components/stat_card.html" with 
            label="Monthly Expenses" 
            value="KES " 
            trend=expense_trend 
            status="danger" 
            icon="credit-card"
        %}

        <!-- Savings Rate Card -->
        {% include "components/stat_card.html" with 
            label="Savings Rate" 
            value=savings_rate|add:"%" 
            status="warning" 
            icon="piggy-bank"
        %}

        <!-- Goals Progress Card -->
        {% include "components/stat_card.html" with 
            label="Active Goals" 
            value=active_goals_count 
            status="info" 
            icon="bullseye"
        %}
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Budget Status (spans 2 columns) -->
        <div class="lg:col-span-2">
            <div class="bg-white rounded-lg shadow-base p-6">
                <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
                    <i class="fas fa-chart-pie text-primary-500 mr-2"></i>
                    Budget Overview
                </h2>
                
                <div class="space-y-4">
                    {% for budget in budgets %}
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <h3 class="font-medium text-gray-900">{{ budget.get_category_display }}</h3>
                            <span class="text-sm font-semibold text-gray-600">
                                KES {{ budget.amount_spent|floatformat:0|intcomma }} / KES {{ budget.limit|floatformat:0|intcomma }}
                            </span>
                        </div>
                        {% include "components/progress_indicator.html" with 
                            percentage=budget.percentage_used 
                            label="" 
                            subtitle=budget.percentage_used|floatformat:1+"%"
                        %}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Savings Goals (sidebar) -->
        <div class="bg-white rounded-lg shadow-base p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <i class="fas fa-target text-warning-500 mr-2"></i>
                Active Goals
            </h2>
            
            <div class="space-y-4">
                {% for goal in active_goals %}
                <div class="p-3 bg-gray-50 rounded-md">
                    <h3 class="font-medium text-gray-900 text-sm">{{ goal.goal_name }}</h3>
                    <p class="text-xs text-gray-600 mt-1">KES {{ goal.current_savings|intcomma }} / {{ goal.target_amount|intcomma }}</p>
                    <div class="mt-2 w-full bg-gray-200 rounded-full h-1.5">
                        <div 
                          class="h-full bg-success-500 rounded-full" 
                          style="width: {{ goal.progress }}%;"
                        ></div>
                    </div>
                </div>
                {% endfor %}
                
                <button class="w-full mt-4 px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-600 transition-colors font-medium text-sm">
                    <i class="fas fa-plus mr-1"></i> New Goal
                </button>
            </div>
        </div>
    </div>

    <!-- Recent Transactions -->
    <div class="bg-white rounded-lg shadow-base p-6">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-gray-900 flex items-center">
                <i class="fas fa-exchange-alt text-primary-500 mr-2"></i>
                Recent Transactions
            </h2>
            <a href="{% url 'transactions:transactions' %}" class="text-primary-500 hover:text-primary-600 text-sm font-medium">
                View all <i class="fas fa-arrow-right ml-1"></i>
            </a>
        </div>

        <div class="overflow-x-auto">
            <table class="w-full">
                <thead class="border-b border-gray-200">
                    <tr>
                        <th class="text-left py-3 px-4 font-semibold text-gray-700 text-sm">Description</th>
                        <th class="text-left py-3 px-4 font-semibold text-gray-700 text-sm">Category</th>
                        <th class="text-left py-3 px-4 font-semibold text-gray-700 text-sm">Amount</th>
                        <th class="text-left py-3 px-4 font-semibold text-gray-700 text-sm">Date</th>
                        <th class="text-center py-3 px-4 font-semibold text-gray-700 text-sm">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for transaction in recent_transactions %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                        <td class="py-3 px-4">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-{% if transaction.transaction_type == 'income' %}arrow-down{% else %}arrow-up{% endif %} text-primary-600 text-xs"></i>
                                </div>
                                <span class="font-medium text-gray-900">{{ transaction.description }}</span>
                            </div>
                        </td>
                        <td class="py-3 px-4">
                            <span class="text-sm text-gray-600">{{ transaction.get_category_display }}</span>
                        </td>
                        <td class="py-3 px-4">
                            <span class="font-semibold {% if transaction.transaction_type == 'income' %}text-success-600{% else %}text-gray-900{% endif %}">
                                {% if transaction.transaction_type == 'income' %}+{% else %}-{% endif %}KES {{ transaction.amount|floatformat:0|intcomma }}
                            </span>
                        </td>
                        <td class="py-3 px-4">
                            <span class="text-sm text-gray-600">{{ transaction.transaction_date|date:"M d, Y" }}</span>
                        </td>
                        <td class="py-3 px-4 text-center">
                            <span class="inline-block px-2 py-1 rounded-full text-xs font-medium bg-success-100 text-success-700">
                                Completed
                            </span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>

<style>
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide {
  animation: slideIn 0.3s ease-out;
}
</style>
{% endblock %}
```

---

## 4. HTMX Integration for Interactivity

### 4.1 Budget Edit (with HTMX)

```html
<!-- templates/budget/budget_row.html -->
<tr class="hover:bg-gray-50" id="budget-{{ budget.id }}">
    <td class="py-3 px-4">{{ budget.get_category_display }}</td>
    <td class="py-3 px-4">KES {{ budget.limit|floatformat:0|intcomma }}</td>
    <td class="py-3 px-4">KES {{ budget.amount_spent|floatformat:0|intcomma }}</td>
    <td class="py-3 px-4">
        <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-primary-500 h-2 rounded-full" style="width: {{ budget.percentage_used }}%"></div>
        </div>
    </td>
    <td class="py-3 px-4">
        <div class="flex gap-2">
            <button 
              hx-get="{% url 'budget:edit' budget.id %}"
              hx-target="#budget-modal"
              hx-swap="innerHTML"
              class="px-3 py-1 text-sm bg-primary-100 text-primary-700 rounded hover:bg-primary-200"
            >
                <i class="fas fa-edit"></i> Edit
            </button>
            <button 
              hx-delete="{% url 'budget:delete' budget.id %}"
              hx-confirm="Are you sure?"
              hx-swap="outerHTML swap:1s"
              class="px-3 py-1 text-sm bg-danger-100 text-danger-700 rounded hover:bg-danger-200"
            >
                <i class="fas fa-trash"></i> Delete
            </button>
        </div>
    </td>
</tr>
```

### 4.2 Django View with HTMX

```python
# budget/views.py
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRefresh

@require_http_methods(["DELETE"])
@login_required
def delete_budget(request, budget_id):
    try:
        budget = Budget.objects.get(id=budget_id, user=request.user)
        budget.delete()
        # Return empty response - htmx will remove the row
        return HttpResponse(status=200)
    except Budget.DoesNotExist:
        return HttpResponse('Budget not found', status=404)

@require_http_methods(["GET"])
@login_required
def edit_budget(request, budget_id):
    budget = Budget.objects.get(id=budget_id, user=request.user)
    return render(request, 'budget/edit_modal.html', {'budget': budget})
```

---

## 5. API Integration Example (REST Framework)

### 5.1 Budget API Serializer

```python
# budget/serializers.py
from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    spent_percentage = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_display', 'limit', 'amount_spent', 'spent_percentage']
    
    def get_spent_percentage(self, obj):
        if obj.limit > 0:
            return (obj.amount_spent / obj.limit) * 100
        return 0
    
    def get_category_display(self, obj):
        return obj.get_category_display()
```

### 5.2 Budget API View

```python
# budget/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class BudgetListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

---

## 6. Database Query Optimization

### 6.1 Efficient Dashboard Queries

```python
# core/views.py
from django.db.models import Sum, Case, When, F, Value
from django.utils import timezone

def optimized_dashboard_view(request):
    user = request.user
    today = timezone.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Use select_related and prefetch_related
    budgets = Budget.objects.filter(user=user).select_related('user')
    
    # Single query for transactions
    month_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=start_of_month
    ).values('transaction_type').annotate(
        total=Sum('amount')
    )
    
    # Cache heavy computations
    from django.core.cache import cache
    cache_key = f'dashboard_metrics_{user.id}'
    metrics = cache.get(cache_key)
    
    if not metrics:
        # Expensive calculations here
        metrics = calculate_metrics(user, start_of_month)
        cache.set(cache_key, metrics, 300)  # Cache for 5 minutes
    
    return metrics
```

---

## 7. Frontend Testing Example (Jest + React)

```javascript
// __tests__/StatCard.test.js
import { render, screen } from '@testing-library/react';
import StatCard from '../components/StatCard';

describe('StatCard Component', () => {
  it('renders stat card with correct values', () => {
    render(
      <StatCard
        label="Monthly Income"
        value="KES 50,000"
        trend={12}
        status="success"
        icon="wallet"
      />
    );
    
    expect(screen.getByText('Monthly Income')).toBeInTheDocument();
    expect(screen.getByText('KES 50,000')).toBeInTheDocument();
    expect(screen.getByText('12%')).toBeInTheDocument();
  });

  it('displays correct trend color for positive trend', () => {
    const { container } = render(
      <StatCard label="Income" value="10000" trend={5} status="success" />
    );
    
    const trendElement = container.querySelector('.text-success-600');
    expect(trendElement).toBeInTheDocument();
  });
});
```

---

## 8. CSS Custom Properties (Design Tokens)

```css
/* styles/variables.css */
:root {
  /* Colors */
  --color-primary: #5B21B6;
  --color-primary-light: #8B5CF6;
  --color-primary-dark: #3C0F7B;
  
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  
  --color-text-primary: #1F2937;
  --color-text-secondary: #6B7280;
  --color-text-light: #9CA3AF;
  
  --color-bg-light: #F3F4F6;
  --color-bg-white: #FFFFFF;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  
  /* Typography */
  --font-sans: 'Inter', 'Segoe UI', sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.5rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-base: 0 2px 4px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
  
  /* Border Radius */
  --radius-sm: 0.375rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  
  /* Transitions */
  --transition-fast: 150ms ease-in-out;
  --transition-base: 300ms ease-in-out;
}

/* Usage */
.card {
  background: var(--color-bg-white);
  color: var(--color-text-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-base);
  padding: var(--space-lg);
  transition: box-shadow var(--transition-base);
}

.card:hover {
  box-shadow: var(--shadow-md);
}
```

---

## 9. Performance Monitoring

```javascript
// utils/performance.js
export function initPerformanceMonitoring() {
  // Measure Largest Contentful Paint (LCP)
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log('LCP:', entry.renderTime || entry.loadTime);
    }
  }).observe({ type: 'largest-contentful-paint', buffered: true });

  // Measure Cumulative Layout Shift (CLS)
  let clsValue = 0;
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (!entry.hadRecentInput) {
        clsValue += entry.value;
        console.log('CLS:', clsValue);
      }
    }
  }).observe({ type: 'layout-shift', buffered: true });

  // Custom event tracking
  window.addEventListener('load', () => {
    const perfData = performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log('Page Load Time:', pageLoadTime);
    
    // Send to analytics
    if (window.gtag) {
      gtag('event', 'page_load_time', {
        'value': pageLoadTime
      });
    }
  });
}
```

---

## 10. Lazy Loading Implementation

```html
<!-- Lazy load images -->
<img 
  src="placeholder.png" 
  data-src="real-image.png"
  loading="lazy"
  alt="Dashboard"
  class="w-full rounded-lg"
/>

<!-- Script for lazy loading -->
<script>
  if ('IntersectionObserver' in window) {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });
    
    images.forEach(img => imageObserver.observe(img));
  }
</script>
```

---

## 11. Migration Strategy

### Phase 1: Design System & Components
- Set up Tailwind CSS
- Create component library
- Update base template

### Phase 2: Page Redesigns (Sequential)
- Dashboard (highest traffic)
- Budgets (frequently used)
- Transactions
- Analytics
- Goals

### Phase 3: Enhancement
- Add HTMX for interactivity
- Add animations
- Performance optimization

---

## 12. Resources & Tools

- **Design**: Figma, Storybook
- **Framework**: Next.js, React, Vue.js
- **Styling**: Tailwind CSS, Styled Components
- **Components**: Shadcn/ui, Headless UI
- **Testing**: Jest, Playwright, Vitest
- **Monitoring**: Sentry, LogRocket, Datadog

---

This implementation guide provides concrete starting points for each design system component and improvement area.

